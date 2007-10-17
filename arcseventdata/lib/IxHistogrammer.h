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


#ifndef H_ARCSEVENTDATA_IXHISTOGRAMMER
#define H_ARCSEVENTDATA_IXHISTOGRAMMER

#include "histogram/Ix.h"
#include "Histogrammer.h"

namespace ARCS_EventData{

  using DANSE::Ix;

  /// IxHistogrammer
  /// This class showcase how to use Histogrammer1.
  /// This class is not really useful otherwise.
  template <typename XDataType, typename Event2X, typename YDataType>
  class IxHistogrammer
  {
  public:

    IxHistogrammer( XDataType xmin, XDataType xmax, XDataType xstep,
		    const Event2X & e2x )
      : m_ix(xmin, xmax, xstep), m_e2x( e2x ),
	m_base( m_ix, m_e2x )
    {
    }

    YDataType * Iarray() { return m_ix.intensities; }

    inline void operator() ( const Event & e )
    {
      m_base( e );
    }
    
    void clear() 
    {
      m_base.clear();
    }

  private:
    typedef Histogrammer1< Ix<XDataType, YDataType>, Event2X, YDataType > BaseT;

    typedef Ix<XDataType, YDataType> IxT;
    IxT m_ix;
    const Event2X & m_e2x;
    BaseT m_base;
  } ;

}


#endif // H_ARCSEVENTDATA_IXHISTOGRAMMER


// version
// $Id$

// End of file 
