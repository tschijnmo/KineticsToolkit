"""
Constants for common property names
===================================

In order for different parts of the code to have got a common convention for
the names of properties of importance of data points, here in this module,
constants are defined for these names to facilitate the interoperability of
different parts of codes. Also, by using constants in this module, another
advantage is that typos in the property names are able to be captured by the
python interpreter.

Properties for the input of computations
----------------------------------------

.. py:data:: CONFIGURATION

    The configuration of the structure being computed. Normally given as a
    string for the name of the configuration.

.. py:data:: METHOD

    The computational methodology. Usually can be given as a string for the
    computational method of the computation. But it can also be more
    complicated structure if finer recording of method is what is concentrated.

Properties for the output of computations
-----------------------------------------

.. py:data:: COORDINATES

    The atomic coordinates. Usually given as a list of lists of atomic
    element symbol followed by three floating point numbers for the
    coordinate of the atoms, in Angstrom.

.. py:data:: ELECTRON_ENERGY

    The electronic energy of the system.

.. py:data:: ZERO_POINT_CORRECTION

    The zero-point correction to the base energy.

.. py:data:: GIBBS_THERMAL_CORRECTION

    The thermal correction to the Gibbs free energy.

.. py:data:: COUNTERPOISE_CORRECTION

    The counterpoise correction fot the basis set superposition error.

By convention the units for the energies is Hartree.

"""


CONFIGURATION = 'configuration'
METHOD = 'method'

COORDINATES = 'coordinates'
ELECTRON_ENERGY = 'electron_energy'
ZERO_POINT_CORRECTION = 'zero_point_correction'
GIIBS_THERMAL_CORRECTION = 'gibbs_thermal_correction'
COUNTERPOISE_CORRECTION = 'counterpoise_correction'

