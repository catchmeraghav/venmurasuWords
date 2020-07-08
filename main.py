#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import datetime
from downloadVenmurasu import downloadVenmurasu
from parseHTMLToTamilTxt import parseHTMLToTamilTxt
from makeWords import makeWordsForChapter
from durusCommit import durusCommit

from collections import OrderedDict

import makeCollections

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

def completeDownloadAndThreeSteps(downloadFiles = True):
    for book in dl.books.keys():
        folder = dl.venmurasuFolder+"/"+book
        if not os.path.exists(folder):
            os.makedirs(folder, mode=0777)
        folder = folder+"/"

        connect = durusCommit(folder, book)
        currentdate = getStartDate(book)
        enddate = getEndDate(book)
        print 'Folder name: ',folder
        while currentdate <= enddate:
            print currentdate
            chapterDownloadAndThreeSteps(currentdate, book, folder, connect, downloadFiles)
            currentdate += datetime.timedelta(days=1)    
        
        #consolidateWordsForBook(connect, book)
        
def chapterDownloadAndThreeSteps(currentdate, book, folder, connect, downloadFiles):
    #print currentdate
    #print 'Date: ', currentdate.strftime('%Y-%m-%d')
    if downloadFiles:
        if not os.path.exists(folder+currentdate.strftime('%Y-%m-%d')+'.html'):
            #dl.downloadChapter(currentdate, folder)
            dl.downloadChapter(currentdate, folder)
            #dl.downloadChapterImage(currentdate, folder)
        if not os.path.exists(folder+currentdate.strftime('%Y-%m-%d')+'.txt'): 
            convertChapterToText(currentdate, folder)
    
    checkRoot = connect.getRoot()
    dateTuple = tuple(currentdate.strftime('%Y-%m-%d').split('-'))
    if dateTuple in checkRoot.get(book, []):
        chapterDict = checkRoot[book][dateTuple]
    else:
        chapterDict = makeChapterDict(currentdate, folder)
    #print chapterDict
    if not isinstance(chapterDict, str):
        commitChapterWord(connect, currentdate, book, chapterDict)

def completeConsolidateVenmurasu():
    venmurasuDBConnect = durusCommit(dl.venmurasuFolder, 'venmurasu')
    venDict = {}
    for book in dl.books.keys():
        folder = dl.venmurasuFolder+"/"+book
        connect = durusCommit(folder, book)
        consolidateWordsForBook(connect, book)
        
        bookRoot = connect.getRoot()
        for word in bookRoot[book][book].keys():
            if word in venDict:
                    venDict[word] += bookRoot[book][book][word]
            else:
                    venDict[word] = bookRoot[book][book][word]
    venRoot = venmurasuDBConnect.getRoot()
    venRoot['Venmurasu'] = venDict

    with open(dl.venmurasuFolder+"/"+"Venmurasu_words.txt", 'w') as wrdFile:
        for item in venDict.iteritems():
            wrdFile.write(str(item[0]) +', '+ str(item[1])+'\n')

    #print 'Venmurasu keys: ', len(venDict.keys())
    venmurasuDBConnect.connectionCommit()

def consolidateWordsForBook(connect, book):
    print book
    bookDict = {}
    bookRoot = connect.getRoot()
    aKey = book
    folder = dl.venmurasuFolder+"/"+aKey
    currentdate = getStartDate(aKey)
    enddate = getEndDate(aKey)
    enddate += datetime.timedelta(days=1) 
    #print 'Folder name: ',folder
    print currentdate, enddate
    while currentdate < enddate:
        chapterDateTuple = tuple(currentdate.strftime('%Y-%m-%d').split('-'))
        print chapterDateTuple, len(bookRoot[book][chapterDateTuple]['wordsDict'].keys())
        for word in bookRoot[book][chapterDateTuple]['wordsDict'].keys():
            if word in bookDict:
                bookDict[word] += bookRoot[book][chapterDateTuple]['wordsDict'][word]
            else:
                bookDict[word] = bookRoot[book][chapterDateTuple]['wordsDict'][word]
        currentdate += datetime.timedelta(days=1)

    bookRoot[book][book] = bookDict
    print "Book unique words: ", len(bookRoot[book][book].keys())
    with open(folder+'/'+book+'_words.txt', 'w') as wrdFile:
        for item in bookRoot[book][book].iteritems():
            wrdFile.write(str(item[0]) +', '+ str(item[1])+'\n')

    connect.connectionCommit()
    print book, ' -- completed'

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

