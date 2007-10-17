// -*- C++ -*-
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 
//                               Michael A.G. Aivazis
//                        California Institute of Technology
//                        (C) 1998-2005  All Rights Reserved
// 
//  <LicenseText>
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 

#include <portinfo>
#include <Python.h>

#include "bindings.h"

#include "misc.h"          // miscellaneous methods

// the method table

struct PyMethodDef pyarcseventdata_methods[] = {

    // dummy entry for testing
    {pyarcseventdata_hello__name__, pyarcseventdata_hello,
     METH_VARARGS, pyarcseventdata_hello__doc__},

    {pyarcseventdata_copyright__name__, pyarcseventdata_copyright,
     METH_VARARGS, pyarcseventdata_copyright__doc__},


// Sentinel
    {0, 0}
};

// version
// $Id$

// End of file
