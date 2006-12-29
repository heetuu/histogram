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


from AbstractQuantity import AbstractQuantity


class ID(AbstractQuantity):

    def isAcceptable(self, value):
        "check if the given value is acceptable for this quantity"
        return isinstance(value, int) or isinstance(value, long)


    def __eq__(self, rhs):
        if not isID(rhs): return False
        return self.name == rhs.name


    def __ne__(self, rhs):
        return not (self==rhs)

    pass # end of AbstractQuantity



def isID(candidate): return isinstance( candidate, ID )


def test():
    from AbstractQuantity import TestCase as TC

    class TestCase(TC):

        def setUp(self):
            self.quantity = ID( "detector" )
            self.value = 1
            self.quantity2 = ID( "detector" )
            self.quantity3 = ID( "pixel" )
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
