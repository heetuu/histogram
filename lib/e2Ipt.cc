#include <iostream>
#include <fstream>
#include "readevent.h"
#include "eventsToIpt.h"

int run( const char *filename, size_t Nevents, 
	 unsigned int tofbegin, unsigned int tofend, unsigned int tofstep,
	 const char *ofilename
	 )
{  

  using namespace DANSE;

  // read events
  EventsReader reader( filename );

  Event * pevents = reader.read( Nevents );

  unsigned int npixels = 115*8*128;

  unsigned int ntof = (tofend-tofbegin)/tofstep;

  unsigned int * counts = new unsigned int[ npixels * ntof ];

  unsigned int shape[2];

  shape[0] = npixels;
  shape[1] = ntof;

  std::cout << "pevents=" << pevents << std::endl
	    << "Nevents=" << Nevents << std::endl
	    << "counts=" << counts << std::endl
	    << "shape=" << shape[0] << ',' << shape[1] << std::endl
	    << "npixels=" << npixels << std::endl
	    << "tof=" << tofbegin << ", " << tofend << ", " << tofstep << std::endl
    ;
  eventsToIpt
    (
     pevents, Nevents, 
     counts, 
     shape,
     npixels,
     tofbegin, tofend, tofstep
     );

  using namespace std;
  ofstream f( ofilename, ios_base::binary);

  f.write( (char *)counts, sizeof( unsigned int ) * npixels*ntof );

  delete [] counts;
  
  delete [] pevents;
}


int main(int argc, char ** argv)
{
  assert (argc == 7 );

  char *filename = argv[1];

  size_t Nevents = atoi( argv[2] );
  
  unsigned int tofbegin = atoi( argv[3] );
  unsigned int tofend = atoi( argv[4] );
  unsigned int tofstep = atoi( argv[5] );

  char *ofilename = argv[6];

  run( filename, Nevents, tofbegin, tofend, tofstep, ofilename );

  return 0;
}

