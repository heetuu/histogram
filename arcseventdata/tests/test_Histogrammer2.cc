#include <cstring>
#include <iostream>

#include "histogram/Ixy.h"
#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"
#include "arcseventdata/Histogrammer.h"


using namespace ARCS_EventData;

class Event2PixTofc: public Event2Quantity2<unsigned int, unsigned int>
{
  public:
  void operator() ( const Event & e, unsigned int & pix, unsigned int & tof ) const 
  {
    pix = e.pixelID;
    tof = e.tof;
  }
};


int main()
{
  
  using namespace ARCS_EventData;
  using namespace DANSE;
  
  typedef Ixy<unsigned int, unsigned int, unsigned int> Ipixtof;
  
  
  Ipixtof ipixtof( 0, 100, 1, 1000, 10000, 1000 );
  ipixtof.clear();
  assert (ipixtof(66, 3500) == 0);
  
  Event2PixTofc e2pt;
  
  Histogrammer2<Ipixtof, Event2PixTofc, unsigned int, unsigned int> her( ipixtof, e2pt );
  
  Event e = { 3500, 66 };
  
  her( e );
  
  assert (ipixtof(66, 3500) == 1);

  delete [] ipixtof.intensities;

  return 0;
  
}

