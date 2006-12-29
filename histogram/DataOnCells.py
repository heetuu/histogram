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



from GridData import GridData

class DataOnCells(GridData):
    from AxisWithBins import AxisWithBins
    from GenuineDiscreteAxis import GenuineDiscreteAxis
    allowed_axis_types = [AxisWithBins, GenuineDiscreteAxis]
    pass



def isDataOnCells(candidate): return isinstance( candidate, DataOnCells )


# version
__id__ = "$Id$"

# End of file 
