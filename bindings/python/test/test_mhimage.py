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
#    but WITHOUT ANY WARRANTY   without even the implied warranty of
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


#using namespace cimg_library  

#names.sort() ....
def sort_names(names, L1):
  #
  _min=None
  #print names
  for i in range(0,L1):
    _min = i
    for j in range(i+1,L1):
      if ( len(names[j]) < len(names[_min]) ):
        _min = j
      if (i != _min):
        swap = names[i]  
        names[i] = names[_min]  
        names[_min] = swap  
    #
  #
  return names


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
  
  dirname1 = argv[0] # weird bug in ph_readfilenames ? /* name of dir to retrieve image files */
  dirname2 = argv[1] #  /* name of file to save db */

  alpha = 2  
  level = 1  

  nbfiles1=0
  files1=None
  for root, dirs, files in os.walk(dirname1):
    nbfiles1=len(files)
    files1=[os.path.join(root,f) for f in files]
  files1.sort()
  #nbfiles1=0
  #ret = pHash.my_ph_readfilenames(dirname1) 
  #if (ret is None):
  #  print "unable to read files from directory",dirname1
  #  return -2
  #if (type(ret) is int):
  #  print "unable to read files from directory",dirname1
  #  return -2
  #print ret
  #(tmpfiles1,nbfiles1)=ret
  #files1=pHash.charPtrArray.frompointer(tmpfiles1)
  #files1=sort_names(files1,nbfiles1)
  #list(files1)
  #print files1

  nbfiles2=0
  files2=None
  for root, dirs, files in os.walk(dirname2):
    nbfiles2=len(files)
    files2=[os.path.join(root,f) for f in files]
  files2.sort()

  if (nbfiles1 != nbfiles2):
    print "number files in both directories not equal"  
    return 1

  #uint8_t **hash1 = (uint8_t**)malloc(nbfiles1*sizeof(uint8_t*))  
  hash1=pHash.uint8_tPtrPtrArray(nbfiles1)
  hash2 = 0  
  hashlen1=0
  hashlen2=0  
  dist = 0  
  print "intra distances"  
  print "***************" 
  for i in range(0,nbfiles1):
    print "file1: %s" %(files1[i])
    ret = pHash.ph_mh_imagehash(files1[i], alpha, level)  
    if (type(ret) is int):
      continue  
    (hash1[i],hashlen1)=ret

    f2=files2[i]
    print "file2: %s"%(files2[i])  
    ret = pHash.ph_mh_imagehash(files2[i], alpha, level)  
    if (type(ret) is int):
      continue  
    (hash2,hashlen2)=ret

    dist = pHash.ph_hammingdistance2(hash1[i], hashlen1, hash2, hashlen2)  
    print "distance = %f"%( dist)  
    print "-------------"  
    hash2=None
  
  print "\n"
  print "--hit any key--"  
  sys.stdin.readline()
  print "inter distances"  
  for i in range(0,nbfiles1):
    for j in range(i+1,nbfiles1):
      dist = pHash.ph_hammingdistance2(hash1[i], hashlen1, hash1[j], hashlen1)  
      print " %d %d dist = %f"%( i, j, dist)  
      print "----------------"  
    
  
  print "done"

  for i in range(0,nbfiles1):
    files1[i]=None
    files2[i]=None
    hash1[i]=None
  
  files1=None
  files2=None  
  hash1=None
  return 0




if __name__ == '__main__':
  main(sys.argv[1:])


