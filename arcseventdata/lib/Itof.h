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


#ifndef H_ARCS_EVENTDATA_ITOF
#define H_ARCS_EVENTDATA_ITOF


#include "histogram/Ix.h"

namespace ARCS_EventData{

  using DANSE::Ix;

  typedef Ix< unsigned int, unsigned int> Itofchannel;
  typedef Ix< double, unsigned int> Itof;

}// ARCS_EventData

#endif 


// version
// $Id$

// End of file 
