#include <math.h>
#include <iostream>
#include "Event.h"
#include "Event2d.h"

namespace ARCS_EventData {
  
  void
  Event2d::operator ()
    ( const Event & e, double &d ) const
  {
    const unsigned int & pixelID = e.pixelID;
    if (pixelID<0 || pixelID>=m_ntotpixels) {
      std::cout << "pixel ID out of bound: " << pixelID << std::endl;
      d = 0.0;
      return;
    }
    const unsigned int & tofchannelno = e.tof;

    const double *ppos = m_pixelPositions + 3*pixelID;
    const double &x = *ppos;
    const double &y = *(ppos+1);
    const double &z = *(ppos+2);

    double tof = tofchannelno * m_tofUnit;

    double sample2pixel = sqrt(x*x+y*y+z*z);
    double velocity = (m_mod2sample+sample2pixel)/tof;
    double lambda = 2*pi/(velocity * V2K);

    double twotheta = acos( x / sample2pixel );

    d = lambda/2/sin(twotheta/2);

//    std::cout << "pixelID=" << pixelID << ", x,y,z=" << x << "," << y << "," << z << ", sample2pixel = " << sample2pixel << ", mo2sample=" << m_mod2sample << "tof = " << tof << "velocity = " << velocity << "lambda=" << lambda << "twotheta = " << twotheta << ", d = " << d << std::endl;
  }
  
}


