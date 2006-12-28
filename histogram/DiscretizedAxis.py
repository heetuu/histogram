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


## Discretized axis for physical quantity that is continuous
## Although its implementation is very similar to GenuineDiscreteAxis,
## they are different in that we can do interpolation for data on
## discretized axis to values that are in between the points.

class DiscretizedAxis(AbstractDiscreteAxis):

    def __init__(self, physical_quantity_type, values):
        AbstractDiscreteAxis.__init__(self, physical_quantity_type)
        self._values = values
        return


    def values(self): return self._values


    def __getitem__(self, s):
        if not isSlicingInfo(s): raise NotImplementedError , \
           "cannot get slice (%s)" % s
        s = self.slicingInfo2IndexSlice( s )
        newValues = self._values[s]
        return DiscretizedAxis( self._physical_quantity_type, newValues )


    def _index(self, value):
        if value in self._values: return self._values.index( value )
        else: raise IndexError , "unable to find index for %s" % value


    pass # end of DiscretizedAxis
    

from SlicingInfo import isSlicingInfo


def test():
    from PhysicalQuantity import newType, new
    from pyre.units.energy import eV
    Ee = newType( "electron energy", eV )

    from AbstractDiscreteAxis import TestCase as TC

    class TestCase(TC):

        def setUp(self):
            self.axis = DiscretizedAxis( Ee, [-5.0, -4.0, -3.0] )
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


        def test___eq__(self):
            "DiscretizedAxis: a == b"
            axis = self.axis
            import copy
            vs = copy.deepcopy( axis.values() )
            axis1 = DiscretizedAxis( Ee, vs )
            self.assertEqual( axis, axis1 )
            return
        

        def test___ne__(self):
            "DiscretizedAxis: a != b"
            axis = self.axis
            import copy
            vs = copy.deepcopy( axis.values() )
            axis1 = DiscretizedAxis( Ee, vs )
            self.assertEqual( axis != axis1, False)

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
