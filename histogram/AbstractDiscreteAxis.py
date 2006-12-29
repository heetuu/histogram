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


class AbstractDiscreteAxis:


    def __init__(self, quantityValueList ):
        self._qvList = quantityValueList
        self.quantity = quantityValueList.quantity
        self.values = quantityValueList.values #
        assert len(quantityValueList) > 2, "an axis must have at least 3 ticks"
        return


    def ticks(self):
        "return values of 'ticks'"
        return self.values


    def index(self, value):
        """return index of value in the 'ticks'
        overload this method to provide more complex behavior
        """
        return self.values.index( value )


    def range2IndexSlice(self, range):
        """range2IndexSlice(range) --> slice instance
        note: slicing is inclusive
        """
        start, end = range.start, range.end
        values = self.values
        if start == front: start = values[0]
        if end == back: end = values[-1]
        #slice. +1 to make the end bracket inclusive
        s = self.index( start ), self.index( end ) + 1
        return slice( *s )


    def __len__(self): return len(self.values)


    def __eq__(self, rhs):
        if not isinstance(rhs, AbstractDiscreteAxis): return False
        return self._qvList == rhs._qvList
    
    
    def __ne__(self, rhs):
        return not (self == rhs)
    
    
    def __getitem__(self, s):
        raise NotImplementedError


    def __str__(self):
        vs = self.values
        return "%s: [%s, %s, ..., %s]" % (
            self.quantity, vs[0], vs[1], vs[-1] )
        
    pass


from Range import front, back


import unittest as ut

class TestCase(ut.TestCase):

    def setUp(self):
        # overload this to test a special subclass of AbstractDiscreteAxis
        # requirements:
        #  * axis must have more than 2 "ticks"
        self.axis = None
        return


    def test_quantity(self):
        "DiscreteAxis: quantity"
        axis = self.axis
        axis.quantity
        return


    def test_values(self):
        "DiscreteAxis: values"
        axis = self.axis
        axis.values
        return


    def test_range2IndexSlice(self):
        "DiscreteAxis: range2indexslice"
        axis = self.axis
        values = axis.values
        v1 = values[0] 
        v2 = values[-2] 
        from Range import Range
        si = Range( v1, v2 )
        s = axis.range2IndexSlice( si )
        self.assertEqual( s, slice(0, len(values)-1) )
        return


    def test___getitem__(self):
        "DiscreteAxis: __getitem__"
        axis = self.axis
        values = axis.values
        v1 = values[0] 
        v2 = values[-2] 
        from Range import Range
        si = Range( v1, v2 )
        newAxis = axis[ si ]
        self.assertEqual( axis.quantity, newAxis.quantity )
        self.assertEqual( len(newAxis.values ), len(values) - 1 )
        return
    
        
    def test_index(self):
        "DiscreteAxis: index"
        raise NotImplementedError


    def test___len__(self):
        "DiscreteAxis: len(axis)"
        self.assertEqual( len(self.axis), len(self.axis.values) )
        return


    def test___eq__(self):
        "DiscreteAxis: a == b"
        raise NotImplementedError


    def test___ne__(self):
        "DiscreteAxis: a != b"
        raise NotImplementedError


    pass


# version
__id__ = "$Id$"

# End of file 
