#include <iostream>

#include "event.h"
#include "histogrammer.h"

namespace DANSE {

  void eventsToIpt
  (
   Event *pevents,  size_t Nevents, 
   unsigned int *counts, 
   unsigned int shape[2],
   unsigned int ntotalpixels,
   unsigned int tofbegin, unsigned int tofend, unsigned int tofstep
   )
  {
    using namespace DANSE;
    
    unsigned int ntofbins = (tofend-tofbegin)/ tofstep;
    
    assert (shape[0] == ntotalpixels); 
    assert (shape[1] == ntofbins);
    
    Histogrammer<unsigned int *, unsigned int, unsigned int, size_t> her(counts, shape, 2);
    
    unsigned int indexes[2];
    
    for (int i=0; i<Nevents; i++) {
      
      const uint &pix = pevents[i].pixelID;
      const uint &tof = pevents[i].tof;
      
      if (tof < tofbegin || tof > tofend) {
	std::cout << "tof " << tof << " is out of bound" << std::endl;
	continue;
      }
      if (pix > ntotalpixels-1) {
	std::cout << "pix " << pix << " is out of bound" << std::endl;
	continue;
      }
      
      indexes[0] = pix;
      indexes[1] = (tof - tofbegin)/tofstep;
      
      her.increment( indexes );
      
    }
    
  }
  
} // namespace DANSE
