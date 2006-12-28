#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from DiscretizedAxis import DiscretizedAxis

class AxisWithBins(DiscretizedAxis):

    def __init__(self, physical_quantity_type, binBoundaries, binCenters = None):
        self._binBoundaries = binBoundaries
        if binCenters is None: binCenters = _calcBinCenters( binBoundaries )
        DiscretizedAxis.__init__(self, physical_quantity_type, binCenters)
        return


    def __getitem__(self, s):
        if not isSlicingInfo(s): raise NotImplementedError , \
           "cannot get slice (%s)" % s
        s = self.slicingInfo2IndexSlice( s )
        #need 1 more boundary than center
        step = s.step
        if step is None: step = 1
        #
        newBBs= self._binBoundaries [ slice(s.start, s.stop + step, step) ]
        newBCs = self._values[s]
        return AxisWithBins( self._physical_quantity_type, newBBs,
                             binCenters = newBCs )


    def binCenters(self): return self.values()


    def binBoundaries(self): return self._binBoundaries

    pass


def _calcBinCenters( bbs ):
    return [ (bbs[i] + bbs[i+1])/2. for i in range( len(bbs) -1 ) ]


from SlicingInfo import isSlicingInfo


def test():
    from PhysicalQuantity import newType, new
    from pyre.units.energy import eV
    Ee = newType( "electron energy", eV )

    from AbstractDiscreteAxis import TestCase as TC

    class TestCase(TC):

        def setUp(self):
            self.axis = AxisWithBins( Ee, [-5.5, -4.5, -3.5, -2.5] )
            return


        def test_values(self):
            "DiscretizedAxis: values"
            TC.test_values(self)
            return


        def test_index(self):
            "DiscretizedAxis: index"
            from PhysicalQuantity import new
            axis = self.axis
            self.assertEqual( axis.index( new(Ee, -5.0 ) ), 0 )
            self.assertEqual( axis.index( new(Ee, -4.0 ) ), 1 )
            self.assertRaises( IndexError, axis.index, new(Ee, -2.0 ) )
            return

        pass

    import unittest as ut
    suite = ut.makeSuite( TestCase )
    alltests = ut.TestSuite( (suite, ) )
    ut.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == "__main__": test()


# version
__id__ = "$Id$"

# End of file 
