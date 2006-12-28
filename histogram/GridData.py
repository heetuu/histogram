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

    def __init__(self, name, axes, physical_quantity_type, data, meta = None):
        """ctor
        
        name: name of this griddata (or mapping, for subclass
        axes: a list of axes
        physical_quantity_type, data: physical quantity that 'data' represents,
          and data itself
        meta: meta data
        """
        
        #constructor of its subclass must have this same form
        #should create a unit test case
        self._name = name
        self._addAxes(axes)
        self._physical_quantity_type = physical_quantity_type
        self._data = data
        if meta is None: meta = AttributeDictionary()
        self._meta = meta
        return


    def name(self): return self._name


    def rename(self, name): self._name = name


    def storage(self): return self._data


    def shape(self): return self._data.shape()


    def dimension(self): return len(self.shape())


    def axes(self): return self._axes


    def data_pqt(self):
        """physical quantity type of data"""
        return self._physical_quantity_type


     #operators
    def __iadd__(self, other):
        if other is None: return self
        stor = self.storage()
        if isPhysicalQuantity(other):
            other = getValue( self._physical_quantity_type, other )
            stor += other
        elif isCompatibleGridData(self, other):
            stor += other.storage() * conversion_constant( other.data_pqt(), self.data_pqt() )
        else:
            raise NotImplementedError , "%s + %s" % (
                self.__class__.__name__, other.__class__.__name__)
        return self


    def __isub__(self, other):
        if other is None: return self
        stor = self.storage()
        if isPhysicalQuantity(other):
            other = getValue( self._physical_quantity_type, other )
            stor -= other
        elif isCompatibleGridData(self, other):
            stor -= other.storage() * conversion_constant( other.data_pqt(), self.data_pqt() )
        else:
            raise NotImplementedError , "%s - %s" % (
                self.__class__.__name__, other.__class__.__name__)
        return self


    def __imul__(self, other):
        stor = self.storage()
        if isNumber(other): stor *= other
        else:
            raise NotImplementedError , "%s * %s" % (
                self.__class__.__name__, other.__class__.__name__)
        return self
    

    def __idiv__(self, other):
        stor = self.storage()
        if isNumber(other): stor /= other
        else:
            raise NotImplementedError , "%s * %s" % (
                self.__class__.__name__, other.__class__.__name__)
        return self


    def __getitem__(self, s):
        """Slicing
        h[ SlicingInfo( (3.0,4.0) ), all ]
        h[ 3.0, all ]
        h[ all, all ]
        h[ SlicingInfo( (front, 4.0) ), SlicingInfo( (999., back) ) ]
        """
        #if isinstance(s, list): s = tuple(s) # expect tuple
        # force s to be a tuple in case of 1D
        if self.dimension() == 1:
            if isSlicingInfo(s): s = (s,)
            if isPhysicalQuantity(s): s = (s,) 
        
        if not (isinstance(s, tuple) and len(s) == self.dimension()):
            raise NotImplementedError , "GridData[ %s ]. my dimension: %s" % (
                s, self.dimension())

        slicingInfos = s
        axes = self.axes()
        noslice, newAxes, indexSlices = getAxisSlicesAndIndexSlices( axes, slicingInfos )

        if noslice: return newPQ( self.data_pqt(), self._data[ indexSlices ] )
            
        newData = self._data[ indexSlices ]
            
        newMeta = self._meta.copy()
        for newAxis, oldAxis in zip(newAxes, axes):
            if not isAxis( newAxis ): # value
                newMeta.set( str(oldAxis.physical_quantity_type()),  newAxis)
                del newAxes[ newAxes.index( newAxis ) ]
                pass
            continue

        name = "slice %s of %s" % (s, self.name())

        pqt = self._physical_quantity_type
        new = self.__class__( name, newAxes, pqt, newData, newMeta )
        return new
            


    def __setitem__(self, s, rhs):
        #if isinstance(s, list): s = tuple(s) # expect tuple
        # force s to be a tuple in case of 1D
        if self.dimension() == 1:
            if isSlicingInfo(s): s = (s,)
            if isPhysicalQuantity(s): s = (s,) 

        if not (isinstance(s, tuple) and len(s) == self.dimension()):
            raise NotImplementedError , "Histogram[ %s ]. my dimension: %s" % (
                s, self.dimension())
        slicingInfos = s
        
        axes = self.axes()
        noslice, newAxes, indexSlices = getAxisSlicesAndIndexSlices( axes, slicingInfos )

        if noslice :
            if not isPhysicalQuantity(rhs): raise ValueError, \
               "%s is not a physical quantity" % rhs
            self._data[ indexSlices ] = getValue( self.data_pqt(), rhs )
            return rhs

        if not isGridData(rhs): raise ValueError, \
           "rhs of setslice must be either a physical quantity or a GridData instance"
        checkAxesCompatibility( rhs.axes(), newAxes )
        self._data[indexSlices] = rhs.storage() \
                                  * conversion_constant(rhs.data_pqt(), \
                                                        self.data_pqt() )
        return self[ s ]
            


    def copy(self):
        axes = self.axes()
        meta = self._meta.copy()
        storage = self.storage().copy()
        pqt = self._physical_quantity_type
        
        copy = self.__class__(
            self.name(), axes, pqt, storage, meta )
        return copy
    

    def _addAxes(self, axes):
        for axis in axes: self._verifyAxisType(axis)
        self._axes = axes
        return


    def _verifyAxisType(self, axis):
        if axis.__class__ in self.allowed_axis_types: return
        raise TypeError , "Wrong axis type %s" % axis.__class__

    pass



