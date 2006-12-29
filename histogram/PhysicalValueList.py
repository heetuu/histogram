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


## list of physcial values
## to represent a list where a common entity can be pulled out as "unit"

class PhysicalValueList:

    def __init__(self, unit, values, roundingErrorTolerance = 1.e-7):
        self._unit = unit
        self._values = values
        self.__iterCounter = 0
        self._roundingErrorTolerance = roundingErrorTolerance
        return


    def unit(self): return self._unit


    def values(self): return self._values


    def index(self, pv):
        v = pv/self._unit 
        try:
            return self._values.index( v )
        except ValueError, e:
            if "not in list" in str(e):
                return searchIndex( v, self._values, self._roundingErrorTolerance)
            raise
        raise


    def __len__(self): return len(self._values)


    def __eq__(self, other):
        if not isPhysicalValueList( other ): return False
        if len(self) != len(other): return False
        try: conversion = other._unit/self._unit
        except: return False
        if not isNumber(conversion): return False
        for v1, v2 in zip(self._values, other._values):
            if abs(v1-v2*conversion) > abs(v1) * self._roundingErrorTolerance: return False
            continue
        return True


    def __ne__(self, other): return not (self==other)


    def __getitem__(self, s):
        vs = self._values[s]
        if "__iter__" in dir(vs): return PhysicalValueList( self._unit, vs )
        return self._unit*vs


    def __setitem__(self, s, v):
        if isinstance(s, slice):
            raise NotImplementedError
        self._values[s] = v/self._unit
        return


    def __iter__(self): return self
    
    def next(self):
        if self.__iterCounter < len(self):
            v = self._values[self.__iterCounter]*self._unit
            self.__iterCounter += 1
            return v
        self.__iterCounter = 0
        raise StopIteration


    pass # end of PhysicalValueList



def isPhysicalValueList( candidate ): return isinstance(candidate, PhysicalValueList)

def isNumber( candidate ):
    types = [int, long, float]
    for t in types:
        if isinstance(candidate, t): return True
        continue
    return False


#helper

def searchIndex( value, values, roundingErrorTolerance ):
    size = len(values)
    for i,v in enumerate(values):
        j = i+1
        if j >= size:
            assert i==size-1
            j = i-1
            if j<0:  break
            pass

        diff = values[j] - values[i]
        if diff == 0.0 : continue
        err = roundingErrorTolerance * abs(diff)
        if abs(value-v) < err : return i
        continue

    raise ValueError, "cannot find %s in %s" % (value, values)




import unittest as ut

class Helper_TestCase(ut.TestCase):

    def test_searchIndex(self):
        "helper: searchIndex"
        self.assertEqual( searchIndex ( 2.99999999, [1.,2.,3], 1e-5), 2 )
        self.assertEqual( searchIndex ( 2.9999999999999, [1.,2.,3], 1e-5), 2 )
        self.assertEqual( searchIndex ( 2.00000000001, [1.,2.,3], 1e-5), 1 )
        self.assertRaises( ValueError, searchIndex, 2.1, [1.,2.,3], 1e-5)
        return

    pass # end of Helper_TestCase




class TestCase(ut.TestCase):

    from pyre.units.energy import eV
    from pyre.units.time import second

    def setUp(self):
        self.pvl = PhysicalValueList( self.eV, [-8., -7., -6., -5.0, -4.0, -3.0] )
        self.pvl2 = PhysicalValueList( self.eV, [-8., -7., -6., -5., -4., -3.] )
        self.different_pvls = [
            [1,2,3],
            PhysicalValueList( self.second, [-8., -7., -6., -5., -4., -3.] ),
            PhysicalValueList( self.eV, [-8., -7., -6., -5., -4.] ),
            ]
        return
    
    
    def test_unit(self):
        "PhysicalValueList: unit"
        self.assertEqual( self.pvl.unit( ), self.eV )
        return


    def test___getitem__1(self):
        "PhysicalValueList: pvl[ slice ]"
        sl = self.pvl[ 1:5]
        self.assertEqual( sl.__class__, PhysicalValueList )
        return


    def test___getitem__2(self):
        "PhysicalValueList: pvl[ index ]"
        self.assertEqual( self.pvl[ 1], -7*self.eV) 
        return


    def test___eq__(self):
        "PhysicalValueList: a == b"
        self.assertEqual( self.pvl, self.pvl2 )
        return


    def test___ne__(self):
        "PhysicalValueList: a != b"
        for pvl in self.different_pvls:
            self.assertNotEqual( self.pvl, pvl )
        return

    pass



def test():
    import unittest as ut
    suite = ut.makeSuite( TestCase )
    suite2 = ut.makeSuite( Helper_TestCase )
    alltests = ut.TestSuite( (suite, suite2) )
    ut.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == "__main__": test()





# version
__id__ = "$Id$"

# End of file 
