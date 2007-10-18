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
PACKAGE = tests

PROJ_CLEAN += $(PROJ_CPPTESTS)

PROJ_PYTESTS = signon.py histogramFrom2colascii_TestCase.py
PROJ_CPPTESTS = test_Histogrammer1 test_Event2Quantity test_IxHistogrammer test_events2Ix test_EventsReader test_Event2d
PROJ_CPPEXE = 
PROJ_TESTS = $(PROJ_PYTESTS) $(PROJ_CPPTESTS) $(PROJ_CPPEXE)
PROJ_LIBRARIES = -L$(BLD_LIBDIR) -larcseventdata


#--------------------------------------------------------------------------
#

all: $(PROJ_TESTS)

test:
	for test in $(PROJ_TESTS) ; do $${test}; done

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#

test_Histogrammer1: test_Histogrammer1.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_Histogrammer1.cc $(PROJ_LIBRARIES)

test_IxHistogrammer: test_IxHistogrammer.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_IxHistogrammer.cc $(PROJ_LIBRARIES)

test_Event2Quantity: test_Event2Quantity.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_Event2Quantity.cc $(PROJ_LIBRARIES)

test_EventsReader: test_EventsReader.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_EventsReader.cc $(PROJ_LIBRARIES)

test_events2Ix: test_events2Ix.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_events2Ix.cc $(PROJ_LIBRARIES)

test_Event2d: test_Event2d.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_Event2d.cc $(PROJ_LIBRARIES)




# version
# $Id$

# End of file
