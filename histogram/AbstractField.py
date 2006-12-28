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


from PhysicalQuantity import PhysicalQuantity


## abstract field: \lambda: x,y,z,...  --> f

class AbstractField:

    def __init__(self, dependent_physical_quantity_types, destination_physical_quantity_type):
        self.dep_types = dependent_physical_quantity_types
        self.dest_type = destination_physical_quantity_type
        return


    def __call__(self, *physical_quantities):
        args = []
        for physical_quantity, type in zip(physical_quantities, self.dep_types):
            type.checkCompatibility( physical_quantity.type )
            args.append( physical_quantity.value * physical_quantity.type.unit/type.unit )
            continue
        return PhysicalQuantity( self._eval( *args ), self.dest_type )


    def _eval(self, *args):
        raise NotImplementedError


    pass # end of AbstractField



def test():
    import unittest as ut

    from pyre.units.time import second
    from pyre.units.length import meter


    class 

    class TestCase(ut.TestCase):

        def test1(self):
            "AbstractField"
            t = PhysicalQuantityType( "time",  second)
            l = PhysicalQuantityType( "distance", meter)
            mapt2l = 
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
