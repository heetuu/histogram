# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

include local.def

PROJECT = arcseventdata
PACKAGE = libarcseventdata

PROJ_SAR = $(BLD_LIBDIR)/$(PACKAGE).$(EXT_SAR)
PROJ_DLL = $(BLD_BINDIR)/$(PACKAGE).$(EXT_SO)
PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_CLEAN += $(PROJ_SAR) $(PROJ_DLL)

PROJ_SRCS = \
    histogrammer.cc \
    eventsToIpt.cc \

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# build the library

all: $(PROJ_SAR) export bins

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ifeq (Win32, ${findstring Win32, $(PLATFORM_ID)})

# build the shared object
$(PROJ_SAR): product_dirs $(PROJ_OBJS)
	$(CXX) $(LCXXFLAGS) -o $(PROJ_DLL) \
	-Wl,--out-implib=$(PROJ_SAR) $(PROJ_OBJS)

# export
export:: export-headers export-libraries export-binaries

else

# build the shared object
$(PROJ_SAR): product_dirs $(PROJ_OBJS)
	$(CXX) $(LCXXFLAGS) -o $(PROJ_SAR) $(PROJ_OBJS)

# export
export:: export-headers export-libraries

endif

EXPORT_HEADERS = \
    histogrammer.h \
    event.h \
    readevent.h \

EXPORT_LIBS = $(PROJ_SAR)
EXPORT_BINS = $(PROJ_DLL)


l2b: l2b.cc littleEndian2bigEndian.h
	g++ -o l2b l2b.cc

itof: itof.cc histogrammer.cc histogrammer.h
	g++ -o itof itof.cc histogrammer.cc

ipix: ipix.cc histogrammer.cc histogrammer.h
	g++ -o ipix ipix.cc histogrammer.cc

e2Ipt: e2Ipt.cc eventsToIpt.cc eventsToIpt.h histogrammer.cc histogrammer.h
	g++ -o e2Ipt e2Ipt.cc histogrammer.cc eventsToIpt.cc


test_event2d: test_event2d.cc event2d.cc event2d.h
	g++ -o test_event2d test_event2d.cc event2d.cc 

bins: l2b itof ipix e2Ipt

tests: test_event2d

# version
# $Id$

#
# End of file
