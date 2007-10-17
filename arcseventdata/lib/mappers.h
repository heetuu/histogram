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


#ifndef H_ARCSEVENTDATA_MAPPERS
#define H_ARCSEVENTDATA_MAPPERS

#include "Event2Quantity.h"

namespace ARCS_EventData{

  class Event2TofChannel: public Event2Quantity1<unsigned int>
  {
  public:
    void operator() ( const Event & e, unsigned int & d ) const 
    {
      d = e.tof;
    }
  };
  
  const Event2TofChannel e2tc;

}


#endif // H_ARCSEVENTDATA_MAPPERS


// version
// $Id$

// End of file 
  
