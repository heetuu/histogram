#include <cstring>
#include <iostream>

#include "histogram/Ix.h"
#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"
#include "arcseventdata/Histogrammer.h"


using namespace ARCS_EventData;

class Event2TofChannel: public Event2Quantity1<unsigned int>
{
  public:
  void operator() ( const Event & e, unsigned int & d ) const 
  {
    d = e.tof;
  }
};


int main()
{
  
  using namespace ARCS_EventData;
  
  typedef Ix<unsigned int, unsigned int> Itof;
  
  
  Itof itof( 1000, 10000, 1000 );
  
  Event2TofChannel e2t;
  
  Histogrammer1<Itof, Event2TofChannel, unsigned int> her( itof, e2t );
  her.clear();
  
  Event e = { 3500, 2048 };
  
  her( e );
  
  assert (itof.Iarray()[2] == 1);
  
  return 0;
  
}

