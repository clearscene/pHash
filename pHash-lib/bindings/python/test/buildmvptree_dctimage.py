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
    #array_class
    hashlist=pHash.DPClass(nbfiles)
    count = 0
    for i in range(0,nbfiles):
      #hashlist.append(pHash.ph_malloc_datapoint(mvpfile.hash_type))
      dp=pHash.ph_malloc_datapoint(mvpfile.hash_type)
      if (dp is None):
        print "mem alloc error"
        return -4
      
      ret,tmphash=pHash.ph_dct_imagehash(os.path.join(root,files[i]))
      if ( ret < 0):
        print "unable to get hash"
        continue
      # malloc dp.hash
      dp.hash=pHash.copy_ulong64Ptr(tmphash)
      # assign dp to DPClass array.
      hashlist[count]=dp
      
      #pHash.DPPtrArray_setitem(hashlist,count,pHash.ph_malloc_datapoint(mvpfile.hash_type))
      #if (pHash.DPPtrArray_getitem(hashlist,count) is None):
      #  print "mem alloc error"
      #  return -4
      
      # who is responsible for alloc/dealloc of hash ?
      # why is hash a void * ?
      #hashlist[count].hash = malloc(sizeof(ulong64));
      #hashlist[count].hash = pHash.new_ulong64Ptr();
      #cc=pHash.ulong64Class()
      
      #hashlist[count].hash = cc.cast() 
      #print 'hashlist[count].hash 1',hashlist[count].hash
      # if hash wasn't a pointer, code would be easier ?:
      #ret,hashlist[count].hash=pHash.ph_dct_imagehash(os.path.join(root,files[i]) )
      #if ( ret < 0):
      #  print "unable to get hash"
      #  continue
      #print "files[%d]: %s hash = %X"%( i, os.path.join(root,files[i]), hashlist[count].hash )
      
      # we need to fight with pointer and cast...
      # tmphash is the hash value, not the hash pointer
      ret,tmphash=pHash.ph_dct_imagehash(os.path.join(root,files[i]))
      #print 'post dct',tmphash
      
      #print 'hashlist[count].hash 3',hashlist[count].hash
      #hashlist[count]=dp
      #cc.assign(tmphash)
      #print 'cc',cc.value()
      #print 'hashlist[count].hash 5',hashlist[count].hash
      #hashlist[count].hash=cc.cast()
      #print 'hashlist[count].hash 10',hashlist[count].hash
      # we need 
      #hashlist[count].hash=pHash.copy_ulong64Ptr(tmphash)
      #print 'hashlist[count].hash 15',hashlist[count].hash

      dp=hashlist[count]
      #print 'dp.hash 1', dp.hash      
      # OK 
      dp.hash=pHash.copy_ulong64Ptr(tmphash)
      #print 'dp.hash 5', dp.hash , 'hashlist[count].hash ',hashlist[count].hash
      hashlist[count]=dp
      print 'hashlist[count].hash 6 ',hashlist[count].hash

      #hashlist[count].hash=pHash.copy_ulong64Ptr(tmphash)
      #print 'hashlist[count].hash ',hashlist[count].hash

      #hashlist[count].hash=pHash.new_ulong64Ptr()
      #print 'dp.hash 7', dp.hash , 'hashlist[count].hash ',hashlist[count].hash            
      #pHash.ulong64Ptr_assign(hashlist[count].hash,tmphash)
      #print 'dp.hash 10', dp.hash, 'hashlist[count].hash ',hashlist[count].hash



      if ( ret < 0):
        print "unable to get hash"
        continue
      #print 'END hashlist[count] ' ,  hashlist[count]
      #print 'hashval ' ,  hashlist[count].hash
      # working solution, 
      hashval=pHash.ulong64Ptr_value(hashlist[count].hash)
      #print 'post value'
      print "files[%d]: %s hash = %x"%( i, os.path.join(root,files[i]), hashval )
      hashlist[count].id = os.path.join(root,files[i])
      hashlist[count].hash_length = 1
      count+=1
  #
  print 'hashlist',hashlist
  print 'hashlist',hashlist.cast()
  ret = pHash.ph_save_mvptree(mvpfile, hashlist[0], count)
  #ret = pHash.ph_save_mvptree(mvpfile, hashlist.cast(), count)
  #ret = pHash.ph_save_mvptree(mvpfile, hashlist, count)
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


