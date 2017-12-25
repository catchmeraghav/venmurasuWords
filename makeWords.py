#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
*
* 28 Feb 2015
* This file is used to read chapter as text and 
* make a dict of words
* The dict of words can further be processed and/ or included in bigger dicts
* bigger dicts corresponding to a book and further the whole series 
*
* Further have included code to save data to a ObjectDB - Durus
* Still getting to know Durus - supposed to be good with cache
*
'''

import re
from tamil import utf8
from downloadVenmurasu import downloadVenmurasu

class makeWordsForChapter(object):
    
    def __init__(self, currentdate, folder):
        self.currentdate = currentdate
        self.folder = folder
        self.chapterWords = {}
        
    def processChapter(self):
        fileName = downloadVenmurasu.makeFileName(self.currentdate, self.folder).replace('.html','.txt')
        with open(fileName, 'rb') as aTxtChapter:
            for line in aTxtChapter.readlines():
                removeSplChr = re.compile("[\"\'\[\]…:.-_*,;]")
                line = removeSplChr.sub('', line)
                line = line.split()
                for word in line:
                    word = ''.join(utf8.get_letters(word))
                    if word in self.chapterWords:
                        self.chapterWords[word]+=1
                    else:
                        self.chapterWords[word] = 1

    def getChapterWords(self):
        if self.chapterWords:
            return self.chapterWords
        else:
            self.processChapter()
            return self.chapterWords
    
    def makeChapterDict(self):
        try:
            self.getChapterWords()
            
            chapterDict = dict([('date', self.currentdate),
                                ('folder', self.folder),
                                ('wordsDict', self.chapterWords)
                            ])
            return chapterDict
        except Exception as e:
            #print e.args
            #print e.message
            return e.message

if __name__ == '__main__':
    makeThis = makeWordsForChapter((2015,2,21),'/home/raghav/Desktop/venmurasuBooks/VenmugilNagaram')
    makeThis.makeChapterDict()
    makeThis = makeWordsForChapter((2015,2,22),'/home/raghav/Desktop/venmurasuBooks/VenmugilNagaram')
    makeThis.makeChapterDict()
    makeThis = makeWordsForChapter((2015,2,23),'/home/raghav/Desktop/venmurasuBooks/VenmugilNagaram')
    makeThis.makeChapterDict()