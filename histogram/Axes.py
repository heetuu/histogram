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



def getAxisSlicesAndIndexSlices( axes, ranges ):
    """getAxisSlicesAndIndexSlices( axes, ranges ) --> noslice, newAxes, indexSlices

    obtain new axes (slices of original axes) and index slices

    axes: a list of axes
    ranges: a list. each element is either a range instance,
      or a single value. 

    newAxes: a list of new axis. each axis is either a slice of original axis,
      or a single value.
    indexSlices: a list. each element is either a index slice corresponding to
      the range, or a single index if range is actually just a value
    noslice:  whether range is actually a list of only single values
    """
    indexSlices = []; noslice = True
    
    newAxes = []
    
    for range, axis in zip(ranges, axes):
        
        if not isRange( range ):
            # if it is not a range instance, it must be a value indexable
            # in this axis.
            
            value = range
            s = axis.index( value )

            newAxes.append( value )
        else:
            s = axis.range2IndexSlice( range )
            if noslice: noslice = False
            newAxes.append( axis[ range ] )
            pass
        
        indexSlices.append( s )
        continue
    
    return noslice, newAxes, indexSlices


def checkAxesCompatibility( axes1, axes2 ):
    for axis1, axis2 in zip(axes1, axes2):
        if axis1 != axis2: raise
        continue
    return


from Range import isRange


# version
__id__ = "$Id$"

# End of file 
