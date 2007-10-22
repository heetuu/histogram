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


#ifndef H_ARCS_EVENTDATA_IPIXTOF
#define H_ARCS_EVENTDATA_IPIXTOF


#include "histogram/Ixy.h"

namespace ARCS_EventData{

  using DANSE::Ixy;

  typedef Ixy< unsigned int, unsigned int, unsigned int> Ipixtofc;
  typedef Ixy< unsigned int, double, unsigned int> Ipixtof;

}// ARCS_EventData

#endif 


// version
// $Id$

// End of file 
