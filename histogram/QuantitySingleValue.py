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


class QuantitySingleValue:

    def __init__(self, quantity, value):
        if not isQuantity(quantity):
            raise ValueError, "%s is not a quantity"% quantity

        checkValue( value, quantity )
        self.quantity = quantity
        return

    pass # end of QuantitySingleValue


from AbstractQuantity import isQuantity, checkValue

# version
__id__ = "$Id$"

# End of file 
