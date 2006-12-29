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


class Histogram:

    def __init__(self, name, data, errors, meta = None):
        self._check_data_and_errors(data, errors)
        self._data = data
        self._errors = errors
        if meta is None:
            from AttributeDictionary import AttributeDictionary
            meta = AttributeDictionary( )
            pass
        self._meta = meta
        self._name = name
        return


    def name(self): return self._name


    def dimension(self): return len(self._data.shape())


    def copy(self): return Histogram( self._name, self._data.copy(), self._errors.copy(),
                                      copy.deepcopy(self._meta) )


    def data(self): return self._data
    def errors(self): return self._errors
    def shape(self): return self._data.shape()
    def size(self): return reduce(operator.mul, self.shape())

    def getz(self, *args): return self._data.getz(*args), self._errors.getz(*args)
    def setz(self, *args):
        xs = list(args[:-1])
        z, zerr = args[-1]
        self._data.setz(*(xs+[z]))
        self._errors.setz(*(xs+[zerr]))
        return

    def getSubHist(self, *ranges, **kwds):
        return Histogram( self._name, self._data.getSubGrid(*ranges, **kwds),
                          self._errors.getSubGrid(*ranges, **kwds) )


    def setSubHist(self,*args):
        ranges = list(args[:-1])
        rhs = args[-1]
        rhsdata = rhs._data; rhserrors = rhs._errors
        self._data.setSubGrid( *(ranges+[rhsdata]) )
        self._errors.setSubGrid( *(ranges+[rhserrors]) )
        return
    

    def _check_data_and_errors(self, data, errors):
        from DataOnCells import isDataOnCells
        if not isDataOnCells(data): raise "data must be an instance of DataOnCells"
        if not isDataOnCells(errors): raise "errors must be an instance of DataOnCells"
        
        for axis1, axis2 in zip(data.axes(), errors.axes()):
            if axis1 != axis2: raise ValueError , \
               "data and error does not have save axis: %s and %s" % (
                axis1, axis2)
            continue
        try:
            data.zs().quantity.unit **2 + errors.zs().quantity.unit
        except:
            raise ValueError, "units of data and errors do not match: %s,%s"%(
                data.zs().quantity.unit, errors.zs().quantity.unit)
        return

    pass # end of Histogram


import copy
from DataOnCells import DataOnCells



#test case
import unittest as ut

class TestCase(ut.TestCase):

    from pyre.units.SI import dimensionless
    
    def setUp(self):
        axes = self.createAxes()

        #phys quant "counts"
        from PhysicalQuantity import PhysicalQuantity
        from pyre.units.unit import dimensionless
        self.Counts = PhysicalQuantity( "counts", dimensionless )
        
        self.data = self.createData(axes)
        self.errors = self.createErrors(axes)

        self.histogram = Histogram( "a histogram", self.data, self.errors )
        return


    def createAxes(self):
        from GenuineDiscreteAxis import createGenuineDiscreteAxis
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
        from PhysicalValueNdArray import PhysicalValueNdArray
        from PhysicalQuantityValueNdArray import PhysicalQuantityValueNdArray
        
        numbers = NdArray( 'double', range(100) )
        numbers.setShape( (10,10) )
        pvl = PhysicalValueNdArray( self.dimensionless, numbers )

        return PhysicalQuantityValueNdArray( self.Counts, pvl)


    def createZerrors(self):
        from ndarray.NumpyNdArray import NdArray
        from PhysicalValueNdArray import PhysicalValueNdArray
        from PhysicalQuantityValueNdArray import PhysicalQuantityValueNdArray

        numbers = NdArray( 'double', [1]*100 )
        numbers.setShape( (10,10) )
        
        pvl = PhysicalValueNdArray( self.dimensionless, numbers )

        return PhysicalQuantityValueNdArray( self.Counts, pvl)


    def createData(self, axes):
        return DataOnCells( "data", axes, self.createZs() )
        

    def createErrors(self, axes):
        return DataOnCells( "errors", axes, self.createZerrors() )


    def test_name(self):
        "Histogram: name"
        hist = self.histogram
        self.assertEqual( hist.name(), "a histogram" )
        return


    def test_data(self):
        "Histogram: data"
        hist = self.histogram
        data = hist.data()
        return


    def test_errors(self):
        "Histogram: errors"
        hist = self.histogram
        errors = hist.errors()
        return


    def test_shape(self):
        "Histogram: shape"
        hist = self.histogram
        shape = hist.shape()
        self.assertEqual( len(shape), 2 )
        self.assertEqual( shape[0], 10 )
        self.assertEqual( shape[1], 10 )
        return


    def test_dimension(self):
        "Histogram: dimension"
        hist = self.histogram
        self.assertEqual( hist.dimension(), 2 )
        return


