#include <cstring>
#include <iostream>

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"
#include "arcseventdata/events2Ix.h"
#include "arcseventdata/Itof.h"


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
  Event e = { 3500, 2048 };

  Event2TofChannel e2t;

  Itofchannel itof( 1000, 8000, 1000 );
  itof.clear();
  
  events2Ix< Event2TofChannel, Itofchannel > (&e, 1, e2t, itof);

  unsigned int * intensities = itof.intensities;
  
  assert (intensities[2] == 1);
  
  delete [] intensities;

  return 0;
}

