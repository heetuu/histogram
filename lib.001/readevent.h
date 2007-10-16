#ifndef H_READEVENT
#define H_READEVENT

#include "event.h"

namespace DANSE{

  class EventsReader {
  public:
    
    EventsReader( const char * filename ) 
      : m_f( new std::ifstream(filename, std::ios_base::binary) )
    {
      if (m_f->bad()) 
	std::cerr <<  "unable to open file" << filename << std::endl;
      
      m_f->seekg(0, std::ios::beg); 
    }

    Event * read( size_t n ) {

      //Event *events = new Event[ n ];
      size_t N = n*sizeof(Event);

      char *buffer = new char [ N ];

      //std::cout << m_f << std::endl;
      //std::cout << m_f->good() << std::endl;
      //std::cout << m_f->rdstate() << std::endl;
      //std::cout << std::ios::failbit << std::endl;

      m_f->read( buffer, N );

      //for (int i=0; i<N; i++) std::cout << int(buffer[i]) << std::endl ;

      return (Event *)buffer;
    }
    
    ~EventsReader() { delete m_f; }

  private:
    std::ifstream *m_f;
  };
}

#endif
