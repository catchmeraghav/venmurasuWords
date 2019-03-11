#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import datetime
from downloadVenmurasu import downloadVenmurasu
from parseHTMLToTamilTxt import parseHTMLToTamilTxt
from makeWords import makeWordsForChapter
from tamil import utf8
#from durusCommit import durusCommit


dl = downloadVenmurasu()

def getStartDate(book):
    aDate = dl.books[book][0]
    return datetime.date(aDate[0], aDate[1], aDate[2])

def getEndDate(book):
    aDate = dl.books[book][1]
    return datetime.date(aDate[0], aDate[1], aDate[2])

def convertChapterToText(currentdate, folder):
    chapterToTamil = parseHTMLToTamilTxt()
    return chapterToTamil.convertChapterToText(currentdate, folder)

def makeChapterDict(currentdate, folder):
    mkWds = makeWordsForChapter(currentdate, folder)
    return mkWds.makeChapterDict()

def commitChapterWord(connect, currentdate, aKey, chapterDict):
    connect.makeChapterCommit(currentdate, aKey, chapterDict)

def completeDownloadAndThreeSteps():
    for book in dl.books.keys():
        folder = dl.venmurasuFolder+"/"+book
        if not os.path.exists(folder):
            os.makedirs(folder, mode=0777)
        
        collectionFolder = dl.venmurasuFolder+"/collection/"
        if not os.path.exists(collectionFolder):
            os.makedirs(collectionFolder, mode=0777)
        commaCollectionFile = collectionFolder+book+'_comma.txt'
        nocommaCollectionFile = collectionFolder+book+'_no_comma.txt'

        folder = folder+"/"
        #connect=Mock()
        #connect = durusCommit(folder, book)
        currentdate = getStartDate(book)
        enddate = getEndDate(book)
        print 'Folder name: ',folder

        commaItems = {}
        nonCommaItems = {}
        with open(nocommaCollectionFile, 'a') as noncommacollectFile:
            with open(commaCollectionFile, 'a') as collectFile:
                while currentdate <= enddate:
                    print currentdate
                    print 'Date: ', currentdate.strftime('%Y-%m-%d')
                    chapterDownloadAndThreeSteps(currentdate, book, folder)

                    res = None
                    res = processChapterForCollections(currentdate, folder)
                    if res:
                        resTxt = "~~~~~~~~~\n",str(currentdate),"\n~~~~~~~~~\n"
                        for itm in res:
                            resTxt += "-->\t", itm,"\n"
                        collectFile.writelines(resTxt)
                    res = None
                    res = processChapterForCollections(currentdate, folder, True)
                    if res:
                        resTxt = "~~~~~~~~~\n",str(currentdate),"\n~~~~~~~~~\n"
                        for itm in res:
                            resTxt += "-->\t", itm,"\n"
                        noncommacollectFile.writelines(resTxt)
            
                    currentdate += datetime.timedelta(days=1)    

        #consolidateWordsForBook(connect, book)
        
def chapterDownloadAndThreeSteps(currentdate, book, folder, connect=None):
    print currentdate
    print 'Date: ', currentdate.strftime('%Y-%m-%d')
    if not os.path.exists(folder+currentdate.strftime('%Y-%m-%d')+'.html'):
        dl.downloadChapter(currentdate, folder)
    imgName = currentdate.strftime('%Y-%m-%d')+'.jpg'
    normalImgName = os.path.join(folder,imgName)
    bigImgName = os.path.join(folder,'big-'+imgName)
            
    if not (os.path.exists(bigImgName) or os.path.exists(normalImgName)):
        pass
        #dl.downloadChapterImage(currentdate, folder)
    if not os.path.exists(folder+currentdate.strftime('%Y-%m-%d')+'.txt'): 
        convertChapterToText(currentdate, folder)

    '''
    checkRoot = connect.getRoot()
    dateTuple = tuple(currentdate.strftime('%Y-%m-%d').split('-'))
    if checkRoot.get(book) and dateTuple in checkRoot[book]:
        chapterDict = checkRoot[book][dateTuple]
    else:
        chapterDict = makeChapterDict(currentdate, folder)
    #print chapterDict
    if not isinstance(chapterDict, str):
        commitChapterWord(connect, currentdate, book, chapterDict)
    #'''

