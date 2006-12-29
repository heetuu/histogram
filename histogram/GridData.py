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


from AttributeDictionary import AttributeDictionary
from GenuineDiscreteAxis import GenuineDiscreteAxis


# collection of grid and data

class GridData:

    allowed_axis_types = [GenuineDiscreteAxis] # overload this data

    def __init__(self, name, axes, zs, meta = None):
        """ctor
        
        name: name of this griddata (or mapping, for subclass
        axes: a list of axes
        zs: a PhysicalQuantityValueNdArray instance. z values
            at each point of the grid defined by the axes
        meta: meta data
        """
        
        #constructor of its subclass must have this same form
        #should create a unit test case
        self._name = name
        self._zs = zs
        self._addAxes(axes)
        if meta is None: meta = AttributeDictionary()
        self._meta = meta
        return


    def name(self): return self._name


    def rename(self, name): self._name = name


    def zs(self): return self._zs


    def shape(self): return self._zs.shape()


    def dimension(self): return len(self.shape())


    def axes(self): return self._axes


    def map(self):
        xs = [ axis.quantity for axis in self.axes() ]
        return (xs, self.zs().quantity)


    def getz(self, *args):
        indexes = []
        for arg, axis in zip( args, self.axes() ):
            checkValue( arg, axis.quantity )
            indexes.append( axis.index(arg) )
            continue
        return self._zs.values[ indexes ]


    def setz(self, *args):
        coords = args[:-1]
        new = args[-1]
        indexes = []
        for coord, axis in zip( coords, self.axes() ):
            checkValue( coord, axis.quantity )
            indexes.append( axis.index(coord) )
            continue
        self._zs.values[ indexes ]  = new
        return


    def getSubGrid(self, *ranges, **kwds):
        """Slicing
        gd.getSubGrid( Range( (3.0,4.0) ), all )
        gd( 3.0, all, newName = "newGridData")
        gd( all, all )
        gd( Range( (front, 4.0) ), Range( (999., back) ) )
        """
        if len(ranges) != self.dimension():
            raise NotImplementedError , "GridData[ %s ]. my dimension: %s" % (
                ranges, self.dimension())

        axes = self.axes()
        noslice, newAxes, indexSlices = getAxisSlicesAndIndexSlices( axes, ranges )

        if noslice: raise "%s is not a list of ranges" % (ranges,)
            
        newZs = self._zs[ indexSlices ]
            
        newMeta = self._meta.copy()
        for newAxis, oldAxis in zip(newAxes, axes):
            if not isAxis( newAxis ): # value
                newMeta.set( str(oldAxis.quantity),  newAxis)
                del newAxes[ newAxes.index( newAxis ) ]
                pass
            continue
        newName = kwds.get("newName")
        if newName is None : newName = "%s in ranges (%s)" % (self.name(), ranges)

        new = self.__class__( newName, newAxes, newZs, newMeta )
        return new


    def setSubGrid(self, *args):
        ranges = args[:-1]
        rhs = args[-1]
        if len(ranges) != self.dimension():
            raise NotImplementedError , "GridData[ %s ]. my dimension: %s" % (
                ranges, self.dimension())
        
        axes = self.axes()
        noslice, newAxes, indexSlices = getAxisSlicesAndIndexSlices( axes, ranges )

        if noslice: raise "%s is not a list of ranges" % (ranges,)

        if not isGridData(rhs): raise ValueError, \
           "rhs of setSubGrid must be either a GridData instance"
        checkAxesCompatibility( rhs.axes(), newAxes )
        self._zs.values[indexSlices] = rhs._zs.values
        return
            


    def copy(self):
        axes = self.axes()
        meta = self._meta.copy()
        zs = self.zs().copy()
        
        copy = self.__class__(
            self.name(), axes, zs, meta )
        return copy
    

    def _addAxes(self, axes):
        shape = self._zs.shape()
        for i,axis in enumerate(axes):
            self._verifyAxisType(axis)
            assert len(axis) == shape[i], "axis %s does not match z data" % axis
            continue
        self._axes = axes
        return


    def _verifyAxisType(self, axis):
        if axis.__class__ in self.allowed_axis_types: return
        raise TypeError , "Wrong axis type %s" % axis.__class__

    pass



