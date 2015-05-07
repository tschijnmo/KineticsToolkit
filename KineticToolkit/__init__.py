"""
Simple and extensible toolkit for theoretic chemical kinetics
=============================================================

In theoretic study of chemical kinetics, it is quite often that a large
amount of quantum chemical computation needs to be performed and recorded,
which could make the post-processing of the kinetics data quite cumbersome,
labour-intensive, and sometimes even error-prone. This package is designed to
make this process easier in a simple and extensible way. The computation
results can be stored in YAML files that act as database for research
projects. Utilities are provided in this package for both creating and
manipulating this YAML file and for the post-processing of the results.

This toolkit is designed to be simple, extensible, and flexible. In its core,
it only assumes the YAML file contains a list of data points, which are
mappings with keys being property names and values being property values. The
keys and values are not fixed to any particular set. Users only need to make
sure the properties stored in the mapping are consistent with the requirement
of the specific post-processing that is needed to be performed.

In this way, the archiving of the results is fully extensible. Also by using
YAML as the storage engine, rather than using some binary formats like SQLite
or formats that is essentially human-unreadable like XML, the YAML file can
be easily edited manually or put under version control.

Public modules of this package includes

.. autosummary::
    :toctree:

    datadb
    propnames
    energetics
    gauinter

All the public symbols of these modules are exported to the root package. So
only the root package needed to be imported for common usage.

"""