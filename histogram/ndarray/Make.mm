# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao Lin
#                        California Institute of Technology
#                        (C) 2006 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = ndarray
PACKAGE = ndarray

#--------------------------------------------------------------------------
#

all: export

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
    __init__.py         \
    NdArray.py           \
    NumpyNdArray.py      \
    StdVectorNdArray.py      \


include doxygen/default.def

export:: export-python-modules 



# version
# $Id: Make.mm 118 2006-04-17 06:41:49Z jiao $

# End of file
