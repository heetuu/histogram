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


class PhysicalQuantityValueNdArray:

    def __init__(self, quantity, valueNdArray):
        if not isPhysicalQuantity(quantity):
            raise ValueError, "%s is not a quantity"% quantity
        self.quantity = quantity
        
        self.checkValueNdArray( valueNdArray )
        self.values = valueNdArray
        return


    def checkValueNdArray(self, valueNdArray):
        if not isPhysicalValueNdArray( valueNdArray ):
            raise ValueError, "%s is not a NdArray of physical quantity values" % (
                valueNdArray, )
        checkValue( valueNdArray.unit(), self.quantity )
        return


    def shape(self): return self.values.shape()


    def copy(self): return PhysicalQuantityValueNdArray( self.quantity, self.values.copy() )


    def __getitem__(self, s):
        rt = self.values[s]
        if isPhysicalValueNdArray( rt ):
            return PhysicalQuantityValueNdArray(self.quantity, rt)
        raise NotImplementedError

    pass # end of QuantityValueNdArray


from AbstractQuantity import isQuantity, checkValue
from PhysicalQuantity import PhysicalQuantity, isPhysicalQuantity
from PhysicalValueNdArray import PhysicalValueNdArray

def isQuantityValueNdArray( candidate ): return isinstance( candidate, QuantityValueNdArray )
def isPhysicalValueNdArray( candidate ): return isinstance( candidate, PhysicalValueNdArray )


import unittest as ut

class TestCase(ut.TestCase):

    from pyre.units.SI import dimensionless

    def setUp(self):
        # quantity + physicalValueNdArray --> physicalQuantityValueNdArray
        self.quantity = q = PhysicalQuantity( "counts", self.dimensionless )

        from ndarray.NumpyNdArray import NdArray
        vnd = NdArray( "double", range(100) )
        vnd.setShape( (10,10) )

        self.pvna = PhysicalValueNdArray( self.dimensionless, vnd )

        self.pqvna = PhysicalQuantityValueNdArray( q, self.pvna )
        return


    def test_checkValueNdArray(self):
        "PhysicalQuantityValueNdArray: checkValueNdArray"
        self.pqvna.checkValueNdArray( self.pvna )
        return


    def test___getitem__(self):
        "PhysicalQuantityValueNdArray: pqvna[ slice ]"
        sl = self.pqvna[ 1:5 ]
        self.assertEqual( sl.__class__, PhysicalQuantityValueNdArray )
        return

    pass



def test():
    import unittest as ut
    suite = ut.makeSuite( TestCase )
    alltests = ut.TestSuite( (suite, ) )
    ut.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == "__main__": test()



# version
__id__ = "$Id$"

# End of file 
