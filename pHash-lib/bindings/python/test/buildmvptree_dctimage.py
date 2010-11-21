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
    print ': distancefunc a.hash',pa.hash, pHash.ulong64Ptr_value(pb.hash)
    #d = pHash.ph_hamming_distance(pHash.copy_ulong64Ptr(pa.hash), pHash.copy_ulong64Ptr(pb.hash))
    d = pHash.ph_hamming_distance(pHash.ulong64Ptr_value(pa.hash), pHash.ulong64Ptr_value(pb.hash))
    #d = pHash.ph_hamming_distance(pa.hash, pb.hash)
    print "%d = distancefunc %s %s"%(d,pa.this,pb.this)
    return d

# if you dont keep ref to mall.this or to mall, it's garbaged..
# if it's garbaged, malloc will realloc
def test():
  print pHash.UINT64ARRAY
  l=[]
  for i in range(0,10):
    mall=pHash.ph_malloc_datapoint(pHash.UINT64ARRAY)
    t=mall.this
    print '%s'%(t)
    #l.append(t)
    l.append(mall)
#idem than malloc
def test2():
  l=[]
  for i in range(0,10):
    mall=pHash.DP()
    t=mall.this
    print '%s'%(t)
    #l.append(t)
    #l.append(mall)

def test3():
  l1=[]
  l=pHash.DPArray(10)
  for i in range(0,10):
    mall=pHash.DP()
    t=mall.this
    print '%s'%(t)
    l[i]=t
    l1.append(t)
  print 'Malloc or changed car python list retain ref. DPArray doesnt.'
  print 'worse, DPArray is fully bloated'
  print "%s"%(l[0].this)
  print "%s"%(l[3].this)

def test4():
  l1=[]
  #l=pHash.DPptrArray(10)
  l=pHash.DPArray(10)
  ret,tmphash=pHash.ph_dct_imagehash('')
  for i in range(0,10):
    mall=pHash.DP()
    t=mall.this
    print '%s'%(t)
    l[i]=mall
    l1.append(mall)
    l[i].hash = pHash.copy_ulong64Ptr(tmphash)
    l[i].id = 'plpopl,psk'
    l[i].hash_length = 1
    print "files[%d]: %s hashlist[i] :%s hash = %x"%( i, l[i].id, l[i] ,l[i].hash )

  print 'Malloc or changed car python list retain ref. DPArrayPtr doesnt.'
  print 'BUT DPptr Array is OK'
  for i in range(0,10):
    print "%s"%(l[i].this)


