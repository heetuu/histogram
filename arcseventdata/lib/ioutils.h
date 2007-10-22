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


#ifndef H_ARCS_EVENTDATA_IOUTILS
#define H_ARCS_EVENTDATA_IOUTILS

#include "histogram/Ix.h"
#include "histogram/Ixy.h"

namespace ARCS_EventData{

  using DANSE::Ix;

  template <typename XDatatype, typename IDatatype>
  void dumpIx( const Ix< XDatatype, IDatatype > & ix, const char * filename )
  {
    std::ofstream of( filename );

    for (int i=0; i<ix.size; i++) 
      of << ix.xbegin + i * ix.xstep + ix.xstep/2 
	 << "\t" << ix.intensities[i] 
	 << std::endl;

    of.close();
    
    return;
  }


  using DANSE::Ixy;

  /// dump Ixy to a binary data file.
  /// This is not really a structured way to save data. 
  /// The purpose for now is that we will be able to save this
  /// histogram to a binary data file, and then read it
  /// from python and save the histogram in hdf5 file format.
  /// This way, we don't need to write python bindings of
  /// all these codes. 
  /// Future, we should have python bindings for this c++ library,
  /// and we will not need this function.
  template <typename XDatatype, typename YDatatype, typename IDatatype>
  void dumpIxy( const Ixy< XDatatype, YDatatype, IDatatype > & ixy, const char * filename )
  {
    std::ofstream of( filename, std::ios::binary );
    XDatatype x; YDatatype y;
    
    std::cout << "In dumpIxy" << std::endl;
    std::cout << "ixy shape: " << ixy.shape[0] << "," << ixy.shape[1] << std::endl;

    char * buf = (char *) ixy.intensities; // bad implementation. intensities could be any iterator, but here we assume that intensities is a pointer
    size_t n = ixy.size * sizeof( IDatatype ) ;
    of.write(buf, n );

    /*
    size_t n = 0;
    for (int i=0; i<ixy.shape[0]; i++) {
      
      x = ixy.xbegin + i * ixy.xstep + ixy.xstep/2;
      
      for (int j=0; j<ixy.shape[1]; j++) {
	
	y = ixy.ybegin + j * ixy.ystep + ixy.ystep/2;
	
	of << ixy( x,y );

	n+=1;

      }

    }
    */
    std::cout << n << " data written" << std::endl;
    of.close();
    
    return;
  }

}// ARCS_EventData

#endif 


// version
// $Id$

// End of file 
