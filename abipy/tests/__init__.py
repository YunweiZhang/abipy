"""
Common test support for all abipy test scripts.

This single module should provide all the common functionality for abipy tests
in a single location, so that test scripts can just import it and work right away.
"""
from __future__ import print_function, division

from os.path import join as pj, dirname, abspath

import os

__all__ = [
    "WFK_NCFILES",
    "DEN_NCFILES",
    "ALL_NCFILES",
    "get_ncfile",
    "get_ncfiles_with_ext",
    "get_reference_file",
]

_DATA_ABSPATH = abspath( pj(dirname(__file__), 'data') )

_CIF_DIRPATH = abspath( pj(dirname(__file__), 'data', "cifs") )

_PSEUDOS_DIRPATH = abspath( pj(dirname(__file__), 'data', "pseudos") )

try:
    _DATA_NCFILES = [pj(_DATA_ABSPATH, f) for f in os.listdir(_DATA_ABSPATH) if f.endswith(".nc")]
except:
    _DATA_NCFILES = list()

def get_ncfile(filename):
    """Return the absolute path of file filename locate in data. None if not found"""
    for f in _DATA_NCFILES:
        if os.path.basename(f) == filename:
            return f
    else:
        return None

def get_ncfiles_with_ext(ext):
    """Return a list with the absolute path of the files with extension ext"""
    ncfiles = []
    for filename in _DATA_NCFILES:
        f = filename.rstrip(".nc").rstrip("-etsf")
        if f.endswith("_"+ext):
            ncfiles.append(filename)
    return ncfiles

def get_reference_file(filename):
    """Returns the absolute path of filename in tests/data directory."""
    return os.path.join(_DATA_ABSPATH, filename)

def get_datadir():
    return _DATA_ABSPATH

def get_ciffile(filename):
    """Returns the absolute path of the CIF file in tests/data/cifs."""
    return os.path.join(_CIF_DIRPATH, filename)

def get_pseudo(filename):
    """Returns the absolute path of a pseudopotential file in tests/data/pseudos."""
    return os.path.join(_PSEUDOS_DIRPATH, filename)

def get_pseudos(*filenames):
    """Returns the absolute path of a pseudopotential file in tests/data/pseudos."""
    return [get_pseudo(f) for f in filenames]

##########################################################################################

WFK_NCFILES = get_ncfiles_with_ext("WFK")

DEN_NCFILES = get_ncfiles_with_ext("DEN")

ALL_NCFILES = WFK_NCFILES + DEN_NCFILES

##########################################################################################
