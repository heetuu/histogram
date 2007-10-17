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


#ifndef H_ARCSEVENTDATA_EVENT2QUANTITY
#define H_ARCSEVENTDATA_EVENT2QUANTITY

namespace ARCS_EventData{

  struct Event;

  /// Event2Quantity1
  /// convert event to a quantity
  /// Forexample, 
  ///   event --> pixel ID
  ///   event --> tof 
  template <typename DataType>
  class Event2Quantity1 {
  public:
    virtual void operator() ( const Event & e, DataType & d ) const = 0;
    virtual ~Event2Quantity1() {} ;
  };

  /// Event2Quantity2
  /// convert event to two quantities
  /// Forexample, 
  ///   event --> pixel ID, tof
  ///   event --> Q, E
  template <typename DataType1, typename DataType2>
  class Event2Quantity2 {
  public:
    virtual void operator() ( const Event & e, DataType1 & d1, DataType2 &d2 ) const = 0;
    virtual ~Event2Quantity2() {}
  };
}


#endif // H_ARCSEVENTDATA_EVENT2QUANTITY


// version
// $Id$

// End of file 