#helpers

from SlicingInfo import isSlicingInfo
from Axes import getAxisSlicesAndIndexSlices, checkAxesCompatibility

def isNumber(a):
    return isinstance(a, int) or isinstance(a, float)


from AbstractDiscreteAxis import AbstractDiscreteAxis

def isAxis(a):
    return isinstance(a, AbstractDiscreteAxis)


from PhysicalQuantity import PhysicalQuantity, newType, getValue,\
     conversion_constant, new as newPQ
def isPhysicalQuantity( pq ):
    return isinstance( pq, PhysicalQuantity )


def isCompatibleGridData( gd1, gd2 ):
    if gd1.shape() != gd2.shape(): return False
    try: checkAxesCompatibility( gd1.axes(), gd2.axes() )
    except: return False
    gd1.data_pqt().checkCompatibility( gd2.data_pqt() ) 
    return True



def isGridData(gd): return isinstance(gd, GridData)


from ndarray.NdArray import NdArray
def isStorage(s): return isinstance(s, NdArray)



#test case
import unittest as ut

class TestCase(ut.TestCase):

    def setUp(self):
        # overload the following to test a special subclass of GridData
        self.GridData = GridData
        axes = self.createAxes()
        from PhysicalQuantity import newType
        from pyre.units.unit import dimensionless
        self.Counts = newType( "counts", dimensionless )
        self.griddata = self.createGridData(axes)
        self.griddata2 = self.createGridData2(axes)
        return


    def createAxes(self):
        from GenuineDiscreteAxis import GenuineDiscreteAxis
        from PhysicalQuantity import newType
        from pyre.units.unit import dimensionless
        
        DetID = newType( "detector ID", dimensionless )
        detAxis = GenuineDiscreteAxis( DetID, range(10) )

        PixID = newType( "pixel ID", dimensionless )
        pixAxis = GenuineDiscreteAxis( PixID, range(10) )

        self.DetID = DetID
        self.PixID = PixID
        
        axes = [detAxis, pixAxis]
        self.detAxis = detAxis; self.pixAxis = pixAxis
        return axes


    def createGridData(self, axes):
        #overload this method to create special griddata instance
        #name must be "name"
        from ndarray.NumpyNdArray import NdArray
        data = NdArray( 'double', range(100) )
        data.setShape( (10,10) )

        return self.GridData( "name", axes, self.Counts, data )


    def createGridData2(self, axes):
        #overload this method to create special griddata instance
        #name must be "gd2"
        from ndarray.NumpyNdArray import NdArray
        data = NdArray( 'double', range(100) )
        data[:] = 0.
        data.setShape( (10,10) )
        return self.GridData( "gd2", axes, self.Counts, data )


    def test_ctor(self):
        "GridData: ctor"
        gd = self.griddata
        axes = gd.axes()
        data = gd.storage()

        from AttributeDictionary import AttributeDictionary
        meta = AttributeDictionary( )
        self.GridData( "name", axes, data, meta )
        return


    def test_name(self):
        "GridData: name, and rename"
        gd = self.griddata
        gd.rename( "name1" )
        self.assertEqual( gd.name(), "name1" )
        gd.rename( "name" )
        self.assertEqual( gd.name(), "name" )
        return


    def test_storage(self):
        "GridData: storage"
        gd = self.griddata
        data = gd.storage()
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


    def test__iadd1__(self):
        "GridData: gd+=<physical quantity>"
        from PhysicalQuantity import new
        
        gd = self.griddata.copy()
        DetID = self.DetID; PixID = self.PixID; Counts = self.Counts
        
        gd += new( self.Counts, 10 )
        
        for i in range(10):
            for j in range(10):
                self.assertEqual( gd[new(DetID, i), new(PixID, j)], new(Counts, 10.+10*i+j) )
        return
    
    
    def test__iadd2__(self):
        "GridData: gd+=gd2"
        from PhysicalQuantity import new
        
        gd = self.griddata.copy()
        gd2 = self.griddata2.copy()

        DetID = self.DetID; PixID = self.PixID; Counts = self.Counts
        gd2[new(DetID,3), new(PixID, 4)] = new(Counts, 10.)

        gd += gd2
        self.assertEqual( gd[new(DetID, 3), new(PixID, 4)], new(Counts, 44.) )
        self.assertEqual( gd[new(DetID, 5), new(PixID, 6)], new(Counts, 56.) )
        return
    
    
    def test__iadd__setitem__(self):
        "GridData: gd[ ? ]+=<physical quantity>"
        from PhysicalQuantity import new
        
        gd = self.griddata.copy()
        DetID = self.DetID; PixID = self.PixID; Counts = self.Counts
        self.assertEqual( gd[new(DetID, 3), new(PixID, 4)], new(Counts, 34.) )
        gd[new(DetID, 3), new(PixID, 4)] += new(Counts, 10. )
        self.assertEqual( gd[new(DetID, 3), new(PixID, 4)], new(Counts, 44.) )
        return
    
    
    def test__isub1__(self):
        "GridData: gd-=<physical quantity>"
        from PhysicalQuantity import new
        
        gd = self.griddata.copy()
        DetID = self.DetID; PixID = self.PixID; Counts = self.Counts
        gd -= new(Counts, 10)
        self.assertEqual( gd[new(DetID, 3), new(PixID, 4)], new(Counts, 24.) )
        return
    
    
    def test__isub2__(self):
        "GridData: gd-=gd2"
        from PhysicalQuantity import new
        
        gd = self.griddata.copy()
        gd2 = self.griddata2.copy()

        DetID = self.DetID; PixID = self.PixID; Counts = self.Counts
        gd2[new(DetID,3), new(PixID, 4)] = new(Counts, 10.)

        gd -= gd2
        self.assertEqual( gd[new(DetID, 3), new(PixID, 4)], new(Counts, 24.) )
        self.assertEqual( gd[new(DetID, 5), new(PixID, 6)], new(Counts, 56.) )
        return
    
    
    def test__imul__(self):
        "GridData: gd*=<number>"
        from PhysicalQuantity import new
        
        gd = self.griddata.copy()
        gd *= 2.
        DetID = self.DetID; PixID = self.PixID; Counts = self.Counts
        self.assertEqual( gd[new(DetID,3), new(PixID, 4)], new(Counts, 68.) )
        return
    
    
    def test__idiv__(self):
        "GridData: gd/=<number>"
        from PhysicalQuantity import new
        
        gd = self.griddata.copy()
        gd /= 2.
        DetID = self.DetID; PixID = self.PixID; Counts = self.Counts
        self.assertEqual( gd[new(DetID,3), new(PixID, 4)], new(Counts, 17.) )
        return


    def test__getitem__1(self):
        "GridData: gd[ phys_quant1, phys_quant2 ]"
        from PhysicalQuantity import new
        
        gd = self.griddata
        DetID = self.DetID; PixID = self.PixID; Counts = self.Counts

        self.assertEqual( gd[new(DetID, 3), new(PixID, 4)], new(Counts, 34.) )
        return


    def test__getitem__2(self):
        "GridData: gd[ slicing, phys_quant2 ]"
        from PhysicalQuantity import new
        from SlicingInfo import SlicingInfo
        
        gd = self.griddata
        DetID = self.DetID; PixID = self.PixID; Counts = self.Counts
        
        detID_slice = SlicingInfo( new(DetID, 3), new(DetID, 7) )
        pixID = new(PixID, 4)

        gds = gd[ detID_slice, pixID ]
        
        self.assertEqual( gds[new(DetID, 5)], new(Counts, 54.) )
        newShape = gds.shape()
        self.assertEqual( len(newShape), 1 )
        self.assertEqual( newShape[0], 5 )
        return


    def test__getitem__3(self):
        "GridData: gd[ slicing, slicing ]"
        from PhysicalQuantity import new
        from SlicingInfo import SlicingInfo
        
        gd = self.griddata
        DetID = self.DetID; PixID = self.PixID; Counts = self.Counts
        
        detID_slice = SlicingInfo( new(DetID, 3), new(DetID, 7) )
        pixID_slice = SlicingInfo( new(PixID, 2), new(PixID, 8) )

        gds = gd[ detID_slice, pixID_slice ]
        
        self.assertEqual( gds[new(DetID, 5), new(PixID, 4)], new(Counts, 54.) )
        newShape = gds.shape()
        self.assertEqual( len(newShape), 2 )
        self.assertEqual( newShape[0], 5 )
        self.assertEqual( newShape[1], 7 )
        return


    def test__setitem__1(self):
        "GridData: gd[ phys_quant1, phys_quant2 ] = value"
        from PhysicalQuantity import new
        
        gd = self.griddata.copy()
        DetID = self.DetID; PixID = self.PixID; Counts = self.Counts
        detID = new(DetID, 3); pixID = new(PixID, 4)

        gd[detID, pixID] = counts = new( Counts, 999 )
        self.assertEqual( gd[detID, pixID], counts )
        return


    def test__setitem__2(self):
        "GridData: gd[ slicing, phys_quant2 ] = another grid data"
        from PhysicalQuantity import new
        from SlicingInfo import SlicingInfo
        
        gd = self.griddata.copy()
        DetID = self.DetID; PixID = self.PixID; Counts = self.Counts
        
        detID_slice = SlicingInfo( new(DetID, 3), new(DetID, 7) )
        pixID = new(PixID, 4)

        from ndarray.NumpyNdArray import NdArray
        newValues = NdArray( 'double', range(5) )

        detAxis1 = self.detAxis[ detID_slice ]
        rhs = self.GridData( "c_det", [detAxis1], Counts, newValues )
        
        gd[ detID_slice, pixID ] = rhs
        
        self.assertEqual( gd[new(DetID, 5), pixID], new(Counts, 2.) )
        return


    def test__setitem__3(self):
        "GridData: gd[ slicing, slicing ] = NdArray instance"
        from PhysicalQuantity import new
        from SlicingInfo import SlicingInfo
        
        gd = self.griddata.copy()
        DetID = self.DetID; PixID = self.PixID; Counts = self.Counts
        
        detID_slice = SlicingInfo( new(DetID, 3), new(DetID, 7) )
        pixID_slice = SlicingInfo( new(PixID, 2), new(PixID, 8) )

        from ndarray.NumpyNdArray import NdArray
        newValues = NdArray( 'double', range(5*7) )
        newValues.setShape( (5,7) )

        detAxis1  = self.detAxis[ detID_slice ]
        pixAxis1  = self.pixAxis[ pixID_slice ]
        rhs = self.GridData( "c_detpix", [detAxis1, pixAxis1], Counts, newValues )

        gd[ detID_slice, pixID_slice ] = rhs
        
        self.assertEqual( gd[new(DetID, 5), new(PixID, 4)], new(Counts, 16.) )
        return


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
