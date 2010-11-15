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

    Evan Klinger - eklinger@phash.org
    David Starkweather - dstarkweather@phash.org
    
    swig interface by Loic Jaquemet - loic.jaquemet@gmail.com

*/
/* 
install swig python-dev CImg-dev & others
see swig autorun automake ... http://realmike.org/python/swig_linux.htm
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

%exception {
	try {
		$function
/*
	} catch(RangeError) {
		SWIG_exception(SWIG_ValueError, "Range Error");
	} catch(DivisionByZero) {
		SWIG_exception(SWIG_DivisionByZero, "Division by zero");
	} catch(OutOfMemory) {
		SWIG_exception(SWIG_MemoryError, "Out of memory");
	*/
	} catch(...) {
		SWIG_exception(SWIG_RuntimeError,"Unknown exception");
	}
}




/* pHash.h n'est pas un header propre pour les lib externes ...
  donc on fait pHashLib.h 
*/


%ignore ph_dct;
%ignore ph_dct_matrix;
%ignore _ph_save_mvptree;
%ignore _ph_add_mvptree;
%ignore _ph_query_mvptree;
%ignore ph_getKeyFramesFromVideo;

/* -------------------------- std */

typedef uint32_t off_t;

//KO typedef uint64t ulong64;
//typedef  unsigned int ulong64;

//%apply uint32_t { off_t };   

//%apply uint64_t { ulong64 };   


%module pHash
%{
#include "pHash.h"

%}

/*
typedef struct ph_hash_point {
    ulong64 hash;
    off_t index; 
} TxtHashPoint;

typedef struct ph_match{
    off_t first_index; 
    off_t second_index;
    uint32_t length;   
} TxtMatch;

*/

/*

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
We  declare INPUT and OUTPUT parameters.
Output parameters are not longer args, but part of the return value tuple/sequence. 
*/

//%apply int *OUTPUT { int *rows, int *columns };


int ph_radon_projections(const CImg<uint8_t> &INPUT,int N,Projections &OUTPUT);
int ph_feature_vector(const Projections &INPUT,Features &OUTPUT);
int ph_dct(const Features &INPUT, Digest &OUTPUT);
int ph_crosscorr(const Digest &INPUT,const Digest &INPUT,double &INPUT, double threshold = 0.90);
int _ph_image_digest(const CImg<uint8_t> &INPUT,double sigma, double gamma,Digest &OUTPUT,int N=180);
int ph_image_digest(const char *file, double sigma, double gamma, Digest &OUTPUT,int N=180);
int ph_compare_images(const char *file1, const char *file2,double &OUTPUT, double sigma = 3.5, double gamma=1.0, int N=180,double threshold=0.90);
// TESTED OK
int ph_dct_imagehash(const char* file,ulong64 &OUTPUT);
int ph_sizeof_dp(DP *INPUT,MVPFile *INPUT);
double ph_dct_videohash_dist(ulong64 *INPUT, int N1, ulong64 *INPUT, int N2, int threshold=21);
double ph_hammingdistance2(uint8_t *INPUT, int lenA, uint8_t *INPUT, int lenB);
float hammingdistance(DP *INPUT, DP *INPUT);
MVPRetCode ph_query_mvptree(MVPFile *INPUT, DP *INPUT, int knearest, float radius,
		float threshold,   DP **OUTPUT, int &OUTPUT);
MVPRetCode ph_save_mvptree(MVPFile *INPUT, DP **INPUT, int nbpoints);
MVPRetCode ph_add_mvptree(MVPFile *INPUT, DP **INPUT, int nbpoints, int &OUTPUT);
off_t ph_save_datapoint(DP *INPUT, MVPFile *INPUT);




/*
Thoses functions returns a list of struct.
Swig gives us a pointer on the first struct, we need to use pointer function after that...
cf %array_functions(type,name)

with an OUTPUT arg, it's a tuple :

Python :
>>> ( Proxy Class, nbvalue) = pHash.ph_texthash(filename)

I can't find a way to make that into a swig list of some sort ...

typemap(out0) type*... impacts the pointer constructor... no good.

/*
%typemap(out) TxtMatch * {
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
you can specify the function name for the typemap

http://thread.gmane.org/gmane.comp.programming.swig/12727/focus=12729

we can have different typemaps
*/

//%typemap(out, null="NULL") TxtHashPoint * TxtHashPoint %{ $result = $1; %}

/* we just have to find a way to make a PyObject from a TxtHashPoint  
SWIG_NewPointerObj(SWIG_as_voidptr(p_data), SWIGTYPE_p_tMyStruct, SWIG_SHADOW)
http://old.nabble.com/C-%3EPerl-%3A-converting-C-array-into-perl-string.-td26642428.html

http://permalink.gmane.org/gmane.comp.programming.swig/16209

*/

/*
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
*/

/*
trying with a helper function...
%{

void ph_texthash_List(const char *filename, TxtHashPoint* list, int *nb ){
    TxtHashPoint * ret=0;
    ret=ph_texthash(filename, nb);
    list=ret;
    //return ret;
    return;
}

%}


//void ph_texthash_List(const char *filename, int *OUTPUT);
//TxtHashPoint[] ph_texthash_List(const char *filename, int *OUTPUT);
void ph_texthash_List(const char *filename, TxtHashPoint* OUTPUT, int *OUTPUT );
*/

/*
The easiest way should be to write a full Class aroud thoses...
*/



// TxtHashPointArray functions give garbled memory 
%array_functions(TxtHashPoint,TxtHashPointArray)
//%array_functions(TxtMatch,TxtMatchArray)

// TxtHashPointArrayIn_frompointer give garbled memory too, but easiest too use.
%array_class(TxtHashPoint,TxtHashPointArrayIn);
//%array_class(TxtMatch,TxtMatchArray);

//useless
%pointer_functions(TxtHashPoint,TxtHashPointPtr);

%newobject ph_texthash;

TxtHashPoint* ph_texthash(const char *filename, int *OUTPUT);
TxtMatch* ph_compare_text_hashes(TxtHashPoint *INPUT, int N1, TxtHashPoint *INPUT, int N2, int *OUTPUT);


//%typemap(out) TxtHashPoint * ;
%clear TxtHashPoint * ;


/* todo */
ulong64* ph_dct_videohash(const char *filename, int &OUTPUT);
DP** ph_read_imagehashes(const char *dirname,int capacity, int &OUTPUT);
uint8_t* ph_mh_imagehash(const char *filename, int &OUTPUT, float alpha=2.0f, float lvl = 1.0f);
char** ph_readfilenames(const char *dirname,int &OUTPUT);
DP* ph_read_datapoint(MVPFile *INPUT);


/* http://thread.gmane.org/gmane.comp.programming.swig/12746/focus=12747 */
namespace cimg_library {}


/* probleme sur primary-expression */  
%include "pHash.h" 




