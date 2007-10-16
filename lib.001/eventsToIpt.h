#ifndef H_EVENTSTOIPT
#define H_EVENTSTOIPT


namespace DANSE {

  void eventsToIpt
    (
     Event *pevents,  size_t Nevents, 
     unsigned int *counts, 
     unsigned int shape[2],
     unsigned int ntotalpixels,
     unsigned int tofbegin, unsigned int tofend, unsigned int tofstep
     );
  
}


#endif //  H_EVENTSTOIPT
