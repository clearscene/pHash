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

%module pHash
%{
#include "pHashLib.h"

%}

/* Create some functions for working with "double *" */
%pointer_functions(double, doublep);

/* Create some functions for working with "int *" */
%pointer_functions(int, intp);
%pointer_functions(uint64_t, uint64_tp);
%pointer_functions(ulong64, ulong64p);

/* functions pour ph_digest & Digest */
%pointer_functions(uint8_t, uint8_tp);
%array_functions(uint8_t,uint8_tArray);
%free(uint8_t);



/* http://thread.gmane.org/gmane.comp.programming.swig/12746/focus=12747 */
namespace cimg_library {}

/* %ignore mvptag; */

/* %include "pHash2.h" */

/* p^robleme sur primary-expression */  
%include "pHashLib.h" 

/* typedef unsigned _uint64 ulong64; */
//typedef unsigned long long ulong64;


//extern "C" const char* ph_about();

/* double & :   http://www.mail-archive.com/python_inside_maya@googlegroups.com/msg01767.html 
http://download.autodesk.com/us/maya/2009help/API/class_m_script_util.html
http://www.swig.org/Doc1.3/Python.html#Python_nn47
*/

//extern "C" int ph_compare_images(const char *file1, const char *file2,double &pcc, double sigma = 3.5, double gamma=1.0, int N=180,double threshold=0.90);



/* %ignore ph_mvp_init(MVPFile *); */

/*


*/

