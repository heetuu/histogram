#include <iostream>
#include <fstream>

#include "readevent.h"

int main()
{

  using namespace DANSE;

  EventsReader reader( "ARCS_5_neutron_event.dat" );

  size_t N = 10;

  Event * pevents = reader.read( N );

  for (int i=0; i<N; i++) {
    std::cout << pevents[i].tof << ", " << pevents[i].pixelID << std::endl ;
  }

  delete [] pevents;

  return 0;
}
