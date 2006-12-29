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


class AbstractQuantity(object):

    def __init__(self, name):
        self.name = name
        return


    def isAcceptable(self, value):
        "check if the given value is acceptable for this quantity"
        raise NotImplementedError


    def __eq__(self, rhs):
        raise NotImplementedError


    def __ne__(self, rhs):
        raise NotImplementedError

    pass # end of AbstractQuantity


def isQuantity( q ): return isinstance( q, AbstractQuantity )

def checkValue( v, q ):
    if not q.isAcceptable( v ):
        raise ValueError, "%s is not an acceptable value for quantity %s" % (
            v, q)
    return



import unittest as ut

class TestCase(ut.TestCase):

    def setUp(self):
        # overload this to test a special subclass of AbstractQuantity
        # quantity == quantity2
        # quantity != qunatity2
        self.quantity = None
        self.value = None
        self.quantity2 = None
        return


    def test_isAcceptable(self):
        "AbstractQuantity: isAcceptable"
        self.assert_( self.quantity.isAcceptable( self.value) )
        return


    def test___eq__(self):
        "AbstractQuantity: a == b"
        self.assertEqual( self.quantity, self.quantity2 )
        return


    def test___ne__(self):
        "AbstractQuantity: a != b"
        self.assertNotEqual( self.quantity, self.quantity3 )
        return

    pass




# version
__id__ = "$Id$"

# End of file 
