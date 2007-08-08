#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \namespace ndarray::StdVectorNdArray
##
## This module hosts an implementation of ndarray.NdArray.NdArray using
## std::vector. This package uses the python package
## <a href="../../../stdVector/stdVector/html/">stdVector</a>.
## stdVector c++ implementation is not as fast as numpy arrays when array is big,
## so a StdVectorNdArray.NdArray is casted to an NumpyNdArray.NdArray
## if an array is big.
##


from NdArray import NdArray as NdArrayBase

from stdVector.StdVector import StdVector



def arrayFromVector( v ):
    res = NdArray( v.datatype(), v.size(), handle = v.handle() )
    res.__ref_to_original_vector = v
    return res


class NdArray(StdVector, NdArrayBase):


    def __init__(self, *args, **kwds):
        StdVector.__init__(self, *args, **kwds)
        if self.size() > 1000000: self._big = True
        else: self._big = False
        return


    def __neg__(self):
        return -1. * self


    def __mul__(self, other):
        res = self.copy()
        res *= other
        return res


    __rmul__ = __mul__
    
            
    def __add__(self, other):
        res = self.copy()
        res += other
        return res


    __radd__ = __add__


    def __sub__(self, other):
        if self == other: return NdArray( self.datatype(), self.size(), 0 )
        return self.__add__( -other )


    def __rdiv__(self, other):
        if isNumber(other):
            res = self.__class__( self.datatype(), self.size(), other)
            res.divideEquals( self )
            return res
        raise NotImplementedError , "__rdiv_ is not defined for %s and %s" % (
            self.__class__.__name__, other.__class__.__name__ )


    def __div__(self, other):
        return self * (1./other)
            


    def __iadd__(self, other):
        if self._big: t = self[:]; t+=other; return self
        if isNumber(other): self.addScalar( other ); return self
        if isNdArray(other): self.plusEquals( other ); return self
        raise NotImplementedError , "__iadd__ is not defined for %s and %s" % (
            self.__class__.__name__, other.__class__.__name__ )


    def __isub__(self, other):
        if self._big: t = self[:]; t-=other; return self
        if isNumber(other): self.addScalar( -other ); return self
        if isNdArray(other): self.minusEquals( other ); return self
        raise NotImplementedError , "__isub__ is not defined for %s and %s" % (
            self.__class__.__name__, other.__class__.__name__ )


    def __imul__(self, other):
        if self._big: t = self[:]; t*=other; return self
        if isNumber(other): self.multScalar( other ); return self
        if isNdArray(other): self.timesEquals( other ); return self
        raise NotImplementedError , "__imul__ is not defined for %s and %s" % (
            self.__class__.__name__, other.__class__.__name__ )


    def __idiv__(self, other):
        if self._big: t = self[:]; t/=other; return self
        if isNumber(other): self.multScalar( 1./other ); return self
        if isNdArray(other): self.divideEquals( other ); return self
        raise NotImplementedError , "__idiv__ is not defined for %s and %s" % (
            self.__class__.__name__, other.__class__.__name__ )



    def sum(self, axis = None):
        if axis is None: return StdVector.sum(self, 0, self.size())
        else:
            r = self[:] # convert to NumpyNdArray
            return r.sum( axis= axis )
        raise
    

    def reverse(self):
        na = self.asNumarray()
        na[:] = 1./na
        return 


    def copy(self):
##         res = self.__class__( self.datatype(), self.asList() )
##         res.setShape(self.shape())
##         return res
        from stdVector import copy
        c = copy(self)
        res = arrayFromVector( c )
        res.setShape( self.shape() )
        return res


    def castCopy(self, typename):
        from stdVector import castCopy
        res = self.__class__(typename, self.size(), 0)
        castCopy(self, res)
        res.setShape( self.shape() )
        return res
    

    def shape(self): return self._shape


    def setShape(self, s):  self._shape = s


    def asNumarray(self):
        r = StdVector.asNumarray(self)
        try:
            r.shape = self.shape()
        except:
            raise ValueError , "shape mismatch: %s, %s" % (r.shape, self.shape())
        return r


    def __getitem__(self, s):
        if isinstance(s, list): s = tuple(s)
        
        numarr = self.asNumarray()
        numarr.shape = self.shape()
        try: subelement = numarr[s]
        except IndexError, msg: raise IndexError, "%s -- out of range" % (s,)

        if isinstance(s, int):
            return subelement
        
        elif isinstance(s, tuple):
            #find out if it is a slicing
            slicing = False
            for i in s:
                if not isinstance(i, int): slicing = True; break
                continue

        elif isinstance(s, slice ):
            slicing = True
            
        else:
            raise NotImplementedError, "Don't know how to get element indexed by %s" % (s,)


        if not slicing: return subelement
        else:
            subarr = subelement
            from NumpyNdArray import NdArray as NumpyNdArray
            res = NumpyNdArray( self.datatype(), 1, 0 )
            res._numarr = subarr
            res._orig_vecndarray = self
            return res
        raise
    

    def __setitem__(self, s, rhs):
        na = self.asNumarray()
        na.shape = self.shape()
        if isNdArray( rhs ): rhs = rhs.asNumarray()
        na[s] = rhs
        return


    #pickle interface    
    def __getstate__(self):
        data = self.asNumarray().copy()
        shape = self.shape()
        return self.datatype(), data, shape

    def __setstate__(self, inputs):
        datatype, data, shape = inputs
        import operator
        size = reduce( operator.mul, shape )
        initVal = 0
        NdArray.__init__( self, datatype, size, initVal )
        self.setShape( shape )
        self.asNumarray()[:] = data
        return
        

    pass # end of NdArray




def isNumber(a):
    return isinstance(a, int) or isinstance(a, float)


def isNdArray(a):
    return isinstance(a, NdArrayBase)



from NdArray import NdArray_TestCase as TestBase, unittest

class NdArray_TestCase(TestBase):
    
    def setUp(self):
        global NdArray
        self.NdArray = NdArray
        return

    pass # end of NdArray_TestCase




def pysuite():
    suite1 = unittest.makeSuite(NdArray_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    journal.info("ARCSStdVectorTest").activate()
    journal.info("NumpyNdArray").activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()



# version
__id__ = "$Id$"

# End of file 
