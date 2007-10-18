#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## This script reads events from event data file
## and create a histogram hdf5 file of I(tof)


# This script use the c++ program "itof" to extract I(tof) from
# an event-mode data file of ARCS, and save the histogram to a 2col ascii file.
# Then the ascii file is read, and a histogram object is created, and
# the histogram object is saved in a h5 file so that it is easier
# to manipulate in HistogramGUI.

import os

def run( eventdatafilename, nevents, h5filename, tofparams ):
    print "eventdatafilename = %s" % eventdatafilename
    print "nevents = %s" % nevents
    print "output h5filename = %s" % h5filename
    print 'tofparams (microseconds) = %s' % (tofparams, )

    if os.path.exists(h5filename):
        raise IOError, "%s already exists" % h5filename

    tofbegin, tofend, tofstep = tofparams # microsecond
    
    itofdat = 'Itof.%s-%s-%s(microseconds).dat' % (
        eventdatafilename, nevents, tofparams)
    cmd = 'itof "%s" %s %s %s %s "%s" ' % (
        eventdatafilename, nevents,
        tofbegin*10, tofend*10, tofstep*10, # 100 ns
        itofdat )
    if os.system( cmd ): raise "%s failed" % cmd

    if not os.path.exists( itofdat ): raise "%s was not created" % itofdat

    from arcseventdata.histogramFrom2colascii import convert
    h = convert( itofdat, name = "I(tof)", xname = 'tof', xunit = 'microsecond' )
    from histogram.hdf import dump
    dump(h, h5filename, '/', 'c' )
    return


def main():
    from optparse import OptionParser
    usage = "usage: %prog [options] event-data-file"
    parser = OptionParser(usage)
    #parser.add_option("-e", "--eventdatafile", dest="eventdatafile",
    #                  help="ARCS event data file")
    parser.add_option("-o", "--out", dest="h5filename", default = "Itof.h5",
                      help="hdf5 file of I(tof) histogram")
    parser.add_option("-n", "--nevents", dest="nevents", default = '1000',
                      type = 'int', help="number of events")
    parser.add_option("-t", "--tof", dest="tofparams", default = '0,10000, 100',
                      help="tof bin parameters (begin, end, step). units: microsecond")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
        raise "should not reach here"

    eventdatafile = args[0]
    h5filename = options.h5filename
    nevents = options.nevents
    tofparams = eval( options.tofparams )

    run( eventdatafile, nevents, h5filename, tofparams )
    return

if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
