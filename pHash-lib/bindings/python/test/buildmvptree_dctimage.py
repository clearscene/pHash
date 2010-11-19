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
#    Evan Klinger - eklinger@phash.org
#    D Grant Starkweather - dstarkweather@phash.org
#

import pHash
import locale,logging,os,sys,time
from os.path import join, getsize

def distancefunc(pa,pb):
    d = pHash.ph_hamming_distance(pa.hash, pb.hash)
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
  mvpfile.leafcapacity = 50
  mvpfile.pgsize = 8192
  mvpfile.filename = filename
  #mvpfile.hashdist = distancefunc
  mvpfile.hash_type =  pHash.UINT64ARRAY

  nbfiles = 0
  print "dir name: %s"%( dir_name)

  for root, dirs, files in os.walk(dir_name):
    root
    nbfiles=len(files)
    print "nbfiles = %d"% nbfiles
    #allocate a list of nbfiles elements # hashlist = (DP**)malloc(nbfiles*sizeof(DP*));
    hashlist=list() 
    count = 0
    for i in range(0,nbfiles):
      hashlist.append(pHash.ph_malloc_datapoint(mvpfile.hash_type))
      if (hashlist[count] is None):
        print "mem alloc error"
        return -4
      
      # who is responsible for alloc/dealloc of hash ?
      # why is hash a void * ?
      #hashlist[count].hash = malloc(sizeof(ulong64));
      
      # if hash wasn't a pointer, code would be easier ?:
      #ret,hashlist[count].hash=pHash.ph_dct_imagehash(os.path.join(root,files[i]) )
      #if ( ret < 0):
      #  print "unable to get hash"
      #  continue
      #print "files[%d]: %s hash = %X"%( i, os.path.join(root,files[i]), hashlist[count].hash )
      
      # we need to fight with pointer and cast...
      # tmphash is the hash value, not the hash pointer
      ret,tmphash=pHash.ph_dct_imagehash(os.path.join(root,files[i]))
      # we need 
      hashlist[count].hash=pHash.copy_ulong64Ptr(tmphash)
      if ( ret < 0):
        print "unable to get hash"
        continue
      # working solution, 
      hashval=pHash.ulong64Ptr_value(hashlist[count].hash)
      print "files[%d]: %s hash = %x"%( i, os.path.join(root,files[i]), hashval )
      hashlist[count].id = os.path.join(root,files[i])
      hashlist[count].hash_length = 1
      count+=1
  #
  ret = pHash.ph_save_mvptree(mvpfile, hashlist, count)
  print "save: ret code %d"%(ret)

  for i in range(0,nbfiles):
    pHash.ph_free_datapoint(hashlist[i])

#  for (int i=0;i<nbfiles;i++){
#	  free(files[i]);
#    }
#    free(files);
#
#    for (int i=0;i<nbfiles;i++){
#	free(hashlist[i]->hash);
#	ph_free_datapoint(hashlist[i]);
#    }
#    free(hashlist);
#
#    return 0;
#}



if __name__ == '__main__':
  main(sys.argv[1:])