def makeVariousCollections():
     
     for book in dl.books.keys():
        folder = dl.venmurasuFolder+"/"+book
        if not os.path.exists(folder):
            os.makedirs(folder, mode=0777)
        
        collectionFolder = dl.venmurasuFolder+"/collection/"
        if not os.path.exists(collectionFolder):
            os.makedirs(collectionFolder, mode=0777)
        commaCollectionFile = collectionFolder+book+'_comma.txt'
        nocommaCollectionFile = collectionFolder+book+'_no_comma.txt'


        titleFile = os.path.join(collectionFolder,'titles.txt')

        folder = folder+"/"
        connect = durusCommit(folder, book)
        currentdate = getStartDate(book)
        enddate = getEndDate(book)
        print 'Folder name: ',folder

        with open(titleFile, 'a') as noncommacollectFile:
            while currentdate <= enddate:
                pass
                currentdate += datetime.timedelta(days=1)    

        commaItems = {}
        nonCommaItems = {}
        with open(nocommaCollectionFile, 'a') as noncommacollectFile:
            with open(commaCollectionFile, 'a') as collectFile:
                while currentdate <= enddate:
                    print currentdate
                    print 'Date: ', currentdate.strftime('%Y-%m-%d')

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

def makeCharacterChapterList():
    for book in dl.books.keys():
        folder = dl.venmurasuFolder+'/'+book 
        collectionFolder = dl.venmurasuFolder+"/characters/"
        if not os.path.exists(collectionFolder):
            os.makedirs(collectionFolder, mode=0777)
        characterCollectionFile = collectionFolder+book+'_characters.txt'

        currentdate = getStartDate(book)
        enddate = getEndDate(book)
        print 'Folder name: ',folder

        characterList = [
                            "பீஷ்மர்",
                            "பீஷ்மன்",
                            "திருதராஷ்டிரர்",
                            "திருதராஷ்டிரன்",
                            "காந்தாரி",
                            "குந்தி",
                            "கர்ணன்",
                            "யுதிஷ்டிரன்",
                            "யுதிஷ்டிரர்",
                            "பீமன்",
                            "அர்ஜுனன்",
                            "நகுலன்",
                            "சகதேவன்",
                            "திரௌபதி",
                            "துரியோதனன்",
                            "துச்சாதனன்",
                            "கிருஷ்ணன்",
                            "இளைய யாதவன்",
                            "இளைய யாதவர்",
                            "சாத்யகி",
                            "திருஷ்டத்யும்னன்"
                            ]


        characItems = { book : OrderedDict({itm : [] for itm in characterList }) }

        while currentdate <= enddate:
            fileName = downloadVenmurasu.makeFileName(currentdate,folder, '.txt')
            with open(fileName, 'rb') as aTxtChapter:
                chapterContent = aTxtChapter.read().replace('\n', '').split('.')
                for item in characterList:
                    firstOccurFlag = False
                    completeList={}

                    for sentence in chapterContent:
                        searchWord = item if len(item) < 20 else item[ : (len(item)*2/3)+1]
                        if searchWord in sentence:
                            if not firstOccurFlag: 
                                sentence3 = []
                                if chapterContent[0] == sentence:
                                    sentence3 = chapterContent[:3]
                                elif chapterContent[-1] == sentence:
                                    sentence3 = chapterContent[-3:]
                                else:
                                    idx = chapterContent.index(sentence)
                                    sentence3 = chapterContent[idx-1 : idx+2] 
                                completeList= { 'chapter' : str(currentdate), 'link' : 'www.venmurasu.in/'+str(currentdate).replace('-','/'),
                                                'sentence' : '.'.join(sentence3),
                                                'count' : sentence.count(item)
                                              }
                                firstOccurFlag = True
                            else:
                                completeList['count'] += sentence.count(item)
                    try:
                        completeList['count'] = str(completeList['count'])
                    except:
                        pass

                    characItems[book][ item ].append(completeList) 
            currentdate += datetime.timedelta(days=1)    

        with open(characterCollectionFile.replace('.','_json.'), 'w') as collectFile:
            collectFile.write(str(characItems))
            
        with open(characterCollectionFile, 'w') as collectFile:
            outStr = ''
            for item in characItems:
                outStr += item + '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
                tabStr = '\t'
                for name in characterList:
                    outStr +='\n________________________________________________________\n'
                    outStr += tabStr + name + '\n'
                    tabStr = '\t\t'
                    if characItems[item][name]:
                        for itm in characItems[item][name]:
                            for key, val in itm.items():
                                outStr += tabStr + key + ':\t' + val + '\n'
                    outStr +='\n________________________________________________________\n'
                outStr +='\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
            collectFile.write( outStr )

   
if __name__ == '__main__':
    # Either download or consolidate - for now - for DB lock reasons
    completeDownloadAndThreeSteps(downloadFiles = True)

    chapter = False
    if chapter:
        book = 'PanniruPadaikaLam'
        folder = '/home/raghav/Desktop/venmurasuBooks/PanniruPadaikaLam/'
        connect = durusCommit(folder, book)
        chapterDownloadAndThreeSteps(datetime.date(2016,4,29), book, folder)
    
    #makeCollections.makeAllBooks()
    completeConsolidateVenmurasu()
    #makeCharacterChapterList()
