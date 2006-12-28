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


## Class that represents a physical quantity

class PhysicalQuantity:

    def __init__(self, value, type):
        self.value = value
        self.type = type
        return
    

    def __eq__(self, rhs):
        try: self.type.checkCompatibility( rhs.type )
        except: return False
        return rhs.value*rhs.type.unit == self.value*self.type.unit


    def __ne__(self, rhs):
        try: self.type.checkCompatibility( rhs.type )
        except: return True
        return rhs.value*rhs.type.unit != self.value*self.type.unit


    def __iadd__(self, rhs):
        if not isPhysicalQuantity( rhs ): raise ValueError, \
           "%s is not a physical quantity" % rhs
        self.type.checkCompatibility( rhs.type )
        self.value += getValue(self.type, rhs)
        return self
    

    def __isub__(self, rhs):
        if not isPhysicalQuantity( rhs ): raise ValueError, \
           "%s is not a physical quantity" % rhs
        self.type.checkCompatibility( rhs.type )
        self.value -= getValue(self.type, rhs)
        return self
    

    def __str__(self):
        return "%s = %s" % (self.type, self.value)

    pass # end of PhysicalQuantity


from PhysicalQuantityType import PhysicalQuantityType

def newType( name, unit ): return PhysicalQuantityType( name, unit )

def new( type, value ): return PhysicalQuantity( value, type )


def getValue(mytype, physical_quantity):
    physical_quantity.type.checkCompatibility( mytype )
    value = physical_quantity.value * physical_quantity.type.unit/mytype.unit
    return value


def conversion_constant( type1, type2 ):
    """factor to convert value in type1 to value in type2

    v1 * unit1 = v2 * unit2
    v2 = v1 * unit1/unit2
    """
    type1.checkCompatibility( type2 )
    return type1.unit/type2.unit


# version
__id__ = "$Id$"

# End of file 
