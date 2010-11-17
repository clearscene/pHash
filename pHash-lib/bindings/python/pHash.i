/*

    pHash, the open source perceptual hash library
    Copyright (C) 2008-2009 Aetilius, Inc.
    All rights reserved.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    swig interface by Loic Jaquemet - loic.jaquemet@gmail.com

*/
/* 
install swig python-dev CImg-dev & others
see swig autorun automake ... http://realmike.org/python/swig_linux.htm
or distutils
*/

%include "std_string.i"
%include "exception.i" 
%include "typemaps.i"
%include "cpointer.i"
%include "carrays.i"
%include "cmalloc.i"
// basic typedef ...  
%include "stdint.i"
%include "windows.i"


/* 
ignoring static, private or useless function
or non-compatible 
*/
%ignore ph_readfilenames;

%ignore ph_dct;
%ignore ph_dct_matrix;

%ignore _ph_image_digest;

%ignore _ph_map_mvpfile;
%ignore _ph_unmap_mvpfile;
%ignore _ph_save_mvptree;
%ignore _ph_add_mvptree;
%ignore _ph_query_mvptree;
%ignore ph_getKeyFramesFromVideo;

/* -------------------------- std */


/*
sizeof(off_t) problem :

/usr/include/python2.6/pyconfig.h:1016: 
#define SIZEOF_OFF_T 8

but C/C++ uses 

sys/stat.h:76
typedef __off_t off_t;

unistd.h:244

# ifndef __off_t_defined
#  ifndef __USE_FILE_OFFSET64
typedef __off_t off_t;
#  else
typedef __off64_t off_t;
#  endif
#  define __off_t_defined
# endif
# if defined __USE_LARGEFILE64 && !defined __off64_t_defined
typedef __off64_t off64_t;
#  define __off64_t_defined
# endif


Solution : use AC_SYS_LARGEFILE in pHash configure.ac 

*/

typedef uint64_t off_t;



%module pHash
%{
#include "pHash.h"
%}

//%apply uint64_t { off_t };   
/*
void print_sizeof_off_t();
%{
  void print_sizeof_off_t(){
    printf("sizeof(off_t): %d\n",sizeof(off_t));
  return;
  }
%}
*/


/*
We  declare INPUT and OUTPUT parameters.
Output parameters are not longer args, but part of the return value tuple/sequence. 
*/

//%apply int *OUTPUT { int *rows, int *columns };


DP* ph_malloc_datapoint(int hashtype);
//void ph_free_datapoint(DP *INPUT);
//const char* ph_about();
int ph_radon_projections(const CImg<uint8_t> &INPUT,int N,Projections &OUTPUT);
int ph_feature_vector(const Projections &INPUT,Features &OUTPUT);
int ph_dct(const Features &INPUT, Digest &OUTPUT);
int ph_crosscorr(const Digest &INPUT,const Digest &INPUT,double &INPUT, double threshold = 0.90);
//_ph_image_digest
int ph_image_digest(const char *file, double sigma, double gamma, Digest &OUTPUT,int N=180);
//_ph_compare_images
int ph_compare_images(const char *file1, const char *file2,double &OUTPUT, double sigma = 3.5, double gamma=1.0, int N=180,double threshold=0.90);
//ph_dct_matrix
int ph_dct_imagehash(const char* file,ulong64 &OUTPUT); // TESTED OK
//ph_dct_image_hashes
//ph_getKeyFramesFromVideo
ulong64* ph_dct_videohash(const char *filename, int &OUTPUT);
DP** ph_dct_video_hashes(char *files[], int count, int threads = 0);
double ph_dct_videohash_dist(ulong64 *INPUT, int N1, ulong64 *INPUT, int N2, int threshold=21);
int ph_hamming_distance(const ulong64 hash1,const ulong64 hash2);
DP** ph_read_imagehashes(const char *dirname,int capacity, int &OUTPUT);
uint8_t* ph_mh_imagehash(const char *filename, int &OUTPUT, float alpha=2.0f, float lvl = 1.0f);
int ph_bitcount8(uint8_t val);
double ph_hammingdistance2(uint8_t *INPUT, int lenA, uint8_t *INPUT, int lenB);
//char** ph_readfilenames(const char *dirname,int &OUTPUT);
DP* ph_read_datapoint(MVPFile *INPUT);
int ph_sizeof_dp(DP *INPUT,MVPFile *INPUT);
off_t ph_save_datapoint(DP *INPUT, MVPFile *INPUT);
//_ph_map_mvpfile
//_ph_unmap_mvpfile
float hammingdistance(DP *INPUT, DP *INPUT);
//_ph_query_mvptree
MVPRetCode ph_query_mvptree(MVPFile *INPUT, DP *INPUT, int knearest, float radius, float threshold,   DP **OUTPUT, int &OUTPUT);
//ph_save_mvptree
MVPRetCode ph_save_mvptree(MVPFile *INPUT, DP **INPUT, int nbpoints);
//ph_add_mvptree
MVPRetCode ph_add_mvptree(MVPFile *INPUT, DP **INPUT, int nbpoints, int &OUTPUT);
TxtHashPoint* ph_texthash(const char *filename, int *OUTPUT);
TxtMatch* ph_compare_text_hashes(TxtHashPoint *INPUT, int N1, TxtHashPoint *INPUT, int N2, int *OUTPUT);





