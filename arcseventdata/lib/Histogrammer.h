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


#ifndef H_ARCSEVENTDATA_HISTOGRAMMER
#define H_ARCSEVENTDATA_HISTOGRAMMER

#include "histogram/AxisMapper.h"

namespace ARCS_EventData{

  using namespace DANSE;

  struct Event;

  /// Histogammer1: add event to a 1D histogram.
  /// Class to add neutron events (objects of Event class) 
  /// to a 1-D histogram (object of DataGrid1D).
  /// The is the core of event-mode reduction.
  /// The idea is, given a neutron event, the histogrammer
  /// deduce the value of the physical quantity from that neutron event, 
  /// and then do histogramming by add 1 to the bin
  /// in which the value of the physical quantity belongs.
  template <typename DataGrid, typename Event2Quantity1, typename DataType>
  class Histogrammer1 {
    
  public:
    Histogrammer1( DataGrid & grid, const Event2Quantity1 & e2q )
      : m_grid( grid ), m_e2q( e2q )
    {
    }
    
    void operator() ( const Event & e )
    {
      m_e2q( e, m_d );
      try {
	m_grid( m_d ) += 1;
      }
      catch (OutOfBound err)  {
	std::cout << m_d << ": out of bound" << std::endl;
      }
	
    }
    
    void clear() 
    {
      m_grid.clear();
    }

  private:
    DataGrid & m_grid;
    const Event2Quantity1 & m_e2q;
    DataType m_d;
  } ;


  /// Histogammer2: add event to a 2D histogram.
  /// Class to add neutron events (objects of Event class) 
  /// to a 2-D histogram (object of DataGrid2D).
  /// This is the core of event-mode reduction.
  /// The idea is, given a neutron event, the histogrammer
  /// deduce the values of the physical quantities from that neutron event, 
  /// and then do histogramming by add 1 to the bin
  /// in which the values of the physical quantities belong.
  template <typename DataGrid, typename Event2Quantity2, 
	    typename DataType1, typename DataType2>
  class Histogrammer2 {
    
  public:
    Histogrammer2( DataGrid & grid, const Event2Quantity2 & e2q2 )
      : m_grid( grid ), m_e2q2( e2q2 )
    {
    }
    
    void operator() ( const Event & e )
    {
      m_e2q2( e, m_d1, m_d2 );
      try {
	m_grid( m_d1, m_d2 ) += 1;
      }
      catch (OutOfBound err)  {
	std::cout << m_d1 << ", " << m_d2 << ": out of bound" << std::endl;
      }
	
    }
    
    void clear() 
    {
      m_grid.clear();
    }

  private:
    DataGrid & m_grid;
    const Event2Quantity2 & m_e2q2;
    DataType1 m_d1;
    DataType2 m_d2;
  } ;

}


#endif // H_ARCSEVENTDATA_HISTOGRAMMER


// version
// $Id$

// End of file 
