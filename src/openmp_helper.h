#ifndef _OPENMP_HELPER_H_
#define _OPENMP_HELPER_H_

#ifdef _OPENMP
    // include openmp header
    #include <omp.h>
#else
    // define serial dummy versions of openmp functions
    // for when compiled without openmp support
    #define omp_get_max_threads() 1
    #define omp_get_thread_num() 0
#endif

#endif
