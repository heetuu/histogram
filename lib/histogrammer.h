
#ifndef H_HISTOGRAMMER
#define H_HISTOGRAMMER


namespace DANSE {

template <typename Iterator, typename DataType, typename Size, typename SuperSize>
class Histogrammer {

  public:
    // array shape must have 'ndim' elements
    Histogrammer( Iterator it, Size * shape, int ndim) :
      m_it(it), m_ndim( ndim ), m_shape( new Size[ndim] ) {

      for (int i=0; i<ndim; i++) m_shape[i] = shape[i];

    }

    ~Histogrammer() { delete [] m_shape; }

    // indexes must have 'ndim' elements
    void increment( Size *indexes, const DataType & d = 1 ) {
      SuperSize ind = 0; // what if this get out of bound of largest integer?
      SuperSize N = 1;
      for (int i=m_ndim-1; i>=0; i--  ) {
        ind += N * indexes[ i ]; 
        N *= m_shape[ i ];
      }
      *(m_it+ind) += d;
    }

  private:
    Iterator m_it;
    Size *m_shape;
    int  m_ndim;
};

}

#endif

