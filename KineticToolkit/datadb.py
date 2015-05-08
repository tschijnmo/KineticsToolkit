"""
The database for computation results
====================================

For maximum flexibility, the database is designed as a linear list of
computation results. With each result given as a mapping with flexible keys
and values. In this module, utilities for reading, writing, and querying such
database are provided.

.. autosummary::
    :toctree:

    DataDB

"""

from collections import abc
import shutil

from yaml import load, dump, YAMLError

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class DataDB(object):

    """
    The database for computation results

    A database is always bind to a YAML file on the disk. The content of the
    file is going to initialize the content of the database. And if the
    database is updated, the results can be written back to disk. Also
    utilities for querying the database is provided as methods of the class.

    ..warning::

        Method :py:meth:`save` needs to be called explicitly to save of
        updated content of the database to disk.

    .. py:attribute:: file_name

        The name of the YAML file for the data base.

    .. py:attribute:: content

        The content of the database.

    .. py:attribute:: yaml_style

        A dictionary for the keyword arguments to be passed to the YAML
        dumper for the formatting of the YAML file. By default only the
        indentation by 4 will be forced.

    """

    #
    # Reading and saving the results
    #

    def __init__(self, file_name, **kwargs):
        """Initializes a database

        If the given files does not exist or is empty, the database will be
        initialized to an empty one, or the content of the file is going to
        be used for the initial content.

        :param str file_name: The name of the YAML file to bind this database.

        All the keyword arguments will be passed to the YAML dumper when
        formatting the output.
        """

        self.file_name = file_name

        try:
            with open(file_name, 'r') as input_file:
                input_content = load(input_file, Loader=Loader)
                if input_content is None:
                    raise IOError()
                elif not isinstance(input_content, abc.Sequence):
                    raise TypeError((
                        'Invalid content in YAML file {}!\n'
                        'A list of data points are needed!'
                    ).format(file_name))
        except IOError:
            # When the file is empty or does not exist.
            self.content = []
        except YAMLError:
            print('Invalid YAML file {}!'.format(file_name))
            raise

        self.yaml_style = {'indent': 4}
        self.yaml_style.update(kwargs)

    def save(self, file_name=None, bak_suffix='.bak'):
        """Save of content of the database

        This method will save the content of the current state of the data
        base to dist.

        :param str file_name: The name of the file to save the content. By
            default it is going to be the name of the file from which this
            database is initialized.
        :param str bak_suffix: The suffix for the backup of the old database
            file. If it is given as a False value, backing up of the old file
            will not be performed.
        :returns: None
        """

        # First perform the backup if request.
        if bak_suffix:
            bak_file_name = self.file_name + bak_suffix
            shutil.copyfile(self.file_name, bak_file_name)

        # Next dump the current content of the database.
        if file_name is None:
            file_name = self.file_name

        try:
            with open(file_name, 'w') as out_fp:
                dump(
                    self.content, stream=out_fp, Dumper=Dumper,
                    **self.yaml_style
                )
        except IOError:
            print('Cannot open the output file {}'.format(file_name))
            raise

        return None

    #
    # Querying the database
    #

    def filter_data(self, keep_idx=False, **crit):
        """Filters the content and get the data points satisfying the criteria

        :param crit: The filtering criteria, given as keyword arguments. The
            keywords given are the names of the properties to test, which
            should be present in the data points to be filtered out. If the
            value is callable, then it will be called with the value of the
            property for it to return a boolean value indicating if the data
            point passes the test. If the value is not callable, the value of
            the property is going to be compared with it, only data points
            with the same value as given will be filtered.
        :param keep_idx: If the indices in the list of data is needed. If it is
            set to True, data points are going to be returned as pairs of
            index and the data point.
        :returns: A list of the data points that satisfies the criterion.
        :rtype: list
        """

        return [
            ((idx, data) if keep_idx else data)
            for idx, data in enumerate(self.content)
            if all(
                k in data and (
                    v(data[k]) if isinstance(v, abc.Callable) else data[k] == v
                )
                for k, v in crit.items()
            )
        ]

    def get_data(self, **kwargs):
        """Gets the only data point satisfying the criteria

        This method is semantically similar to the method
        :py:meth:`filter_data`. But it will assure that there is only one
        data point satisfying the criteria and return the single data point.
        """

        all_data = self.filter_data(**kwargs)

        if len(all_data) < 1:
            raise ValueError(
                'No data point is found satisfying the criteria!'
            )
        elif len(all_data) > 1:
            raise ValueError(
                'Multiple data points are found satisfying the criteria!'
            )
        else:
            return all_data[0]

    #
    # Small utilities for adding and removing data
    #

    def append_data(self, data):
        """Appends a new data point"""
        self.content.append(data)

    def remove_data(self, **crit):
        """Removes the data points with a criteria

        All data points satisfying the criteria are going to be removed.

        :returns: The number of data points that is removed.
        :rtype: int
        """

        # Find the indices of the data points to be removed.
        idxes = [
            i[0] for i in self.filter_data(keep_idx=True, **crit)
        ]

        # Note that this is only suitable for deleting a small number of data
        # points.
        self.content = [
            v for i, v in enumerate(self.content) if i not in idxes
        ]

        return len(idxes)
