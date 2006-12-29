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

## Class that represents a physical quantity

class PhysicalQuantity(AbstractQuantity):

    def __init__(self, name, unit):
        """new physical quantity

        name: name of physical quantity
        unit: unit of physical quantity. instance of pyre.units.unit
        """
        AbstractQuantity.__init__(self, name)
        self.unit = unit
        return
    

    def isAcceptable(self, value):
        "check if the given value is acceptable for this quantity"
        try: value + self.unit
        except: return False
        return True


    def __eq__(self, rhs):
        if not isPhysicalQuantity(rhs): return False
        if self.name != rhs.name: return False
        return self.isAcceptable( rhs.unit )


    def __ne__(self, rhs):
        return not (self==rhs)

    pass # end of PhysicalQuantity


def isPhysicalQuantity( candidate ): return isinstance( candidate, PhysicalQuantity )


# version
__id__ = "$Id$"

# End of file 
