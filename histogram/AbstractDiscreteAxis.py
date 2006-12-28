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


    def __init__(self, physical_quantity_type ):
        self._physical_quantity_type = physical_quantity_type
        return


    def physical_quantity_type(self): return self._physical_quantity_type


    def physical_quantities(self):
        pqt = self._physical_quantity_type
        from PhysicalQuantity import new
        return [ new(pqt, v) for v in self.values() ]


    def index(self, physical_quantity):
        value = self._getValue( physical_quantity )
        return self._index( value )


    def slicingInfo2IndexSlice(self, slicingInfo):
        """slicingInfo2Range(slicingInfo) --> slice instance
        note: slicing is inclusive
        """
        startPQ, endPQ = slicingInfo.start, slicingInfo.end
        start = self._getValue( startPQ )
        end = self._getValue( endPQ )
        values = self.values()
        if start == front: start = values[0]
        if end == back: end = values[-1]
        #slice. +1 to make the end bracket inclusive
        s = ( self._index( start ), self._index( end ) + 1 )
        return slice( *s )


    def values(self):
        raise NotImplementedError


    def __eq__(self, rhs):
        if not isinstance(rhs, AbstractDiscreteAxis): return False
        try: self._physical_quantity_type.checkCompatibility( rhs._physical_quantity_type )
        except: return False
        for pq1, pq2 in zip(self.physical_quantities(), rhs.physical_quantities()):
            if pq1 != pq2 : return False
            continue
        return True
    
    
    def __ne__(self, rhs):
        return not (self == rhs)
    
    
    def __getitem__(self, s):
        raise NotImplementedError

        
    def _index(self, value):
        raise NotImplementedError


    def _getValue(self, physical_quantity):
        from PhysicalQuantity import getValue
        return getValue(self._physical_quantity_type, physical_quantity )

    pass


from SlicingInfo import front, back


import unittest as ut

class TestCase(ut.TestCase):

    def setUp(self):
        # overload this to test a special subclass of AbstractDiscreteAxis
        # requirements:
        #  * axis must have more than 2 "ticks"
        self.axis = None
        return


    def test_values(self):
        "DiscreteAxis: values"
        axis = self.axis
        axis.values()
        return


    def test_slicingInfo2IndexSlice(self):
        "DiscreteAxis: slicinginfo2indexslice"
        axis = self.axis
        values = axis.values()
        tp = self.axis.physical_quantity_type()
        from PhysicalQuantity import new
        q1 = new(tp, values[0] )
        q2 = new(tp, values[-2] )
        from SlicingInfo import SlicingInfo
        si = SlicingInfo( q1, q2 )
        s = axis.slicingInfo2IndexSlice( si )
        self.assertEqual( s, slice(0, len(values)-1) )
        return


    def test_getitem(self):
        "DiscreteAxis: __getitem__"
        axis = self.axis
        values = axis.values()
        tp = self.axis.physical_quantity_type()
        from PhysicalQuantity import new
        q1 = new(tp, values[0] )
        q2 = new(tp, values[-2] )
        from SlicingInfo import SlicingInfo
        si = SlicingInfo( q1, q2 )
        newAxis = axis[ si ]
        self.assertEqual( axis.physical_quantity_type(), newAxis.physical_quantity_type() )
        self.assertEqual( len(newAxis.values() ), len(values) - 1 )
        return
    
        
    def test_index(self):
        "DiscreteAxis: index"
        raise NotImplementedError


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
