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


def main(argv):
  '''
  '''
  logging.basicConfig(level=logging.DEBUG)
	
  print pHash.ph_about()

  if (len(argv) < 2):
	  print "not enough input arguments"
	  return -1
  
  file1 = argv[0]
  file2t = argv[1]
  file2 = file2t

  print "file1=%s"%( file1)
  ret = pHash.ph_dct_videohash(file1)
  if (type(ret) is int ):
    return 2
  hash1,L1=ret 
  hash1=pHash.ulong64Array.frompointer(hash1)
  
  print "length %d"%( L1)
  for i in range(0,L1):
     print "hash1[%d]=%x"%( i, hash1[i])

  while (file2 != "exit" ):    
    print "file=%s"%( file2)
    ret = pHash.ph_dct_videohash(file2)
    if (type(ret) is int  ):
      return 3
    hash2,L2=ret 
    hash2=pHash.ulong64Array.frompointer(hash2)

    print "length %d"%( L2)

    sim = pHash.ph_dct_videohash_dist(hash1.cast(), L1, hash2.cast(), L2, 21)
    print "similarity %f"%( sim)

    del hash2
    hash2 = None

    file2 = sys.stdin.readline()

  del hash1
  del hash2
  hash1 = None
  hash2 = None
  file2 = None       
  print "done"
  return 0



 
if __name__ == '__main__':
  main(sys.argv[1:])


