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
#    but WITHOUT ANY WARRANTY without even the implied warranty of
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
  logging.basicConfig(level=logging.DEBUG)
  
  print pHash.ph_about()

  if (len(argv) < 2):
    print "not enough input arguments"
    print "usage: %s directory dbname [radius] [knearest] [threshold]"%( sys.argv[0])
    return -1

  dir_name = argv[0]#/* name of files in directory of query images */
  filename = argv[1]#/* name of file to save db */

  mvpfile=pHash.MVPFile()
  mvpfile.filename = filename
  pHash.my_set_callback(mvpfile,distancefunc)  
  mvpfile.hash_type = pHash.UINT64ARRAY

  nbfiles = 0
  print "dir name: %s"%( dir_name)
  ret = pHash.ph_readfilenames(dir_name)
  if (type(ret) is int):
    print "unable to read files from directory"
    return -2
  (tmpfiles,nbfiles)=ret
  files=pHash.charPtrArray.frompointer(tmpfiles)
  print "nbfiles = %d"%( nbfiles)

  #allocate a list of nbfiles elements # hashlist = (DP**)malloc(nbfiles*sizeof(DP*));
  hashlist=pHash.DPptrArray(nbfiles)
  if ( hashlist is None):
    print "mem alloc error"
    return -3
  
  count=0
  tmphash=0x00000000
  for i in range(0,nbfiles):
    tmpdp=pHash.ph_malloc_datapoint(mvpfile.hash_type)
    if (tmpdp is None):
      print "mem alloc error"
      return -4
    tmpdp.thisown=0
    hashlist[count]=tmpdp
    
    #useless malloc, we use copy_
    #hashlist[count].hash=pHash.new_ulong64Ptr()
    #if (hashlist[count].hash is None):
    #  print "mem alloc error"
    #  return -5

    print "file[%d] = %s"%( i, files[i])        
    ret=pHash.ph_dct_imagehash(files[i])
    if (type(ret) is int):
      print "unable to get hash"
      hashlist[count].hash=None
      phash.ph_free_datapoint(hashlist[count])
      continue
    (res,tmphash)=ret

    hashlist[count].id = files[i]
    hashlist[count].hash=pHash.copy_ulong64Ptr(tmphash)
    hashlist[count].hash_length = 1
    count+=1
  #

  print "add files to file %s"%(filename)
  nbsaved=0
  ret = pHash.ph_add_mvptree(mvpfile, hashlist.cast(), count)
  if (type(ret) is int):
    print "error on ph_add_mvptree"
    return -6
  (res,nbsaved)=ret
  print "number saved %d out of %d, ret code %d"%( nbsaved,count,res)

  # freeeee. we need to add %newobject to ph_readfilesnames
  #for i in range(0,nbfiles):
  #  free(files[i])
  #
  files=None

  for i in range(0,nbfiles):
    hashlist[i].hash = None
    pHash.ph_free_datapoint(hashlist[i])
  
  hashlist=None

  return 0






if __name__ == '__main__':
  main(sys.argv[1:])

