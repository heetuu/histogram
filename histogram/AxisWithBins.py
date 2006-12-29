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

    def __init__(self, quantity_binBoundaries):
        """ctor
        binBoundaries: bin boundaries. instance of PhysicalValueList
        """
        qbb = quantity_binBoundaries
        binBoundaries = self._binBoundaries = qbb.values
        self._binCenters = binCenters = _calcBinCenters( binBoundaries )
        qbc = QuantityValueList( qbb.quantity, binCenters )
        DiscretizedAxis.__init__(self, qbc)
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
        newqBBs = QuantityValueList( self.quantity(), newBBs )
        return AxisWithBins( newqBBs )


    def binCenters(self): return self._binCenters


    def binBoundaries(self): return self._binBoundaries

    pass


def _calcBinCenters( bbs ):
    unit = bbs.unit()
    bbvs = bbs.values()
    bcvs = [ (bbvs[i] + bbvs[i+1])/2. for i in range( len(bbvs) -1 ) ]
    return PhysicalValueList( unit, bcvs )


from SlicingInfo import isSlicingInfo
from QuantityValueList import QuantityValueList
from PhysicalValueList import PhysicalValueList


def test():
    from PhysicalQuantity import PhysicalQuantity
    from pyre.units.energy import eV
    Ee = PhysicalQuantity( "electron energy", eV )

    from AbstractDiscreteAxis import TestCase as TC

    class TestCase(TC):

        def setUp(self):
            energyValueList = PhysicalValueList(
                eV,  [-8.5, -7.5, -6.5, -5.5, -4.5, -3.5, -2.5] )
            EeValueList = QuantityValueList( Ee, energyValueList )
            self.axis = AxisWithBins( EeValueList )
            return


        def test_binCenters(self):
            "AxisWithBins: binCenters"
            bc = self.axis.binCenters()
            self.assertEqual( bc.__class__, PhysicalValueList )
            self.assertEqual( bc, PhysicalValueList(
                eV,  [-8., -7., -6., -5., -4., -3.] ) )
            return


        def test_values(self):
            "AxisWithBins: values"
            TC.test_values(self)
            return


        def test_index(self):
            "AxisWithBins: index"
            axis = self.axis
            self.assertEqual( axis.index( -5.0*eV ), 3 )
            self.assertEqual( axis.index( -4.0*eV ), 4 )
            self.assertRaises( ValueError, axis.index, -2.0*eV )
            return


        def test___eq__(self):
            "AxisWithBins: a == b"
            axis = self.axis
            import copy
            vs = copy.deepcopy( axis.binBoundaries() )
            axis1 = AxisWithBins( QuantityValueList( Ee, vs ) )
            self.assertEqual( axis, axis1 )
            return
        

        def test___ne__(self):
            "AxisWithBins: a != b"
            axis = self.axis
            import copy
            vs = copy.deepcopy( axis.binBoundaries() )
            axis1 = AxisWithBins( QuantityValueList( Ee, vs ) )
            self.assertEqual( axis != axis1, False)
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
