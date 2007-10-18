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
## and create a histogram hdf5 file of I(dspacing)


# This script use the c++ program "idspacing" to extract I(dspacing) from
# an event-mode data file of ARCS, and save the histogram to a 2col ascii file.
# Then the ascii file is read, and a histogram object is created, and
# the histogram object is saved in a h5 file so that it is easier
# to manipulate in HistogramGUI.

import os

def run( eventdatafilename, nevents, pixelPositionsFilename, h5filename, dspacingparams ):
    print "eventdatafilename = %s" % eventdatafilename
    print "nevents = %s" % nevents
    print "pixel-positions-filename=%s" % pixelPositionsFilename
    print "output h5filename = %s" % h5filename
    print 'dspacingparams (unit: angstrom) = %s' % (dspacingparams, )

    if os.path.exists(h5filename):
        raise IOError, "%s already exists" % h5filename

    dspacingbegin, dspacingend, dspacingstep = dspacingparams # angstrom
    
    idspacingdat = 'Idspacing.%s-%s-%s(angstrom).dat' % (
        eventdatafilename, nevents, dspacingparams)
    cmd = 'idspacing "%s" %s "%s" %s %s %s "%s" ' % (
        eventdatafilename, nevents, pixelPositionsFilename,
        dspacingbegin, dspacingend, dspacingstep, 
        idspacingdat )
    if os.system( cmd ): raise "%s failed" % cmd

    if not os.path.exists( idspacingdat ): raise "%s was not created" % idspacingdat

    from arcseventdata.histogramFrom2colascii import convert
    h = convert( idspacingdat, name = "I(dspacing)", xname = 'dspacing', xunit = 'angstrom' )
    from histogram.hdf import dump
    dump(h, h5filename, '/', 'c' )
    return


def main():
    from optparse import OptionParser
    usage = "usage: %prog [options] event-data-file"
    parser = OptionParser(usage)
    #parser.add_option("-e", "--eventdatafile", dest="eventdatafile",
    #                  help="ARCS event data file")
    parser.add_option("-o", "--out", dest="h5filename", default = "Idspacing.h5",
                      help="hdf5 file of I(dspacing) histogram")
    parser.add_option("-n", "--nevents", dest="nevents", default = '1000',
                      type = 'int', help="number of events")
    parser.add_option("-t", "--dspacing", dest="dspacingparams", default = '0,5,0.01',
                      help="d-spacing bin parameters (begin, end, step). units: angstrom")
    parser.add_option("-p", "--pixel-positions", dest = "pixelPositionsFilename",
                      default = "pixelID2position.bin",
                      help="binary file containing pixel positions" )

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
        raise "should not reach here"

    eventdatafile = args[0]
    h5filename = options.h5filename
    nevents = options.nevents
    dspacingparams = eval( options.dspacingparams )
    pixelPositionsFilename = options.pixelPositionsFilename

    run( eventdatafile, nevents, pixelPositionsFilename, h5filename, dspacingparams )
    return

if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
