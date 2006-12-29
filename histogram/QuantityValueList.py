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


class QuantityValueList:

    def __init__(self, quantity, valuelist):
        if not isQuantity(quantity):
            raise ValueError, "%s is not a quantity"% quantity
        self.quantity = quantity
        
        self.checkValueList( valuelist )
        self.values = valuelist
        return


    def checkValueList(self, valueList):
        for value in valueList: checkValue( value, self.quantity )
        return


    def __len__(self): return len(self.values)


    def __getitem__(self, s):
        if not isinstance(s, slice):
            raise NotImplementedError, "QuantityValueList[ %s ]" % s
        rt = self.values[s]
        return QuantityValueList(self.quantity, rt)


    def __eq__(self, rhs):
        if not isQuantityValueList( rhs ): return False
        if self.quantity != rhs.quantity: return False
        if len(self) != len(rhs): return False
        for v1,v2 in zip(self.values, rhs.values):
            if v1 != v2: return False
            continue
        return True


    def __ne__(self, rhs):
        return not (self == rhs)

    pass # end of QuantityValueList


from AbstractQuantity import isQuantity, checkValue


def isQuantityValueList( candidate ): return isinstance( candidate, QuantityValueList )


import unittest as ut

class TestCase(ut.TestCase):

    def setUp(self):
        # overload this to test a special subclass of QuantityValueList
        # quantity + valuelist --> qvlist
        # qvlist2 == qvlist
        # for qvl in different_qvlists: qvl != qvlist
        self.quantity = None
        self.valuelist = None
        self.qvlist = None
        self.qvlist2 = None
        self.different_qvlists = None        
        return


    def test_checkValueList(self):
        "QuantityValueList: checkValueList"
        self.qvlist.checkValueList( self.valuelist )
        return


    def test___getitem__(self):
        "QuantityValueList: qvl[ slice ]"
        sl = self.qvlist[ 1:5]
        self.assertEqual( sl.__class__, QuantityValueList )
        return


    def test___eq__(self):
        "QuantityValueList: a == b"
        self.assertEqual( self.qvlist, self.qvlist2 )
        return


    def test___ne__(self):
        "QuantityValueList: a != b"
        for qvl in self.different_qvlists:
            self.assertNotEqual( self.qvlist, qvl )
        return

    pass



def test():
    #requires ID
    from ID import ID

    class TestCase1(TestCase):

        def setUp(self):
            self.quantity = q = ID( "detector" )
            qd = ID('pixel')
            assert qd != q

            self.valuelist = vl = range(10)
            vld = range( 10, 20 )
            assert vl != vld
            
            self.qvlist = QuantityValueList( q, vl )
            self.qvlist2 = QuantityValueList( q, vl )
            self.different_qvlists = [
                QuantityValueList( q, vld ),
                QuantityValueList( qd, vl ),
                QuantityValueList( qd, vld ),
                ]
            return

        pass

    import unittest as ut
    suite = ut.makeSuite( TestCase1 )
    alltests = ut.TestSuite( (suite, ) )
    ut.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == "__main__": test()



# version
__id__ = "$Id$"

# End of file 
