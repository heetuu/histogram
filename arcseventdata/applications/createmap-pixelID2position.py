#!/usr/bin/env python

# This script creates the map to convert pixelID to the postion of the pixel

def createMap( arcs, nPixelsPerDetector, nDetectorsPerPack, nPacks ):

    nPixelsPerPack = nDetectorsPerPack * nPixelsPerDetector

    assert nPixelsPerPack%1024==0
    assert nDetectorsPerPack==8

    # number of bits to shift
    from math import log
    nbits_pack = int( log( nPixelsPerPack, 2 ) )
    nbits_det = int( log( nPixelsPerDetector, 2 ) )
    ntotpixels = (nPacks+1) << nbits_pack

    # array to hold results
    import numpy
    res = numpy.zeros( ntotpixels * 3, 'd' )
    res.shape = ntotpixels, 3


    from pyre.units.length import meter
    
    from instrument.elements.DetectorVisitor import DetectorVisitor

    class Mapper( DetectorVisitor ):

        onDetector = DetectorVisitor.onElementContainer

        def onPixel(self, pixel):
            indexes = self.indexes(  )

            position = self._geometer.positionRelativeToSample( indexes )

            detindexes = self.detindexes()

            packID, detID, pixelID = detindexes
            
            longpixelID = pixelID + (detID << nbits_det) + ( (packID+1) << nbits_pack )

            res[longpixelID] = position/meter

            #print detindexes, longpixelID, res[longpixelID]
            
            return

        pass # end of Mapper

    Mapper().render( arcs, arcs.geometer )

    return res


def help():
    msg = '''
createmap-pixelID2position.py  ARCS.xml
'''
    print msg
    return


def main():
    import sys
    if len(sys.argv) != 2:
        help()
        exit(1)
    arcsxml = sys.argv[1]

    from instrument.nixml import parse_file
    arcs = parse_file( arcsxml )

    nPixelsPerDetector = 128
    nDetectorsPerPack = 8
    nPacks = len(arcs.getDetectorSystem().elements())
    
    pixelID2position = createMap( arcs, nPixelsPerDetector, nDetectorsPerPack, nPacks )

    import pickle
    pickle.dump( pixelID2position, open('pixelID2position.pkl','w'))

    return


if __name__ == '__main__': main()

    
