#!/usr/bin/env python

## This script convert the binary data file created
## by e2Ipt to a histogram and save it to hdf5 file.

def run( binfilename, h5filename, tofparams ):
    print binfilename , h5filename, tofparams, "unit:microsecond"

    s = open(binfilename, 'rb' ).read()
    import numpy
    a = numpy.fromstring(s, 'u4' )
    a.shape = 115,8,128,-1
    
    from histogram import histogram, arange

    tofbegin, tofend, tofstep = tofparams

    h = histogram(
        'Iddpt',
        [ ('detectorpackID', range(115) ),
          ('detectorID', range(8) ),
          ('pixelID', range(128) ),
          ('tof', arange(tofbegin,tofend, tofstep), 'microsecond'),
          ],
        data = a )

    from histogram.hdf import dump
    dump( h, h5filename, '/', 'c' )

    return


def main():
    import sys

    argv = sys.argv

    binfilename = argv[1]

    h5filename = argv[2]

    tofparams = eval( argv[3] )

    run(binfilename, h5filename, tofparams)

    return


if __name__ == '__main__': main()

    
