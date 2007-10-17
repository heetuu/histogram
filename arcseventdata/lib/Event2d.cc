#include <math.h>
#include "Event.h"
#include "Event2d.h"

namespace ARCS_EventData {
  
  void
  Event2d::operator ()
    ( const Event & e, double &d ) const
  {
    const unsigned int & pixelID = e.pixelID;
    const unsigned int & tofchannelno = e.tof;

    const double *ppos = m_pixelPositions + 3*pixelID;
    const double &x = *ppos;
    const double &y = *(ppos+1);
    const double &z = *(ppos+2);

    double tof = tofchannelno * m_tofUnit;

    double velocity = m_mod2sample/tof;
    double lambda = 2*pi/(velocity * V2K);

    double twotheta = acos( z /sqrt(x*x+y*y+z*z) );

    d = lambda/2/sin(twotheta/2);
  }
  
}


