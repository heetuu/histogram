# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = arcseventdata
PACKAGE = applications


PROJ_LIBRARIES = -L$(BLD_LIBDIR) -larcseventdata


# directory structure

BUILD_DIRS = \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse



EXPORT_PYTHON_MODULES = \




itof: events2Itof.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ events2Itof.cc $(PROJ_LIBRARIES)

idspacing: events2Id.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ events2Id.cc $(PROJ_LIBRARIES)



PROJ_CPPEXE = itof idspacing

EXPORT_PYAPPS = \
	createmap-pixelID2position.py \
	numpyarray2binary.py \


EXPORT_BINS = $(PROJ_CPPEXE) $(EXPORT_PYAPPS)

export-binaries:: $(EXPORT_BINS)

export:: export-binaries release-binaries #export-package-python-modules 


# version
# $Id$

# End of file
