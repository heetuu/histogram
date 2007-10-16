#include <iostream>
#include <fstream>

#include "readevent.h"
#include "histogrammer.h"

int run( const char *filename,  size_t Nevents,  unsigned int tofbegin, unsigned int tofend, unsigned int tofstep,
	 const char *outfilename)
{

  using namespace DANSE;

  // read events
  EventsReader reader( filename );

  Event * pevents = reader.read( Nevents );


  unsigned int nbins = (tofend-tofbegin)/ tofstep;

  unsigned int counts [ nbins ];

  for (int i=0; i<nbins; i++) counts[i] = 0;

  unsigned int shape[1];

  shape[0] = nbins;

  Histogrammer<unsigned int *, unsigned int, unsigned int, size_t> her(counts, shape, 1);

  unsigned int indexes[1];

  for (int i=0; i<Nevents; i++) {
    const uint &tof = pevents[i].tof;
    
    if (tof < tofbegin || tof > tofend) {
      std::cout << "tof " << tof << " is out of bound" << std::endl;
      continue;
    }
    indexes[0] = (tof - tofbegin)/tofstep;

    her.increment( indexes );

  }

  delete [] pevents;

  std::ofstream of( outfilename );

  for (int i=0; i<nbins; i++) {
    of << tofbegin + i * tofstep + tofstep/2 << "\t" << counts[i] << std::endl;
  }

  of.close();

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
