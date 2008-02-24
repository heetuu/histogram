# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2003  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

PROJECT = array_kluge
PACKAGE = _array_klugemodule
MODULE = _array_kluge

include std-pythonmodule.def
include local.def

PROJ_CXX_SRCLIB = -ljournal

PROJ_SRCS = \
    bindings.cc \
    exceptions.cc \
    misc.cc \
    charPtr2stringBdgs.cc \
    vPtr2stdvectorPtrBdgs.cc \
    vPtr2numarrayBdgs.cc \


include doxygen/default.def
docs: export-doxygen-docs


# version
# $Id: Make.mm 55 2007-11-13 19:19:45Z linjiao $

# End of file
