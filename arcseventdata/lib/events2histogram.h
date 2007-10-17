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


#ifndef H_ARCSEVENTDATA_EVENTS2HISTOGRAM
#define H_ARCSEVENTDATA_EVENTS2HISTOGRAM

namespace ARCS_EventData{

  struct Event;
  
  template <typename Histogrammer>
  void events2histogram( const Event *events, size_t N, Histogrammer & her )
  {
    for (size_t i=0; i< N; i++ ) her( events[i] );
  }

}


#endif // H_ARCSEVENTDATA_EVENTS2HISTOGRAM


// version
// $Id$

// End of file 
