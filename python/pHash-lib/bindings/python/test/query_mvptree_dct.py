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

nb_calcs=0

def distancefunc(pa,pb):
  global nb_calcs
  nb_calcs+=1
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
  #@TODO
  #mvpfile.hashdist = distancefunc
  #mvpfile.hashdist = distancefunc #save: ret code 17
  pHash.my_set_callback(mvpfile,distancefunc)  
  mvpfile.hash_type = pHash.UINT64ARRAY

  nbfiles = 0
  print "using db %s"%( filename)
  print "using dir %s for query files"%( dir_name)
  nbfiles = 0
  print "dir name: %s"%( dir_name)
  nbfiles=0
  files=None
  for root, dirs, filest in os.walk(dir_name):
    nbfiles=len(filest)
    files=[os.path.join(root,f) for f in filest]
  files.sort()
  print "nb query files = %d"%( nbfiles)


  #DP *query = pHash.ph_malloc_datapoint(mvpfile.hash_type)
  query=pHash.ph_malloc_datapoint(mvpfile.hash_type)
  if (query is None):
    print "mem alloc error"
    return -3
  query.thisown=0

  argc=len(argv)+1
  radius = 30.0
  threshold = 15.0
  knearest = 20
  if (argc >= 4):
    radius = float(argv[3])
  
  if (argc >= 5):
    knearest = int(argv[4])
  
  if (argc >= 6):
      threshold = float(argv[5])
  
  print "radius = %f"%( radius)
  print "knearest = %d"%( knearest)
  print "threshold = %f"%( threshold)

  # malloc
  results = pHash.DPptrArray(knearest)
  if (results is None):
    return -3
  
  tmphash = 0x0000000000000000
  nbfound = 0
  count = 0
  sum_calcs = 0
  for i in range(0,nbfiles):
    ret=pHash.ph_dct_imagehash(files[i]) 
    if (type(ret) is int):
      print "unable to get hash"
      continue
    ret2,tmphash=ret

    print "query[%d]: %s %x"%( i, files[i], tmphash)
    query.id = files[i]
    query.hash = pHash.copy_ulong64Ptr(tmphash)
    query.hash_length = 1

    global nb_calcs
    nb_calcs = 0
    nbfound = 0
    ret = pHash.ph_query_mvptree(mvpfile,query,knearest,radius,threshold,results.cast())
    if (type(ret) is int ):
      print "could not complete query, %d"%(retcode)
      continue
    #print 'pHash.ph_query_mvptree',ret 
    # results DP **   
    retcode,nbfound = ret
    #print 'errcodes : pHash.PH_ERRCAP ',pHash.PH_ERRCAP
    if (retcode != pHash.PH_SUCCESS and retcode != pHash.PH_ERRCAP):
      print "could not complete query, %d"%(retcode)
      continue
    count+=1
    sum_calcs += nb_calcs
  
    print " %d files found"%( nbfound)
    for j in range (0,nbfound):
      d = distancefunc(query, results[j])
      print " %d  %s distance = %f"%( j, results[j].id, d)

    print "nb distance calcs: %d"%( nb_calcs)
    for j in range(0,nbfound):
      #free(results[j]->id)
      #del results[j].id
      results[j].id = None
      #del results[j].hash
      results[j].hash = None
      pHash.ph_free_datapoint(results[j])
    
  #end for i


  ave_calcs = float(sum_calcs)/float(count)      
  print "ave calcs/query: %f"%( ave_calcs)


  #for i in range (0, nbfiles):
  #  del files[i]

  del files

  pHash.ph_free_datapoint(query)
  del results
  #del mvpfile.filename

  return 0



if __name__ == '__main__':
  main(sys.argv[1:])

