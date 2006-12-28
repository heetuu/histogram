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



def getAxisSlicesAndIndexSlices( axes, slicingInfos ):
    """getAxisSlicesAndIndexSlices( axes, slicingInfos ) --> noslice, newAxes, indexSlices

    obtain new axes (slices of original axes) and index slices

    axes: a list of axes
    slicingInfos: a list. each element is either a slicingInfo instance,
      or a single value. 

    newAxes: a list of new axis. each axis is either a slice of original axis,
      or a single value.
    indexSlices: a list. each element is either a index slice corresponding to
      the slicingInfo, or a single index if slicingInfo is actually just a value
    noslice:  whether slicingInfo is actually a list of only single values
    """
    indexSlices = []; noslice = True
    
    newAxes = []
    
    for slicingInfo, axis in zip(slicingInfos, axes):
        
        if not isSlicingInfo( slicingInfo ):
            # if it is not a slicingInfo instance, it must be a value indexable
            # in this axis.
            
            value = slicingInfo
            s = axis.index( value )

            newAxes.append( value )
        else:
            s = axis.slicingInfo2IndexSlice( slicingInfo )
            if noslice: noslice = False
            newAxes.append( axis[ slicingInfo ] )
            pass
        
        indexSlices.append( s )
        continue
    
    return noslice, newAxes, indexSlices


def checkAxesCompatibility( axes1, axes2 ):
    for axis1, axis2 in zip(axes1, axes2):
        if axis1 != axis2: raise
        continue
    return


from SlicingInfo import isSlicingInfo


# version
__id__ = "$Id$"

# End of file 
