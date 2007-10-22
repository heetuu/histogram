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


#ifndef H_ARCSEVENTDATA_EVENTS2IXY
#define H_ARCSEVENTDATA_EVENTS2IXY

#include "Histogrammer.h"
#include "events2histogram.h"

namespace ARCS_EventData{

  struct Event;
  
  /// Function to histogramming neutron events to I(x,y) histogram.
  /// events2Ix is a function that histograms neutron events (objects
  /// of class Event) in to a 2D histogram.
  /// Event2XY: a Event2Quantity2 class
  /// Ixy: a DataGrid2D class or a Ixy class
  /// IDataType: data type of intensity
  template <typename Event2XY, typename Ixy>
  void events2Ixy
  ( const Event *events, size_t N, const Event2XY & e2xy, Ixy & ixy )
  {
    Histogrammer2< Ixy, Event2XY, typename Ixy::xdatatype, typename Ixy::ydatatype> 
      her( ixy, e2xy );
    events2histogram( events, N, her );
    return ;
  }

}


#endif // H_ARCSEVENTDATA_EVENTS2IX


// version
// $Id$

// End of file 
  
