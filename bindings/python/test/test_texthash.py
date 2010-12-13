#!/usr/bin/python -OO
# -*- coding: iso-8859-15 -*-

#
#    pHash, the open source perceptual hash library
#    Copyright (C) 2009 Aetilius, Inc.
#    All rights reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Loic Jaquemet - loic.jaquemet+phash@gmail.com
#

import pHash
import locale,logging,os,sys,time



def main(argv):
  '''
  '''
  #locale.setlocale(locale.LC_ALL,'fr_FR')
  #logger=logging.getLogger('root')
  #logger.setLevel(logging.DEBUG)
  #logging.basicConfig(level=logging.INFO)
  logging.basicConfig(level=logging.DEBUG)
	
  print pHash.ph_about()
  
  if(len(argv)<2):
    print "not enough input args" 
    return
 
  try:
    file1 = argv[0]
    file2 = argv[1]

    # new style
    print "file1: %s" %(file1)
    res=pHash.ph_texthash(file1)
    if type(res) is int  :
      print 'err: return args:', res
      return None
    (h1,nb1)=res
    print "length %d"%(nb1)

    print "file2: %s" %(file2)
    res=pHash.ph_texthash(file2)
    if type(res) is int  :
      print 'err: return args:', res
      return None
    (h2,nb2)=res
    print "length %d"%(nb2)

    # LISTITEM template doesnt work !
    res=pHash.ph_compare_text_hashes(h1,nb1,h2,nb2)
    if type(res) is int :
      print "unable to complete compare function"
      return
    (matches2,count)=res
    # we use a Array wrapper for single pointer
    matches=pHash.TxtMatchArray.frompointer(matches2)

    print " %d matches"%(count)
    print " indxA  indxB  length"
    for j in range(0,count,1):
      # off_t is lld in C code ....
      print " %d %d %d"%( matches[j].first_index, matches[j].second_index,matches[j].length) 
    return 
  except Exception,e:
    print e


if __name__ == '__main__':
  main(sys.argv[1:])



