#!/usr/bin/python -OO
# -*- coding: iso-8859-15 -*-
#
#
#    pHash, the open source perceptual hash library
#    Copyright (C) 2009 Aetilius, Inc.
#    All rights reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Loic Jaquemet - loic.jaquemet+swig@gmail.com
#

import pHash
import locale,logging,os,sys,time
from os.path import join

def distancefunc(pa,pb):
  # pa.hash is a void * pointer.
  # we need to cast it into ulong64* AND get it's value
  d = pHash.ph_hamming_distance(pHash.ulong64Ptr_value(pHash.voidToULong64(pa.hash)), pHash.ulong64Ptr_value(pHash.voidToULong64(pb.hash)))
  return d


def main(argv):
  '''
  '''
  #locale.setlocale(locale.LC_ALL,'fr_FR')
  #logger=logging.getLogger('root')
  #logger.setLevel(logging.DEBUG)
  #logging.basicConfig(level=logging.INFO)
  logging.basicConfig(level=logging.DEBUG)	
  print pHash.ph_about()

  if (len(argv) < 2):
    print "not enough input args"
    print "usage: %s dirname filename"% (sys.argv[0])
    return -1
  
  dir_name = argv[0] #;/* name of dir to retrieve image files */
  filename = argv[1] #;/* name of file to save db */

  mvpfile= pHash.MVPFile() 
  mvpfile.branchfactor = 2
  mvpfile.pathlength = 5
  mvpfile.leafcapacity = 23 #50
  mvpfile.pgsize = 4096 #8192
  mvpfile.filename = filename
  #mvpfile.hashdist = distancefunc #save: ret code 17
  pHash.my_set_callback(mvpfile,distancefunc)
  mvpfile.hash_type =  pHash.UINT64ARRAY

  nbfiles = 0
  print "dir name: %s"%( dir_name)

  for root, dirs, files in os.walk(dir_name):
    nbfiles=len(files)
    print "nbfiles = %d"% nbfiles
    #allocate a list of nbfiles elements # hashlist = (DP**)malloc(nbfiles*sizeof(DP*));
    hashlist=pHash.DPptrArray(nbfiles)
    count = 0
    for i in range(0,nbfiles):
      filename=os.path.normpath(os.path.join(root,files[i]) )
      # malloc DP or use pHash.DP() // pHash.ph_malloc_datapoint(mvpfile.hash_type)
      #tmp=pHash.ph_malloc_datapoint(mvpfile.hash_type)
      tmp=pHash.DP()
      if (tmp is None):
        print "mem alloc error"
        return -4
      tmp.hash_type = mvpfile.hash_type
      # say to python, to NOT garbage collect DP reference.
      tmp.thisown = 0
      # store the ref.
      hashlist[count]=tmp
      # calculate image hash
      ret,tmphash=pHash.ph_dct_imagehash(filename)
      if ( ret < 0):
        print "unable to get hash"
        continue
      # we can't assign .hash to hashlist[count].hash = tmphash because .hash is a pointer
      # we use ulong64Ptr instead of voidPtr because .. it's a ulong64 ? casting is dynamic
      hashlist[count].hash = pHash.copy_ulong64Ptr(tmphash)
      #
      print "files[%d]: %s hash = %x"%( i, filename, tmphash )
      hashlist[count].id = filename
      hashlist[count].hash_length = 1
      count+=1
  # method with DPptrArray being a DP **
  hashlistf=hashlist.cast()
  ret = pHash.ph_save_mvptree(mvpfile, hashlistf, count)
  # ret 11 is null hash distance function
  # save: ret code 17 has callback func. -> not enought hashdist ?
  print "save: ret code %d"%(ret)
    
  
  #free is done by GC .. ?
  #for i in range(0,nbfiles):
  #  pHash.free(hashlist[i].hash)

  #free is NOT done by GC 
  for i in range(0,nbfiles):
    pHash.ph_free_datapoint(hashlist[i])
  
  #free is done by GC .. ?
  #for i in range(0,nbfiles):
  #  pHash.free(files[i])
  # pHash.free(hashlist)



if __name__ == '__main__':
  main(sys.argv[1:])