def processChapterForCollections(currentdate, folder, nonComma = False):
    commaLimit = 3
    fileName = downloadVenmurasu.makeFileName(currentdate,folder, '.txt')
    chapterList= []
    with open(fileName, 'rb') as aTxtChapter:

        for line in aTxtChapter.readlines():
            for sentence in line.split('.'):
                commaCount = sentence.count(',')
                if commaCount > commaLimit:
                    #print ''.join(utf8.get_letters(sentence))
                    chapterList.append(sentence)

                if nonComma:
                    # A second checkon collectable
                    checkList = ['ரும்', 'உம்', 'யும்', 'கும்',  'ளும்', 'னும்']
                    checkCount = 0
                    for item in checkList:
                        if item in sentence:
                            checkCount += sentence.count(item)
                    if checkCount > commaLimit:
                        #print "Non comma item check: ", ''.join(utf8.get_letters(sentence))
                        chapterList.append(sentence)
    if chapterList:
        return chapterList
    else:
        return None        



def completeConsolidateVenmurasu():
    #venmurasuDBConnect = durusCommit(dl.venmurasuFolder, 'venmurasu')
    venDict = {}
    for book in dl.books.keys():
        pass
        #venmurasuDBConnect.connectionCommit()

def consolidateWordsForBook(connect, book):
    bookDict = {}
    bookRoot = connect.getRoot()
    for aKey in dl.books.keys():
        folder = dl.venmurasuFolder+"/"+aKey
        currentdate = getStartDate(aKey)
        enddate = getEndDate(aKey)
        print 'Folder name: ',folder
        
        while currentdate <= enddate:
            chapterDateTuple = tuple(currentdate.strftime('%Y-%m-%d').split('-'))
            print chapterDateTuple, len(bookRoot[book][chapterDateTuple]['wordsDict'].keys())
            for word in bookRoot[book][chapterDateTuple]['wordsDict'].keys():
                if word in bookDict:
                    bookDict[word] += bookRoot[book][chapterDateTuple]['wordsDict'][word]
                else:
                    bookDict[word] = bookRoot[book][chapterDateTuple]['wordsDict'][word]
    print "Book unique words: ", len(bookRoot[book][book].keys())
    bookRoot[book][book] = bookDict
    connect.connectionCommit()

def mergeChapterWordsInToBook(currentdate, book, folder, connect):
    chapterDownloadAndThreeSteps(currentdate, book, folder, connect)
    bookRoot = connect.getRoot()
    bookDict = bookRoot[book][book]
    chapterDateTuple = tuple(currentdate.strftime('%Y-%m-%d').split('-'))
    for key in bookRoot[book][chapterDateTuple]['wordsDict'].keys():
        if key in bookDict:
            bookDict[key] += bookRoot[book][chapterDateTuple]['wordsDict'][key]
        else:
            bookDict[key] = bookRoot[book][chapterDateTuple]['wordsDict'][key]
    bookRoot[book][book] = bookDict
    connect.connectionCommit()
    
if __name__ == '__main__':
    
    # Either download or consolidate - for now - for DB lock reasons
    download = True
    if download:
        chapter = False
        if not chapter:
            completeDownloadAndThreeSteps()
        if chapter:
            book = 'PanniruPadaikaLam'
            folder = '/home/raghav/Desktop/venmurasuBooks/PanniruPadaikaLam/'
            #connect = durusCommit(folder, book)
            chapterDownloadAndThreeSteps(datetime.date(2016,4,29), book, folder)
            
    if not download:
        completeConsolidateVenmurasu()