##     def test_axes(self):
##         "Histogram: axes"
##         hist = self.histogram
##         axes = hist.axes()
##         self.assertEqual( len(axes), 2 )
##         return


    def test_getz(self):
        "Histogram: getz( x, y )"
        hist = self.histogram
        z, zerr = hist.getz( 3, 4 )
        self.assertEqual( z, 34.*self.dimensionless )
        self.assertEqual( zerr, 1.*self.dimensionless )
        return


    def test_setz(self):
        "Histogram: setz( x, y, newz )"
        hist = self.histogram.copy()
        hist.setz( 3, 4, (100.*self.dimensionless, 100.*self.dimensionless ) )
        z, zerr = hist.getz( 3, 4 )
        self.assertEqual( z, 100.*self.dimensionless )
        self.assertEqual( zerr, 100.*self.dimensionless )
        return


    def test_getSubHist1(self):
        "Histogram: getSubHist( range, value )"
        from Range import Range
        
        hist = self.histogram
        subhist = hist.getSubHist( Range(3,7), 4 )
        
        z, zerr = subhist.getz(5)
        self.assertEqual( z,  54.*self.dimensionless )
        self.assertEqual( zerr,  1.*self.dimensionless )
        
        newShape = subhist.shape()
        self.assertEqual( len(newShape), 1 )
        self.assertEqual( newShape[0], 5 )
        return


    def test_getSubHist2(self):
        "Histogram: getSubHist( range, range )"
        from Range import Range
        
        hist = self.histogram

        subhist = hist.getSubHist( Range(3,7), Range(2,8) )
        z, zerr = subhist.getz(5,4)
        
        self.assertEqual( z,  54.*self.dimensionless )
        self.assertEqual( zerr,  1.*self.dimensionless )
        
        newShape = subhist.shape()
        self.assertEqual( len(newShape), 2 )
        self.assertEqual( newShape[0], 5 )
        self.assertEqual( newShape[1], 7 )
        return


    def test_setSubHist1(self):
        "Histogram: setSubHist( range, value, newHist )"
        from Range import Range
        
        hist = self.histogram.copy()

        from ndarray.NumpyNdArray import NdArray
        from PhysicalValueNdArray import PhysicalValueNdArray
        from PhysicalQuantityValueNdArray import PhysicalQuantityValueNdArray
        
        newNumbers = NdArray( 'double', range(5) )
        pvl = PhysicalValueNdArray( self.dimensionless, newNumbers )
        newZs = PhysicalQuantityValueNdArray( self.Counts, pvl)

        newNumbers = NdArray( 'double', [10,10,10,10,10] )
        pvl = PhysicalValueNdArray( self.dimensionless, newNumbers )
        newZerrors = PhysicalQuantityValueNdArray( self.Counts, pvl)

        detAxis1 = self.detAxis[ Range(3,7) ]
        newdata = DataOnCells( "data", [detAxis1], newZs )
        newerrors = DataOnCells( "errors", [detAxis1], newZerrors )

        rhs = Histogram( "c_det", newdata, newerrors )
        
        hist.setSubHist( Range(3,7), 4, rhs )

        z, zerr = hist.getz( 5,4 )
        self.assertEqual( z, 2.*self.dimensionless)
        self.assertEqual( zerr, 10.*self.dimensionless)
        return


    def test_setSubHist2(self):
        "Histogram: setSubHist( range, range, newHist )"
        from Range import Range
        
        hist = self.histogram.copy()

        from ndarray.NumpyNdArray import NdArray
        from PhysicalValueNdArray import PhysicalValueNdArray
        from PhysicalQuantityValueNdArray import PhysicalQuantityValueNdArray

        newNumbers = NdArray( 'double', range(5*7) )
        newNumbers.setShape( (5,7) )
        pvl = PhysicalValueNdArray( self.dimensionless, newNumbers )
        newZs = PhysicalQuantityValueNdArray( self.Counts, pvl)

        newNumbers = NdArray( 'double', [10]*(5*7) )
        newNumbers.setShape( (5,7) )
        pvl = PhysicalValueNdArray( self.dimensionless, newNumbers )
        newZerrors = PhysicalQuantityValueNdArray( self.Counts, pvl)

        detAxis1  = self.detAxis[ Range(3,7) ]
        pixAxis1  = self.pixAxis[ Range(2,8) ]
        newdata = DataOnCells( "data", [detAxis1, pixAxis1], newZs)
        newerrors = DataOnCells( "errors", [detAxis1, pixAxis1], newZerrors)
        rhs = Histogram( "c_detpix", newdata, newerrors)

        hist.setSubHist( Range(3,7), Range(2,8), rhs )
        z, zerr = hist.getz( 5,4 )
        self.assertEqual(z, 16.*self.dimensionless )
        self.assertEqual(zerr, 10.*self.dimensionless )
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

