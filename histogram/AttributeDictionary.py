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


from AbstractAttributeContainer import AbstractAttributeContainer

class AttributeDictionary( AbstractAttributeContainer):


    def get( self, name):
        """get( name) -> value"""
        try:
            attr = self._attributes[ name]
        except KeyError:
            msg = "no attribute named %s" % name
            raise KeyError, msg
        return attr
    

    def set( self, name, value):
        """set( name, value) -> None"""
        self._attributes[name] = value
        return
    

    def __init__( self, attributes = None):
        if attributes is None: attributes = {}
        self._attributes = attributes
        return


    def __iter__(self): return self._attributes.iteritems()


    def copy(self): return AttributeDictionary( self._attributes.copy() )

    
def test():

    from AbstractAttributeContainer import TestCase as TC

    class TestCase(TC):

        def setUp(self):
            self.attributeContainer = AttributeDictionary( )
            return

        pass

    import unittest as ut
    suite = ut.makeSuite( TestCase )
    alltests = ut.TestSuite( (suite, ) )
    ut.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == "__main__": test()


# version
__id__ = "$Id$"

# End of file 
