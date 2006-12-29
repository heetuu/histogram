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


from AbstractDiscreteAxis import AbstractDiscreteAxis

class GenuineDiscreteAxis(AbstractDiscreteAxis):

    def __init__(self, quantityValueList):
        AbstractDiscreteAxis.__init__(self, quantityValueList)
        return
    

    def __getitem__(self, s):
        if not isSlicingInfo(s): raise NotImplementedError , \
           "cannot get slice (%s) of axis (%s)" % (s, self)
        s = self.slicingInfo2IndexSlice( s )
        newValues = self.values()[s]
        return GenuineDiscreteAxis( QuantityValueList( self._quantity, newValues ) )

    pass # end of GenuineDiscreteAxis


from SlicingInfo import isSlicingInfo
from QuantityValueList import QuantityValueList
    

def test():
    from pyre.units.energy import eV
    from PhysicalQuantity import PhysicalQuantity
    from PhysicalValueList import PhysicalValueList
    
    Eb = PhysicalQuantity( "bound state electron energy", eV )

    from AbstractDiscreteAxis import TestCase as TC

    class TestCase(TC):

        def setUp(self):
            energyValueList = PhysicalValueList( eV,  [-8., -7., -6., -5.0, -4.0, -3.0] )
            EbValueList = QuantityValueList( Eb, energyValueList )
            self.axis = GenuineDiscreteAxis( EbValueList )
            return


        def test_values(self):
            "GenuineDiscreteAxis: values"
            TC.test_values(self)
            return


        def test_index(self):
            "GenuineDiscreteAxis: index"
            axis = self.axis
            self.assertEqual( axis.index( -5.0*eV ), 3 )
            self.assertEqual( axis.index( -4.0*eV ), 4 )
            self.assertRaises( ValueError, axis.index, -2.0*eV )
            return


        def test___eq__(self):
            "GenuineDiscreteAxis: a == b"
            axis = self.axis
            import copy
            vs = copy.deepcopy( axis.values() )
            axis1 = GenuineDiscreteAxis( QuantityValueList( Eb, vs ) )
            self.assertEqual( axis, axis1 )
            return
        

        def test___ne__(self):
            "GenuineDiscreteAxis: a != b"
            axis = self.axis
            import copy
            vs = copy.deepcopy( axis.values() )
            axis1 = GenuineDiscreteAxis( QuantityValueList( Eb, vs ) )
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
