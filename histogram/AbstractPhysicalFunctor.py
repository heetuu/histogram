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


import PhysicalQuantity 


## abstract functor with physics meaning: \lambda: x,y,z,...  --> f

class AbstractPhysicalFunctor:

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
        return PhysicalQuantity.new( self.dest_type, self._eval( *args ) )


    def _eval(self, *args):
        raise NotImplementedError


    pass # end of AbstractPhysicalFunctor



def new( dependent_physical_quantity_types, destination_physical_quantity_type,
         normal_functor ):
    class NewF(AbstractPhysicalFunctor):
        def __init__(self):
            AbstractPhysicalFunctor.__init__(
                self,
                dependent_physical_quantity_types,
                destination_physical_quantity_type)
            return

        def _eval(self, *args): return normal_functor( *args )

        pass

    return NewF()
    


def test():
    import unittest as ut

    from pyre.units.time import second, millisecond
    from pyre.units.length import meter

    time = PhysicalQuantity.newType( "time",  second)
    time2 = PhysicalQuantity.newType( "time",  millisecond)
    dist = PhysicalQuantity.newType( "distance", meter)

    class FreeFallDistance(AbstractPhysicalFunctor):
        
        """free fall
        \lambda: t-->h
        """
        
        def __init__(self):
            AbstractPhysicalFunctor.__init__(self, [time], dist)
            return

        def _eval(self, *args):
            return 9.8/2.0 * (args[0]**2)

        pass
    
    mapt2l = FreeFallDistance()

    def freefall_dist( *args ): return 9.8/2.0 * (args[0]**2)
    mapt2l_ = new( [time], dist, freefall_dist)

    class TestCase(ut.TestCase):

        def test1(self):
            "AbstractPhysicalFunctor"
            t1 = PhysicalQuantity.new(time, 1.0)
            self.assertAlmostEqual( mapt2l( t1 ).value, 4.9 )
            self.assertAlmostEqual( mapt2l_( t1 ).value, 4.9 )
            
            t2 = PhysicalQuantity.new(time2, 1.0)
            self.assertAlmostEqual( mapt2l( t2 ).value, 4.9e-6 )
            self.assertAlmostEqual( mapt2l_( t2 ).value, 4.9e-6 )
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

