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

namespace ARCS_EventData{

  struct Event;

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
      m_grid( m_d ) += 1;
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

}


#endif // H_ARCSEVENTDATA_HISTOGRAMMER


// version
// $Id$

// End of file 
