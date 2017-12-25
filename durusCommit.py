#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from durus.file_storage import FileStorage
from durus.connection import Connection
from durus.persistent_dict import PersistentDict

class durusCommit(object):
    "A class to simply commit a given data with date tuple as key"
    def __init__(self, folder, dbFileName):
        self.dbFileName = folder+'/'+dbFileName+'.durus'
        ##print 'Durus file name: ', self.dbFileName
        self.con = Connection(FileStorage(self.dbFileName))
        
    
    def getRoot(self):
        return self.con.get_root()
    
    def connectionCommit(self):
        self.con.commit()
    
    def makeChapterCommit(self, currentdate, book, chapterDict):
        dateKey = ()
        #print 'Book name: ',book
        if isinstance(currentdate, tuple):
            dateKey = currentdate
        if isinstance(currentdate, datetime.date):
            dateKey = tuple(currentdate.strftime('%Y-%m-%d').split('-'))
        #print 'Datekey : ',dateKey  
        
        root = self.con.get_root()
        if not book in root:
            root[book] = PersistentDict()
            self.con.commit()
        root[book][dateKey] = chapterDict
        self.con.commit()
        ##print 'Durus root key - Book key: ',root.keys()
        ##print 'Durus root key - Chapter key: ',root[root.keys()[0]].keys()
        #print "commit done"

if __name__ == '__main__':
    from makeWords import makeWordsForChapter
    folder='/home/raghav/Desktop/venmurasuBooks/VenmugilNagaram'
    
    c = durusCommit('VenmugilNagaram')
    makeThis = makeWordsForChapter((2015,2,21),folder)
    chapterDict = makeThis.saveChapterWordsToDurus()
    c.makeChapterCommit((2015,2,21), folder, chapterDict)
    
    makeThis = makeWordsForChapter((2015,2,22),folder)
    chapterDict = makeThis.saveChapterWordsToDurus()
    c.makeChapterCommit((2015,2,22), folder, chapterDict)
    
    makeThis = makeWordsForChapter((2015,2,23),folder)
    chapterDict = makeThis.saveChapterWordsToDurus()
    c.makeChapterCommit((2015,2,23), folder, chapterDict)