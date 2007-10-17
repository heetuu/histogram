#include <cstring>
#include <iostream>

#include "arcseventdata/Event.h"
#include "arcseventdata/mappers.h"
#include "arcseventdata/events2Ix.h"
#include "arcseventdata/Itof.h"
#include "arcseventdata/EventsReader.h"


int run( const char *filename,  size_t Nevents, 
	 unsigned int tofbegin, unsigned int tofend, unsigned int tofstep,
	 const char *outfilename)
{

  using namespace ARCS_EventData;

  // read events
  EventsReader reader( filename );

  Event * pevents = reader.read( Nevents );

  Itofchannel itof( tofbegin, tofend, tofstep );
  itof.clear();
  
  events2Ix< Event2TofChannel, Itofchannel > (pevents, Nevents, e2tc, itof);

  unsigned int * intensities = itof.intensities;
  
  delete [] pevents;

  std::ofstream of( outfilename );

  for (int i=0; i<itof.size; i++) {
    of << tofbegin + i * tofstep + tofstep/2 << "\t" << itof.intensities[i] << std::endl;
  }

  of.close();

  delete [] intensities;

  return 0;
}

void help()
{
  std::cout << "itof event-data-filename Nevents tofbegin tofend tofstep output-filename" << std::endl;
  std::cout << "  - tof: 100us" << std::endl;
}


int main( int argc, char ** argv )
{
  if (argc != 7 ) { help(); exit(1); }

  char *filename = argv[1];

  size_t Nevents = atoi( argv[2] );
  
  unsigned int tofbegin = atoi( argv[3] );
  unsigned int tofend = atoi( argv[4] );
  unsigned int tofstep = atoi( argv[5] );

  char *ofilename = argv[6];

  run( filename, Nevents, tofbegin, tofend, tofstep, ofilename );

  return 0;
}