/* http://thread.gmane.org/gmane.comp.programming.swig/12746/focus=12747 */
namespace cimg_library {}


/* probleme sur primary-expression */  
%include "pHash.h" 

//%array_class(TxtHashPoint,TxtHashPointArrayIn);
%array_functions(TxtHashPoint,TxtHashPointArray)
%array_functions(TxtMatch,TxtMatchArray)
%array_functions(DP,DPArray)
%array_functions(MVPRetCode,MVPRetCodeArray)


%newobject ph_texthash;

/* from http://www.swig.org/papers/PyTutorial97/PyTutorial97.pdf p75 */
/*
%extend TxtHashPoint {
  TxtHashPoint *__getitem__(int index)  {
      return (self+index);
  }
}

%extend TxtMatch {
  TxtMatch *__getitem__(int index)  {
      return (self+index);
  }
}
*/

%define LISTGETITEM(type)
%extend type {
  type *__getitem__(int index)  {
      return (self+index);
  }
}

%enddef

LISTGETITEM(TxtHashPoint)
LISTGETITEM(TxtMatch)


/*
CHEAT SHEET : void f(double* a, int n)
implicit array lenght, pour eviter le passager de int nbElements

%typemap(python,ignore) int n(int *ptr_n){
   ptr_n=&$target;
}

%typemap(python,in) double *a{
   int i,size;
   *ptr_n=size=PyList_Size($source);
   $target=(double *)malloc(sizeof(double)*size);
   for(i=0;i<size;i++){
      $target[i]=PyFloat_AsDouble(PyList_GetItem($source,i));
   }
}

%typemap(python,freearg) double *a{
   free($source);
}

%inline %{
#include <stdio.h>
void f(double* a, int n)
{
  int i;
  for(i=0;i<n;i++)
    a[i] = (double)i/(double)n;
}
%}

*/

/*
CHEAT SHEET : MyStruct * makeList()

Thoses functions returns a list of struct.
Swig gives us a pointer on the first struct, we need to use pointer function after that...

we can use 
// TxtHashPointArray functions give garbled memory 
//%array_functions(TxtHashPoint,TxtHashPointArray)

// TxtHashPointArrayIn_frompointer give garbled memory too, but easiest too use.
//%array_class(TxtHashPoint,TxtHashPointArrayIn);

//useless
//%pointer_functions(TxtHashPoint,TxtHashPointPtr);

or simply add an %extend to (type * )__get_item__


*/

