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
from downloadVenmurasu import downloadVenmurasu

class makeSentencesForChapter(object):
    
    def __init__(self, currentdate, folder):
        self.currentdate = currentdate
        self.folder = folder
        self.title = ''
        self.chapterSentences = {}
        
        self.avoidList = [
                          ]
        
    def processChapter(self):
        fileName = downloadVenmurasu.makeFileName(self.currentdate, self.folder).replace('.html','.txt')
        with open(fileName, 'rb') as aTxtChapter:
            for line in aTxtChapter.readlines():
                removeSplChr = re.compile("[\"\'\[\]…:-_*,;]")
                line = removeSplChr.sub('', line)
                line = line.replace('\n','')
                if line:
                    line = line.split('.')
                    for ln in line:
                        lineLen = len(ln.split())
                        if 3 > lineLen  or lineLen > 20:
                            continue #go for the next line
                        tamilLine = ln
                        ##print tamilLine
                        if lineLen in self.chapterSentences:
                            self.chapterSentences[lineLen].append(tamilLine)
                        else:
                            self.chapterSentences[lineLen] = [tamilLine]
        
    def getTitle(self):
        fileName = downloadVenmurasu.makeFileName(self.currentdate, self.folder)
        with open(fileName, 'rb') as fl:
            for line in fl:
                if '<strong>' in line:
                    line = line.split('<strong>')[1]
                    while '<' in line: 
                        line = line.split('<')[0]
                        while '>' in line: 
                            line = line.split('>')[1]
                    while ':' in line: 
                        line = line.split(':')[1]
                    line = line.split('-')[0] if '-' in line else line
                    self.title = line
                    break
                    
    def getChapterSentences(self):
        if self.chapterSentences:
            return self.chapterSentences
        else:
            self.processChapter()
            #print self.chapterSentences
            return self.chapterSentences
    
    def makeChapterDict(self):
        try:
            self.getChapterSentences()
            self.getTitle()
            chapterDict = dict([('date', self.currentdate),
                                ('folder', self.folder),
                                ('sentenceDict', self.chapterSentences),
                                ('title', self.title)
                                ])
            return chapterDict
        except Exception as e:
            ##print e.args
            ##print e.message
            return e.message

if __name__ == '__main__':
    
    ff = open('/home/raghav/Desktop/testtest,txt', 'w')
    makeThis = makeSentencesForChapter((2015,2,21),'/home/raghav/Desktop/venmurasuBooks/VenmugilNagaram')
    ff.write(str(makeThis.makeChapterDict()))
    makeThis = makeSentencesForChapter((2015,2,22),'/home/raghav/Desktop/venmurasuBooks/VenmugilNagaram')
    ff.write(str(makeThis.makeChapterDict()))
    makeThis = makeSentencesForChapter((2015,2,23),'/home/raghav/Desktop/venmurasuBooks/VenmugilNagaram')
    ff.write(str(makeThis.makeChapterDict()))
    
