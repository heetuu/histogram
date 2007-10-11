#include <iostream>
#include <fstream>

#include "readevent.h"
#include "histogrammer.h"

int run( const char *filename,  size_t Nevents,  unsigned int pixbegin, unsigned int pixend, unsigned int pixstep,
	 const char *outfilename)
{

  using namespace DANSE;

  // read events
  EventsReader reader( filename );

  Event * pevents = reader.read( Nevents );


  unsigned int nbins = (pixend-pixbegin)/ pixstep;

  unsigned int counts [ nbins ];

  for (int i=0; i<nbins; i++) counts[i] = 0;

  unsigned int shape[1];

  shape[0] = nbins;

  Histogrammer<unsigned int *, unsigned int, unsigned int, size_t> her(counts, shape, 1);

  unsigned int indexes[1];

  for (int i=0; i<Nevents; i++) {
    const uint &pix = pevents[i].pixelID;
    
    if (pix < pixbegin || pix > pixend) {
      std::cout << "pix " << pix << " is out of bound" << std::endl;
      continue;
    }
    indexes[0] = (pix - pixbegin)/pixstep;

    her.increment( indexes );

  }

  delete [] pevents;

  std::ofstream of( outfilename );

  for (int i=0; i<nbins; i++) {
    of << pixbegin + i * pixstep + pixstep/2 << "\t" << counts[i] << std::endl;
  }

  of.close();

  return 0;
}


int main( int argc, char ** argv )
{
  assert (argc == 7 );

  char *filename = argv[1];

  size_t Nevents = atoi( argv[2] );
  
  unsigned int pixbegin = atoi( argv[3] );
  unsigned int pixend = atoi( argv[4] );
  unsigned int pixstep = atoi( argv[5] );

  char *ofilename = argv[6];

  run( filename, Nevents, pixbegin, pixend, pixstep, ofilename );

  return 0;
}