def main(argv):
  '''
  '''
  #locale.setlocale(locale.LC_ALL,'fr_FR')
  #logger=logging.getLogger('root')
  #logger.setLevel(logging.DEBUG)
  #logging.basicConfig(level=logging.INFO)
  logging.basicConfig(level=logging.DEBUG)	
  print pHash.ph_about()

  debug=False

  #test4()
  #return

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
  # @TODO
  #mvpfile.hashdist = distancefunc #save: ret code 17
  pHash.my_set_callback(mvpfile,distancefunc)
  mvpfile.hash_type =  pHash.UINT64ARRAY

  nbfiles = 0
  print "dir name: %s"%( dir_name)

  for root, dirs, files in os.walk(dir_name):
    nbfiles=len(files)
    print "nbfiles = %d"% nbfiles
    #allocate a list of nbfiles elements # hashlist = (DP**)malloc(nbfiles*sizeof(DP*));
    #array_class - malloc hashlist
    #hashlist=list() 
    hashlist=pHash.DPArray(nbfiles)
    l=[]
    count = 0
    if ( not debug):
      for i in range(0,nbfiles):
        filename=os.path.normpath(os.path.join(root,files[i]) )
        # malloc DP or use pHash.DP()
        tmp=pHash.DP()
        hashlist[count]=tmp
        #hashlist[count]=pHash.ph_malloc_datapoint(mvpfile.hash_type)
        if (hashlist[count] is None):
          print "mem alloc error"
          return -4
        #print 'debug'
        ret,tmphash=pHash.ph_dct_imagehash(filename)
        if ( ret < 0):
          print "unable to get hash"
          continue

        # we can't assign .hash to hashlist[count].hash = tmphash because .hash is a pointer
        # malloc .hash
        # we use ulong64Ptr instead of voidPtr because .. it's a ulong64 ?
        hashlist[count].hash = pHash.copy_ulong64Ptr(tmphash)
        
        print "files[%d]: %s hash = %x"%( i, filename, tmphash )
        hashlist[count].id = filename
        hashlist[count].hash_length = 1
        count+=1
        l.append(tmp)
     #
    if debug :
      #debug
      count=0
      ret,tmphash=pHash.ph_dct_imagehash('plop/5108884.jpg')
      l=[]
      for i in range(0,nbfiles):
        #hashlist[count]=pHash.ph_malloc_datapoint(mvpfile.hash_type)
        tmp=pHash.DP()
        hashlist[count]=tmp
        hashlist[count].hash_type=mvpfile.hash_type
        if (hashlist[count] is None):
          print "mem alloc error"
          return -4
        tmphash+=1
        #tmphash=pHash.new_ulong64Ptr()
        #tmphash=pHash.ulong64Ptr_assign(tmphash,0x591e67a59696b449)
        hashlist[count].hash = pHash.copy_ulong64Ptr(tmphash)
        #hashlist[count].hash = tmphash
        #print '@',pHash.ulong64Ptr_value(pHash.copy_ulong64Ptr(tmphash))
        #print "files[%d]: %s hashlist[i] :%s hash = %x"%( i, filename, hashlist[i].this ,tmphash )
        hashlist[count].id = filename
        hashlist[count].hash_length = 1
        print "files[0] hashlist[0] :%s "%( hashlist[0].this )
        print "files[%d]: %s hashlist[%d] :%s hash = %x"%( i, filename, count, hashlist[count].this ,tmphash )
        count+=1
        l.append(tmp)
      print "files[%d]: %s hashlist[i] :%s hash = %x"%( 5, filename, hashlist[5].this ,tmphash )
    #enddebug
    
  #
  # arg 2 must be DP**
  # hashlist is an array. hashlist.cast().this is DP *
  # hashlist is proxy to DPClass ( proxy to DP*)
  # hashlist.cast is proxy DP* 
  # we need a pointer on hashlist.cast()[0] ->
  #      TypeError: (pHash.)'DP' object does not support indexing
  # hashlist.cast().this is a pointer to the DP[0]  ( SWIG Object to DP *)
  # 
  #

  # method with pointer_function // 
  ###hashlist1=pHash.copy_DPFunc(hashlist.cast().this)
  ###hashlist2=pHash.copy_DPptrFunc(hashlist1)
  ## ok working
  ##hashlist2=pHash.copy_DPptrFunc(hashlist.cast().this)
  # method with DPArray being a DP **
  #print hashlist.cast()
  hashlist2=hashlist.cast()

  hashlistf=hashlist2

  #print 'hashlist2',hashlist2 
  # method with pointer_class
  #hashlist1=pHash.DPClass.frompointer(hashlist.cast().this)
  #hashlist2=pHash.DPptrClass()
  #hashlist2.assign(hashlist1.cast().this)
  #hashlistf=hashlist2.cast()

  #print 'count',count  
  #print
  #print 'callsizeof ',pHash.print_sizeof_MVPFile()
  #print 'hashlistf',hashlistf
  #for i in range(0,count):
  #  print 'hashlist[%d]  %s'%(i,hashlist[i].this)
  #  #
  ret = pHash.ph_save_mvptree(mvpfile, hashlistf, count)
  # ret 11 is null hash distance function
  # save: ret code 17 has callback func. -> not enought hashdist ?
  print "save: ret code %d"%(ret)


  print '%s'%( mvpfile)
  
  print '%s'%(mvpfile.filename)
  #segfault
  #print '%s'%(mvpfile.buf)
  print '%s'%(mvpfile.file_pos)
  print '%s'%(mvpfile.fd)
  print '%s'%(mvpfile.filenumber)
  print '%s'%(mvpfile.nbdbfiles)
  print '%s'%(mvpfile.branchfactor)
  print '%s'%(mvpfile.pathlength)
  print '%s'%(mvpfile.leafcapacity)
  print '%s'%(mvpfile.pgsize)
  print '%s'%(mvpfile.hash_type)
  #print '%s'%(mvpfile.hashdist)


  #free is done by GC .. ?
  #for i in range(0,nbfiles):
  #  pHash.ph_free_datapoint(hashlist[i])

  #free is done by GC .. ?
  #for i in range(0,nbfiles):
  #  pHash.free(files[i])

  #free is done by GC .. ?
  #for i in range(0,nbfiles):
  #  pHash.free(hashlist[i]->hash)

  # pHash.free(hashlist)



if __name__ == '__main__':
  main(sys.argv[1:])


