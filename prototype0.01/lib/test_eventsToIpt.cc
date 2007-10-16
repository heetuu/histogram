#include <iostream>
#include <fstream>
#include "readevent.h"
#include "eventsToIpt.h"

int main()
{
  size_t Nevents = 10000;

  using namespace DANSE;

  const char * filename = "ARCS_5_neutron_event.dat";
  // read events
  EventsReader reader( filename );

  Event * pevents = reader.read( Nevents );

  unsigned int npixels = 113*8*128;

  unsigned int ntof = 100;

  unsigned int * counts = new unsigned int[ npixels * ntof ];

  unsigned int shape[2];
  shape[0] = npixels;
  shape[1] = ntof;

  unsigned int tofbegin(10000), tofend(90000), tofstep(800);

  eventsToIpt
    (
     pevents, Nevents, 
     counts, 
     shape,
     npixels,
     tofbegin, tofend, tofstep
     );



  delete [] counts;
  
  delete [] pevents;
}
