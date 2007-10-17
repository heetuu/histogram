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


#ifndef H_ARCSEVENTDATA_EVENTS2IX
#define H_ARCSEVENTDATA_EVENTS2IX

#include "IxHistogrammer.h"
#include "events2histogram.h"

namespace ARCS_EventData{

  struct Event;
  
  ///
  /// Event2X: a Event2Quantity class
  /// Ix: a DataGrid1D class or  Ix class
  /// IDataType: data type of intensity
  template <typename Event2X, typename Ix>
  void events2Ix
  ( const Event *events, size_t N, const Event2X & e2x, Ix & ix )
  {
    Histogrammer1< Ix, Event2X, typename Ix::xdatatype> her( ix, e2x );
    events2histogram( events, N, her );
    return ;
  }

}


#endif // H_ARCSEVENTDATA_EVENTS2IX


// version
// $Id$

// End of file 
  
