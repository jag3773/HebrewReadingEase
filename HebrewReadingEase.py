#!/usr/bin/env python
# -*- coding: utf8 -*-
#  Copyright (c) 2010 Jesse Griffin
#  http://creativecommons.org/licenses/MIT/
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

from string import punctuation
from operator import itemgetter
from xml.dom import minidom
from collections import defaultdict
from decimal import *
import os
import sys

####################
class ReadingEase():

  def __init__(self):
    self.reference = sys.argv[1:]
    self.bookdir = '../morphhb/wlc'
    books = os.listdir(self.bookdir)
    self.listdir = './lists'
    self.biblefile = 'HebrewBible.txt'
    self.biblefreqlistfile = 'HebrewBible-FrequencyList.txt'
    self.hrefile = 'hre.txt'
    self.N = 113000
    self.books = ["Gen","Exod","Lev","Num", "Deut", "Josh", "Judg", "Ruth",
      "1Sam","2Sam","1Kgs","2Kgs","1Chr", "2Chr","Ezra","Neh","Esth","Job",
      "Ps","Prov","Eccl","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel",
      "Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal"]
    self.cantillation = [u'\u0590',u'\u0591',u'\u0592',u'\u0593',u'\u0594',u'\u0595',
          u'\u0596',u'\u0597',u'\u0598',u'\u0599',u'\u059A',u'\u059B',
          u'\u059C',u'\u059D',u'\u059E',u'\u059F',u'\u05A0',u'\u05A1',
          u'\u05A2',u'\u05A3',u'\u05A4',u'\u05A5',u'\u05A6',u'\u05A7',
          u'\u05A8',u'\u05A9',u'\u05AA',u'\u05AB',u'\u05AC',u'\u05AD',
          u'\u05AE',u'\u05AF',u'\u002F'] #Also includes '/' character

  def normalize(self, data):
    for cant in self.cantillation:
      data = data.replace(cant, '')
    return data

  def transform(self):
    if os.access(self.biblefile, os.F_OK): print "Found flat Hebrew Bible file"
    else:
      print "Creating flat Hebrew Bible file..."
      self.biblef = open(self.biblefile, 'w')
      for self.book in self.books:
        print self.book
        bookxml = minidom.parse('./%s/%s.xml' % (self.bookdir, self.book))
        chapterlist = bookxml.getElementsByTagName('chapter')
        self.c = 1
        for chap in chapterlist:
          chapterxml = chapterlist[self.c - 1]
          verselist = chapterxml.getElementsByTagName('verse')
          for verse in verselist:
            self.ref = ( verse.attributes['osisID'].value.encode('utf-8')
                       .split('.') )
            self.mywelements = verse.childNodes
            self.mytext = []
            for el in self.mywelements:
              try:
                if el.tagName == 'w':
                  self.mytext.append(self.normalize(el.firstChild.data)
                      .encode('utf-8'))
                elif el.tagName == 'note':
                  self.noteelements = el.childNodes
                  for nel in self.noteelements:
                    if nel.tagName == 'rdg':
                      if nel.attributes['type'] == 'x-qere':
                        self.mytext.pop(-1)
                        self.mytext.append(self.normalize(nel.childNodes[0]
                                   .firstChild.data).encode('utf-8'))
                      else: pass
                    else: pass
                else: pass
              except AttributeError: pass
            print >> self.biblef, '%s' % '\n'.join(self.mytext)
          self.c += 1
      self.biblef.close()

  def createdictionary(self):
    if os.access(self.biblefreqlistfile, os.F_OK):
      print "Loading Frequency Dictionary..."
      mylist = '{' + open(self.biblefreqlistfile).read() + '}'
      myformlist = mylist.replace('\n', ' ')
      self.dictlist = eval(myformlist)
    else:
      #perhaps import collections and use Counter()
      print "Creating Frequency Dictionary..."
      self.words = defaultdict(int)
      self.words_gen = (line.strip().lower() for line in open(self.biblefile))
      for word in self.words_gen:
        self.words[word] = self.words.get(word, 0) + 1
      self.top_words = sorted(self.words.iteritems(), key=itemgetter(1),
                                                   reverse=True)[:self.N]
      freqwords = open(self.biblefreqlistfile, 'a')
      for word, frequency in self.top_words:
        print >> freqwords, "'%s': %d," % (word, frequency)
      freqwords.close()
      mylist = '{' + open(self.biblefreqlistfile).read() + '}'
      myformlist = mylist.replace('\n', ' ')
      self.dictlist = eval(myformlist)

  def rate(self):
    print "Rating..."
    self.href = open(self.hrefile, 'w')
    for self.book in self.books:
      print self.book
      bookxml = minidom.parse('./%s/%s.xml' % (self.bookdir, self.book))
      chapterlist = bookxml.getElementsByTagName('chapter')
      self.c = 1
      self.myb = []
      for chap in chapterlist:
        chapterxml = chapterlist[self.c - 1]
        verselist = chapterxml.getElementsByTagName('verse')
        self.v = 1
        self.myc = []
        for verse in verselist:
          self.ref = verse.attributes['osisID'].value.encode('utf-8').split('.')
          self.mywelements = verse.childNodes
          self.myv = []
          for el in self.mywelements:
            try:
              if el.tagName == 'w':
                self.myv.append(self.normalize(el.firstChild.data)
                                                     .encode('utf-8'))
                self.myc.append(self.normalize(el.firstChild.data)
                                                     .encode('utf-8'))
                self.myb.append(self.normalize(el.firstChild.data)
                                                     .encode('utf-8'))
              elif el.tagName == 'note':
                self.noteelements = el.childNodes
                for nel in self.noteelements:
                  if nel.tagName == 'rdg':
                    if nel.attributes['type'] == 'x-qere':
                      self.myv.pop(-1)
                      self.myv.append(self.normalize(nel.childNodes[0]
                                      .firstChild.data).encode('utf-8'))
                      self.myc.pop(-1)
                      self.myc.append(self.normalize(nel.childNodes[0]
                                      .firstChild.data).encode('utf-8'))
                      self.myb.pop(-1)
                      self.myb.append(self.normalize(nel.childNodes[0]
                                      .firstChild.data).encode('utf-8'))
                    else: pass
                  else: pass
              else: pass
            except AttributeError: pass
          self.readingease(self.myv)
          print >> self.href, '%d, %d, %s.%s.%i' % (self.myreadingease,
            self.myharmonicease, self.book, self.c, self.v)
          self.v += 1
        self.readingease(self.myc)
        print >> self.href, '%d, %d, %s.%s' % (self.myreadingease,
          self.myharmonicease, self.book, self.c)
        self.c += 1
      self.readingease(self.myb)
      print >> self.href, '%d, %d, %s' % (self.myreadingease,
        self.myharmonicease, self.book)
    self.href.close()

  def readingease(self, passage):
    'Generate the reading ease of the text based on the frequency list'
    self.numofwords = Decimal('0')
    self.freqsum = Decimal('0')
    self.harmonic = Decimal('0')
    for word in passage:
      mywordfreq = self.dictlist.get(word)
      self.freqsum += Decimal('%d' % mywordfreq)
      self.harmonic += 1 / Decimal('%d' % mywordfreq)
      self.numofwords += 1
    self.myreadingease = self.freqsum / self.numofwords
    self.myharmonicease = self.numofwords / self.harmonic

if __name__ == '__main__':
  hre = ReadingEase()
  hre.transform()
  hre.createdictionary()
  hre.rate()
