#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Range:

    def __init__(self, *inputs ):
        """
        Range( 3.0, 5.5 )
        Range( 1, 99 )
        Range( Range( 3,5 ) )
        Range( front, 33 )
        """
        if len(inputs)==1:
            range = inputs[0]
            if not isinstance(range, Range): self._wrongInputs( inputs )
            self.start, self.end = range.start, range.end
            return
        else:
            try: self.start, self.end = inputs 
            except: self._wrongInputs(inputs)
            pass
        return


    def __str__(self):
        return "[%s:%s]" % (self.start, self.end)


    __repr__ = __str__


    def _wrongInputs(self, inputs):
        raise ValueError , \
              "Wrong inputs for Range: %s" \
              % (inputs,)


    class SpecialPosition:

        def __init__(self, name):
            self.name = name
            return


        def __str__(self): return "%s" % self.name

        pass # end of SpecialPosition


    pass # end of Range


front = Range.SpecialPosition( "front" )
back = Range.SpecialPosition( "back" )
all = Range( front, back )



def isRange( s ):
    return isinstance(s, Range)



def test():
    Range( 3.0, 5.5 )
    Range( 1, 99 )
    Range( Range( 3,5 ) )
    Range( front, 33 )
    return

if __name__ == "__main__": test()

# version
__id__ = "$Id$"

# End of file 
