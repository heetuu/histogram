#!/usr/bin/env python

## This script reads events from event data file
## and create a histogram hdf5 file

def run( eventdatafilename, nevents, h5filename, tofparams ):
    print "eventdatafilename = %s" % eventdatafilename
    print "nevents = %s" % nevents
    print "h5filename = %s" % h5filename
    print 'tofparams (microseconds) = %s' % (tofparams, )

    tofbegin, tofend, tofstep = tofparams # microsecond
    
    import os
    iptbinary = 'Ipt.%s-%s-%s(microseconds).bin' % (
        eventdatafilename, nevents, tofparams)
    cmd = 'e2Ipt "%s" %s %s %s %s "%s" ' % (
        eventdatafilename, nevents,
        tofbegin*10, tofend*10, tofstep*10, # 100 ns
        iptbinary )
    if os.system( cmd ): raise "%s failed" % cmd

    if not os.path.exists( iptbinary ): raise "%s was not created" % iptbinary
    
    cmd = 'binary2histogram.py "%s" "%s" "%s"' % (
        iptbinary, h5filename, tofparams )
    if os.system(cmd): raise "%s failed" % cmd
    if not os.path.exists( h5filename ): raise "%s was not created" %(
        h5filename,)
    return


def help():
    m = '''
e2Ipt.py eventdatafilename nevents h5filename tofparams(begin,end,step; units=microsecond)
'''
    print m
    return


def main():
    import sys

    argv = sys.argv
    if len(argv) != 5:
        help()
        sys.exit(3)

    eventdatafilename = argv[1]
    nevents = int( argv[2] )

    h5filename = argv[3]

    tofparams = eval( argv[4] )

    run(eventdatafilename, nevents, h5filename, tofparams)

    return


if __name__ == '__main__': main()

    
