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



## Class that represents a physical quantity type


class PhysicalQuantityType:


    def __init__(self, name, unit):
        self.name = name
        self.unit = unit
        return


    def checkCompatibility( self, type2 ):
        if self.name != type2.name : 
            raise IncompatiblePhysicalQuantity( "name mismatch: %s, %s" %
                                                (self.name, type2.name) )
        try: self.unit + type2.unit
        except:
            raise IncompatiblePhysicalQuantity( "unit mismatch: %s, %s" % 
                                                (self.unit, type2.unit) )
        return


    def __str__(self): return "%s (unit: %s)" % (self.name, self.unit)

    pass # end of PhysicalQuantityType




class IncompatiblePhysicalQuantity(Exception): pass
    


def test():
    import unittest as ut

    from pyre.units.energy import meV
    from pyre.units.length import meter

    class TestCase(ut.TestCase):

        def test1(self):
            "testCompatibility"
            t1 = PhysicalQuantityType( "neutron energy", meV )
            t2 = PhysicalQuantityType( "neutron energy", meter )
            self.assertRaises(
                IncompatiblePhysicalQuantity, t1.checkCompatibility, t2)
            return

        pass

    suite = ut.makeSuite( TestCase )
    alltests = ut.TestSuite( (suite, ) )
    ut.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == "__main__": test()

# version
__id__ = "$Id$"

# End of file 
