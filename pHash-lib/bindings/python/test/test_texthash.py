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
#    Evan Klinger - eklinger@phash.org
#    David Starkweather - dstarkweather@phash.org
#

import pHash
import locale,logging,os,sys,time


'''
TxtHashPoint* ph_texthash(const char *filename, int *OUTPUT);
TxtMatch* ph_compare_text_hashes(TxtHashPoint *INPUT, int N1, TxtHashPoint *INPUT, int N2, int *OUTPUT);

TxtHashPoint { item,index}


optimized version is :

    res1=pHash.ph_texthash(filename1)
    (points1Ptr,nb1)=res1

    res2=pHash.ph_texthash(filename2)
    (points1Ptr,nb2)=res2

    res=pHash.ph_compare_text_hashes(points1Ptr,nb1,points2Ptr,nb2)

    matches=Text.makeTxtMatchList(res)

'''
class Text:
  ''' '''
  def makeHash(self,filename):
    res=pHash.ph_texthash(filename)
    #res=0
    #print pHash.ph_texthash_List(filename,res)
    #print '------ makeHash :',res
    return self.makeTxtHashPointList(res)
  #
  def makeTxtHashPointList(self,res):
    if len(res) != 2 :
      print 'err: return args:', res
      return None
    (pointsPtr,nb)=res
    #item=pHash.TxtHashPointPtr_value(pointsPtr)
    items=pointsPtr
    #items=pHash.TxtHashPointArrayIn_frompointer(pointsPtr)
    print 'items :',items
    #print 'item.this :',item.this
    #help(item.this)
    #print 'item.this.index :',item.this.index
    #print 'index:',item.index,'hash:',item.hash 
    #print 'items : ',items
    #print 'index:',item.index,'hash:',item.hash 
    #print help(item)
    print '----------------- '   , (nb)
    ret=0
    #ret=[ pHash.TxtHashPointArray_getitem(pointsPtr, ind) for ind in range(0,nb,1)]
    for ind in range(0,nb):
      #print 'ind: ',ind
      #ptr=pHash.TxtHashPointArray_getitem(items, ind)
      #print 'ptr', ptr
      #item=pHash.TxtHashPointPtr_value(ptr.this)
      item=items[ind]
      #print 'item :',item
      print 'index:',item.index,'hash:',item.hash 
      #print 'item : %d'%(int(item))
      #print 'hash',item.hash
      #print 'index',item.index
      #print 'hash: %016X(%016d) \t index: %08X(%d)'%(item.hash,item.hash,item.index,item.index  )
      #print 'hash+index: %08.16X %04.8X'%(item.hash,item.index  )
      #print '%04.8X %08.16X '%(item.index,item.hash  )
    return ret
  ''' '''
  def compare(self,hashPoints1,hashPoints2):
    ''' make C arrays '''
    nb1=len(hashPoints1)
    nb2=len(hashPoints2)
    hashes1=pHash.new_TxtHashPointArray(nb1)
    hashes2=pHash.new_TxtHashPointArray(nb2)
    for i in range(0,nb1):
      pHash.TxtHashPointArray_setitem(hashes1,i,hashPoints1[i])
    for i in range(0,nb2):
      pHash.TxtHashPointArray_setitem(hashes2,i,hashPoints2[i])
    # go
    res=pHash.ph_compare_text_hashes(hashes1,nb1,hashes2,nb2)
    return self.makeTxtMatchList(res)
  #
  def makeTxtMatchList(self, res):
    if len(res) != 2 :
      return None
    (matchesPtr,nb)=res
    print (matchesPtr,nb)
    ret=[ pHash.TxtMatchArray_getitem(matchesPtr, ind) for ind in range(0,nb,1)]
    #print ' pointer ? ' ,   matchesPtr.lenght
    #for ind in range(0,nb,1):
    #  item=pHash.TxtMatchArray_getitem(matchesPtr, ind) 
    #  print 'item :',item
    #  print 'length',item.length
    return ret


class Image:
  ''' '''
  def makeHash(self,filename):
    '''WORKING
    int ph_dct_imagehash(const char* file,ulong64 &OUTPUT); '''
    res=pHash.ph_dct_imagehash(filename)
    if len(res) != 2 :
      return None
    ret,myHash=res
    print myHash
    return myHash


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

    #names,nb=pHash.ph_readfilenames(os.path.dirname(file1))
    #print names,nb
    #img='/home/jal/Pictures/test.jpg'
    #image=Image()
    #image.makeHash(img)
    #return
    
    # new style
    text=Text()
    #print "file1: %s" %(file1)
    h1=text.makeHash(file1)
    if ( h1 is None):
      print "Unable to complete text hash function"
      return
    #print "length %d"%(len(h1))
    
    return
    
    h2=text.makeHash(file2)
    #print "file2: %s" %(file2)
    if ( h2 is None):
      print "Unable to complete text hash function"
      return
    #print "length %d"%(len(h2))
    
    matches=text.compare(h1,h2)
    #print 'matches ',matches
        
    if (matches is None or len(matches) == 0):
      print "unable to complete compare function"
      return
    
    count=len(matches)
    print " %d matches"%(count)
    print " indxA  indxB  length"
    for j in range(0,count,1):
      print " %d %d %d"%( matches[j].first_index, matches[j].second_index,matches[j].length) 
    return 
  except Exception,e:
    print e


if __name__ == '__main__':
  main(sys.argv[1:])



