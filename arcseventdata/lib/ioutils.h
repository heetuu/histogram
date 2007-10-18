// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                        (C) 2007  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


#ifndef H_ARCS_EVENTDATA_IOUTILS
#define H_ARCS_EVENTDATA_IOUTILS

#include "histogram/Ix.h"

namespace ARCS_EventData{

  using DANSE::Ix;

  template <typename XDatatype, typename IDatatype>
  void dumpIx( const Ix< XDatatype, IDatatype > & ix, const char * filename )
  {
    std::ofstream of( filename );

    for (int i=0; i<ix.size; i++) 
      of << ix.xbegin + i * ix.xstep + ix.xstep/2 
	 << "\t" << ix.intensities[i] 
	 << std::endl;

    of.close();
    
    return;
  }

}// ARCS_EventData

#endif 


// version
// $Id$

// End of file 
