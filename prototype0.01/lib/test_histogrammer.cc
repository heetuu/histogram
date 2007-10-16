#include <cassert>
#include <cstring>
#include <iostream>

#include "histogrammer.h"


int main()

{

  using namespace DANSE;

  unsigned int counts [ 4*6 ];
  for (int i=0; i<4*6; i++) counts[i] = 0;
  short shape[2];

  shape[0] = 4; shape[1] = 6;

  Histogrammer<unsigned int *, unsigned int, short, size_t> her(counts, shape, 2);

  short indexes[2];
  indexes[0] = 2; indexes[1] = 3;
  her.increment( indexes );

  for (int i=0; i<4*6; i++)
    std::cout << counts[i] << ", ";
  std::cout << std::endl;

  assert( counts[0] == 0 );
  assert( counts[ 3+2*6 ] == 1 );

  return 0;
}
