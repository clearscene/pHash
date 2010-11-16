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




*/

// typedef need to be defined, not in std typemaps.i
//typedef uint64_t off_t;
//typedef __off64_t off_t;
typedef uint32_t off_t;

// NEED TO FORCE off_t to uint32 ... see config.h

/*
//%apply uint32_t { off_t };   



typedef struct ph_hash_point {
    ulong64 hash;
    off_t index; 
} TxtHashPoint;

*/



%module pHash
%{

//typedef uint64_t off_t;
//typedef __off64_t off_t;


#include "pHash.h"
%}

/*
%typemap(memberin) off_t {
    if (PyLong_Check($input))
        //$1 = (unsigned long) PyLong_AsLongLong($input);
        $1 = (long long) PyLong_AsLongLong($input);
    else if (PyInt_Check($input))
        //$1 = (unsigned long) PyInt_AsLong($input);
        $1 = (long long) PyInt_AsLongLong($input);
 	
 }
*/

%typemap(out) off_t {
    PyObject *o = PyInt_FromLong($1);
    $result = o;
 }


%apply uint32_t { off_t };   
//%apply uint64_t { off_t };   

void print_sizeof_off_t();
%{
  void print_sizeof_off_t(){
    printf("sizeof(off_t): %d\n",sizeof(off_t));
  return;
  }
%}

/*
PROOF that SWIg messes up C memory....
*/
/*
%typemap(out) TxtHashPoint * ph_texthash {
    PyObject *list = PyList_New(*arg2);
    int i =0;
    printf("arg5 value is %d\n",*arg2);
    printf("$1 is %x\nsizeof(off_t): %d\n",$1,sizeof(off_t));
    TxtHashPoint * ptri=$1;
    for(i=0; i< *arg2; i++ ) {
      //  PyList_Append(list,$1[i]);
      //swig_o=SWIG_NewPointerObj(SWIG_as_voidptr($1[i]), SWIGTYPE_p_tTxtHashPoint, SWIG_SHADOW)
		  //PyList_SetItem(list,i, list) ;//(PyObject *) $1[i]);
		  //PyList_SetItem(list,i, swig_o ) ;
      //TxtHashPoint *ptr=($1+i);
      //printf("typemap C/hash+index: %lld %lld\n",ptr->hash,ptr->index );
      TxtHashPoint ptr=ptri[i];
      printf("typemap C/hash+index: %lld %lld\n",ptr.hash,ptr.index );
		}
    $result=list;
}
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



%newobject ph_texthash;

/* from http://www.swig.org/papers/PyTutorial97/PyTutorial97.pdf p75 */
%extend TxtHashPoint {
  TxtHashPoint *__getitem__(int index)  {
      return (self+index);
  }

  void printme()  {
      TxtHashPoint *ptr=(self);
      printf("C/hash+index: %lld %lld\n",ptr->hash,ptr->index );
      return;
  }
  void printptr(int index)  {
      TxtHashPoint *ptr=(self+index);
      printf("C/hash+index: %lld %lld\n",ptr->hash,ptr->index );
      return;
  }
}


%extend TxtMatch {
  TxtMatch *__getitem__(int index)  {
      return (self+index);
  }
}




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


or simply add an extend to (type * )__get_item__

with an OUTPUT arg, it's a tuple :

Python :
>>> ( Proxy Class, nbvalue) = pHash.ph_texthash(filename)


OR using TYPEMAP(out)
I can't find a way to make that into a swig list of some sort ...
we need to cast the pointer in a PyObject ???

you can specify the function name for the typemap
http://thread.gmane.org/gmane.comp.programming.swig/12727/focus=12729

%typemap(out) TxtMatch * myfunc{
    PyObject *list = PyList_New(*arg5);
    int i =0;
    printf("arg5 value is %d\n",*arg5);
    for(i=0; i< *arg5; i++ ) {
      //PyList_Append(list,$1[i]);
		  PyList_SetItem(list,i, *** Object $1[i]);
		}
    $result=list;
}
*/


/* 
we just have to find a way to make a PyObject from a TxtHashPoint  
SWIG_NewPointerObj(SWIG_as_voidptr(p_data), SWIGTYPE_p_tMyStruct, SWIG_SHADOW)
http://old.nabble.com/C-%3EPerl-%3A-converting-C-array-into-perl-string.-td26642428.html

http://permalink.gmane.org/gmane.comp.programming.swig/16209

%typemap(out) TxtHashPoint * ph_texthash {
    PyObject *list = PyList_New(*arg2);
    int i =0;
    printf("arg5 value is %d\n",*arg2);
    for(i=0; i< *arg2; i++ ) {
      //  PyList_Append(list,$1[i]);
      swig_o=SWIG_NewPointerObj(SWIG_as_voidptr($1[i]), SWIGTYPE_p_tTxtHashPoint, SWIG_SHADOW)
		  //PyList_SetItem(list,i, list) ;//(PyObject *) $1[i]);
		  PyList_SetItem(list,i, swig_o ) ;

		}
    $result=list;
}

[..]

//%typemap(out) TxtHashPoint * ;
//%clear TxtHashPoint * ;

*/


