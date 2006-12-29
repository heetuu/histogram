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


## multiple dimensional array of physcial values
## to represent a list where a common entity can be pulled out as "unit"

class PhysicalValueNdArray:

    def __init__(self, unit, numbers, roundingErrorTolerance = 1.e-7):
        """ctor
        unit: common entity of all physical values
        numbers: numbers withouth unit. must be a NdArray instance
        roundingErrorTolerance: rounding error tolerance
        """
        self._unit = unit
        if not isNdArray(numbers): raise ValueError, \
           "%s is not a NdArray instance" % (numbers,)
        self._numbers = numbers
        self.__iterCounter = 0
        self._roundingErrorTolerance = roundingErrorTolerance
        return


    def unit(self): return self._unit


    def numbers(self): return self._numbers


    def shape(self): return self._numbers.shape()


    #math functions
    def reverse(self):
        self._unit = 1./self._unit
        self._numbers.reverse()
        return


    #operators
    def __neg__(self):
        return -1. * self


    def __add__(self, other):
        r = self.copy()
        r += other
        return r
    

    __radd__ = __add__


    def __sub__(self, other):
        r = self.copy()
        r -= other
        return r


    def __rsub__(self, other):
        r = self.copy()
        r *= -1
        r += other
        return r


    def __mul__(self, other):
        r = self.copy()
        r *= other
        return r


    __rmul__ = __mul__
    
            
    def __div__(self, other):
        return self * (1./other)
            

    def __rdiv__(self, other):
        r = self.copy()
        r.reverse()
        r*=other
        return r


    # more operators. this time in-place
     
    def __iadd__(self, other):
        numbers = self._numbers
        if self.isCompatiblePhysicalValueArray(other):
            numbers += other.numbers() * (other.unit()/self.unit())
        else:
            # other is a value
            numbers += other/self.unit()
        return self


    def __isub__(self, other):
        numbers = self._numbers
        if self.isCompatiblePhysicalValueArray(other):
            numbers -= other.numbers() * (other.unit()/self.unit())
        else:
            # other is a value
            numbers -= other/self.unit()
        return self


    def __imul__(self, other):
        #other must be a value
        self._unit *= other
        return self
    

    def __idiv__(self, other):
        #other must be a value
        self._unit /= other
        return self


    def __getitem__(self, s):
        vs = self._numbers[s]
        if isNdArray(vs): return PhysicalValueNdArray( self._unit, vs )
        return self._unit*float(vs)


    def __setitem__(self, s, v):
        tmp = v/self._unit
        try: self._numbers[s] = tmp._numbers
        except: self._numbers[s] = tmp
        return


    def isCompatiblePhysicalValueArray(self, candidate):
        if not isinstance(candidate, PhysicalValueNdArray): return False
        try:  candidate._unit + self._unit
        except: return False
        return True


    def copy(self):
        return PhysicalValueNdArray( self._unit, self._numbers.copy(),
                                     self._roundingErrorTolerance)
    

    pass # end of PhysicalValueNdArray



#helpers

def isPhysicalValueNdArray( candidate ): return isinstance(candidate, PhysicalValueNdArray)
from ndarray.NdArray import NdArray
def isNdArray( candidate ): return isinstance( candidate, NdArray )


import unittest as ut



class TestCase(ut.TestCase):

    from pyre.units.SI import dimensionless, second

    def setUp(self):
        from ndarray.NumpyNdArray import NdArray
        numbers = NdArray( "double", range(100) )
        numbers.setShape( (10,10) )
        
        self.pvna = PhysicalValueNdArray( self.dimensionless, numbers)
        return
    
    
    def test_unit(self):
        "PhysicalValueNdArray: unit"
        self.assertEqual( self.pvna.unit( ), self.dimensionless )
        return


    def test___getitem__1(self):
        "PhysicalValueNdArray: pvna[ slice ]"
        sl = self.pvna[ 1:5]
        self.assertEqual( sl.__class__, PhysicalValueNdArray )
        return


    def test___getitem__2(self):
        "PhysicalValueNdArray: pvna[ index ]"
        self.assertEqual( self.pvna[ 1,5 ], 15.*self.dimensionless )
        return


    def test___iadd__1(self):
        "PhysicalValueNdArray: pvna += value"
        pvna = self.pvna.copy()
        pvna += 10.*self.dimensionless
        self.assertEqual( pvna[1,5], 25. * self.dimensionless)
        return


    def test___iadd__2(self):
        "PhysicalValueNdArray: pvna += pvna2"
        pvna = self.pvna.copy()
        pvna2 = pvna.copy()
        pvna += pvna2
        self.assertEqual( pvna[1,5], 30. * self.dimensionless)
        return


    def test___isub__1(self):
        "PhysicalValueNdArray: pvna -= value"
        pvna = self.pvna.copy()
        pvna -= 10.*self.dimensionless
        self.assertEqual( pvna[1,5], 5. * self.dimensionless)
        return


    def test___isub__2(self):
        "PhysicalValueNdArray: pvna -= pvna2"
        pvna = self.pvna.copy()
        pvna2 = pvna.copy()
        pvna -= pvna2
        self.assertEqual( pvna[1,5], 0. * self.dimensionless)
        return
    

    def test___imul__(self):
        "PhysicalValueNdArray: pvna *= value"
        pvna = self.pvna.copy()
        pvna *= 10.*self.second
        self.assertEqual( pvna[1,5], 150. * self.second)
        return


    def test___idiv__(self):
        "PhysicalValueNdArray: pvna /= value"
        pvna = self.pvna.copy()
        pvna /= 10.*self.second
        self.assertEqual( pvna[1,5], 1.5 / self.second)
        return


    def test___neg__(self):
        "PhysicalValueNdArray: -pvna "
        pvna = -self.pvna
        self.assertEqual( pvna[1,5], -15 * self.dimensionless)
        return
    

    def test___add__1(self):
        "PhysicalValueNdArray: pvna1 + value"
        pvna1 = self.pvna + 10*self.dimensionless
        self.assertEqual( pvna1[1,5], 25 * self.dimensionless)
        return


    def test___add__2(self):
        "PhysicalValueNdArray: pvna1 + pvna2"
        pvna3 = self.pvna + self.pvna
        self.assertEqual( pvna3[1,5], 30 * self.dimensionless)
        return
    

    def test___sub__1(self):
        "PhysicalValueNdArray: pvna1 - value"
        pvna1 = self.pvna - 10*self.dimensionless
        self.assertEqual( pvna1[1,5], 5 * self.dimensionless)
        return


    def test___sub__2(self):
        "PhysicalValueNdArray: pvna1 - pvna2"
        pvna3 = self.pvna - self.pvna.copy()
        self.assertEqual( pvna3[1,5], 0. * self.dimensionless)
        return

    
    def test___mul__(self):
        "PhysicalValueNdArray: pvna1 * value"
        pvna1 = self.pvna * (10*self.second)
        self.assertEqual( pvna1[1,5], 150. * self.second)
        return
    

    def test___div__(self):
        "PhysicalValueNdArray: pvna1 / value"
        pvna1 = self.pvna / (10*self.second)
        self.assertEqual( pvna1[1,5], 1.5 / self.second)
        return
    

    def test___rdiv__(self):
        "PhysicalValueNdArray: value / pvna"
        #pvna1 = (10*self.second) /self.pvna
        pvna1 = self.pvna.__rdiv__(10*self.second) 
        self.assertEqual( pvna1[1,5], 2./3 * self.second)
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