#helpers

from Range import isRange, Range
from Axes import getAxisSlicesAndIndexSlices, checkAxesCompatibility
from AbstractQuantity import checkValue
from PhysicalQuantity import PhysicalQuantity
from PhysicalValueList import PhysicalValueList
from PhysicalValueNdArray import PhysicalValueNdArray
from PhysicalQuantityValueNdArray import PhysicalQuantityValueNdArray

def isNumber(a):
    return isinstance(a, int) or isinstance(a, float)


from AbstractDiscreteAxis import AbstractDiscreteAxis

def isAxis(a):
    return isinstance(a, AbstractDiscreteAxis)


def isPhysicalQuantity( pq ):
    return isinstance( pq, PhysicalQuantity )


def isCompatibleGridData( gd1, gd2 ):
    if gd1.shape() != gd2.shape(): return False
    try: checkAxesCompatibility( gd1.axes(), gd2.axes() )
    except: return False
    gd1.data_pqt().checkCompatibility( gd2.data_pqt() ) 
    return True



def isGridData(gd): return isinstance(gd, GridData)


#test case
import unittest as ut

class TestCase(ut.TestCase):

    from pyre.units.unit import dimensionless
    
    def setUp(self):
        # overload the following to test a special subclass of GridData
        self.GridData = GridData
        axes = self.createAxes()

        #phys quant "counts"
        from PhysicalQuantity import PhysicalQuantity
        from pyre.units.unit import dimensionless
        self.Counts = PhysicalQuantity( "counts", dimensionless )
        
        self.griddata = self.createGridData(axes)
        self.griddata2 = self.createGridData2(axes)
        return


    def createAxes(self):
        from GenuineDiscreteAxis import createGenuineDiscreteAxis
        from PhysicalQuantity import PhysicalQuantity
        from ID import ID
        
        DetID = ID( "detector ID" )
        detAxis = createGenuineDiscreteAxis( DetID, range(10) )

        PixID = ID( "pixel ID" )
        pixAxis = createGenuineDiscreteAxis( PixID, range(10) )

        self.DetID = DetID
        self.PixID = PixID
        
        axes = [detAxis, pixAxis]
        self.detAxis = detAxis; self.pixAxis = pixAxis
        return axes


    def createZs(self):
        from ndarray.NumpyNdArray import NdArray
        numbers = NdArray( 'double', range(100) )
        numbers.setShape( (10,10) )
        
        pvl = PhysicalValueNdArray( self.dimensionless, numbers )

        return PhysicalQuantityValueNdArray( self.Counts, pvl)


    def createZs2(self):
        from ndarray.NumpyNdArray import NdArray
        numbers = NdArray( 'double', [0]*100 )
        numbers.setShape( (10,10) )
        
        pvl = PhysicalValueNdArray( self.dimensionless, numbers )

        return PhysicalQuantityValueNdArray( self.Counts, pvl)


    def createGridData(self, axes):
        #overload this method to create special griddata instance
        #name must be "name"
        return self.GridData( "name", axes, self.createZs() )
        

    def createGridData2(self, axes):
        #overload this method to create special griddata instance
        #name must be "gd2"
        return self.GridData( "gd2", axes, self.createZs2() )


    def test_ctor(self):
        "GridData: ctor"
        gd = self.griddata
        axes = gd.axes()
        zs = gd.zs()

        from AttributeDictionary import AttributeDictionary
        meta = AttributeDictionary( )
        self.GridData( "name", axes, zs, meta )
        return


    def test_name(self):
        "GridData: name, and rename"
        gd = self.griddata
        gd.rename( "name1" )
        self.assertEqual( gd.name(), "name1" )
        gd.rename( "name" )
        self.assertEqual( gd.name(), "name" )
        return


    def test_zs(self):
        "GridData: zs"
        gd = self.griddata
        data = gd.zs()
        return


    def test_shape(self):
        "GridData: shape"
        gd = self.griddata
        shape = gd.shape()
        self.assertEqual( len(shape), 2 )
        self.assertEqual( shape[0], 10 )
        self.assertEqual( shape[1], 10 )
        return


    def test_dimension(self):
        "GridData: dimension"
        gd = self.griddata
        self.assertEqual( gd.dimension(), 2 )
        return


    def test_axes(self):
        "GridData: axes"
        gd = self.griddata
        axes = gd.axes()
        self.assertEqual( len(axes), 2 )
        return


    def test_getz(self):
        "GridData: getz( x, y )"
        gd = self.griddata
        self.assertEqual( gd.getz( 3, 4 ), 34.*self.dimensionless )
        return


    def test_setz(self):
        "GridData: setz( x, y, newz )"
        gd = self.griddata
        gd.setz( 3, 4, 99.*self.dimensionless )
        self.assertEqual( gd.getz( 3, 4 ), 99.*self.dimensionless )
        return


    def test_getSubGrid1(self):
        "GridData: getSubGrid( range, value )"
        gd = self.griddata

        subgd = gd.getSubGrid( Range(3,7), 4 )
        
        self.assertEqual( subgd.getz(5),  54.*self.dimensionless )
        newShape = subgd.shape()
        self.assertEqual( len(newShape), 1 )
        self.assertEqual( newShape[0], 5 )
        return


    def test_getSubGrid2(self):
        "GridData: getSubGrid( range, range )"
        gd = self.griddata

        subgd = gd.getSubGrid( Range(3,7), Range(2,8) )
        
        self.assertEqual( subgd.getz(5,4),  54.*self.dimensionless )
        newShape = subgd.shape()
        self.assertEqual( len(newShape), 2 )
        self.assertEqual( newShape[0], 5 )
        self.assertEqual( newShape[1], 7 )
        return


    def test_setSubGrid1(self):
        "GridData: setSubGrid( range, value, newGrid )"
        gd = self.griddata.copy()

        from ndarray.NumpyNdArray import NdArray
        newNumbers = NdArray( 'double', range(5) )
        pvl = PhysicalValueNdArray( self.dimensionless, newNumbers )
        newZs = PhysicalQuantityValueNdArray( self.Counts, pvl)

        detAxis1 = self.detAxis[ Range(3,7) ]
        rhs = self.GridData( "c_det", [detAxis1], newZs )
        
        gd.setSubGrid( Range(3,7), 4, rhs )
        
        self.assertEqual( gd.getz( 5,4 ), 2.*self.dimensionless)
        return


##     def test__setitem__3(self):
##         "GridData: gd[ slicing, slicing ] = NdArray instance"
##         from PhysicalQuantity import new
##         from Range import Range
        
##         gd = self.griddata.copy()
##         DetID = self.DetID; PixID = self.PixID; Counts = self.Counts
        
##         detID_slice = Range( new(DetID, 3), new(DetID, 7) )
##         pixID_slice = Range( new(PixID, 2), new(PixID, 8) )

##         from ndarray.NumpyNdArray import NdArray
##         newValues = NdArray( 'double', range(5*7) )
##         newValues.setShape( (5,7) )

##         detAxis1  = self.detAxis[ detID_slice ]
##         pixAxis1  = self.pixAxis[ pixID_slice ]
##         rhs = self.GridData( "c_detpix", [detAxis1, pixAxis1], Counts, newValues )

##         gd[ detID_slice, pixID_slice ] = rhs
        
##         self.assertEqual( gd[new(DetID, 5), new(PixID, 4)], new(Counts, 16.) )
##         return


    pass



def test():
    import unittest as ut
    suite = ut.makeSuite( TestCase )
    alltests = ut.TestSuite( (suite, ) )
    ut.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == "__main__": test()


# version
__id__ = "$Id$"

# End of file 
