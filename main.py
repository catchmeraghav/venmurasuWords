#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import datetime
from downloadVenmurasu import downloadVenmurasu
from parseHTMLToTamilTxt import parseHTMLToTamilTxt
from makeWords import makeWordsForChapter
from tamil import utf8
import json
import codecs
from collections import OrderedDict
from durusCommit import durusCommit
from datetime import datetime

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
            print folder, ' -- create'
        
        collectionFolder = dl.venmurasuFolder+"/collection/"
        if not os.path.exists(collectionFolder):
            os.makedirs(collectionFolder, mode=0777)
        commaCollectionFile = collectionFolder+book+'_comma.txt'
        nocommaCollectionFile = collectionFolder+book+'_no_comma.txt'

        folder = folder+"/"
        connect = durusCommit(folder, book)
        currentdate = getStartDate(book)
        enddate = getEndDate(book)
        print 'Folder name: ',folder

        commaItems = {}
        nonCommaItems = {}
        with open(nocommaCollectionFile, 'a') as noncommacollectFile:
            with open(commaCollectionFile, 'a') as collectFile:
                while currentdate <= enddate:
                    print currentdate
                    #print 'Date: ', currentdate.strftime('%Y-%m-%d')
                    chapterDownloadAndThreeSteps(currentdate, book, folder, connect)

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
    #print currentdate
    #print 'Date: ', currentdate.strftime('%Y-%m-%d')

    if not os.path.exists(folder+currentdate.strftime('%Y-%m-%d')+'.html'):
        print folder+currentdate.strftime('%Y-%m-%d')+'.html' , " : ", str(os.path.exists(folder+currentdate.strftime('%Y-%m-%d')+'.html'))
        print "downloading now"
        dl.downloadChapter(currentdate, folder)
    else: 
        pass #print "html file exists - not downloading"

    
    '''
    imgName = currentdate.strftime('%Y-%m-%d')+'.jpg'
    normalImgName = os.path.join(folder,imgName)
    bigImgName = os.path.join(folder,'big-'+imgName)
            
    if not (os.path.exists(bigImgName) or os.path.exists(normalImgName)):
        pass
        dl.downloadChapterImage(currentdate, folder)
    '''
    
    if not os.path.exists(folder+currentdate.strftime('%Y-%m-%d')+'.txt'): 
        convertChapterToText(currentdate, folder)
    else: 
        pass #print "txt file exists - not converting"

    #'''
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

        folder = folder+"/"
        connect = durusCommit(folder, book)
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

        consolidateWordsForBook(connect, book)
 

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


def completeConsolidateVenmurasu():
    venmurasuDBConnect = durusCommit(dl.venmurasuFolder, 'venmurasu')
    for book in dl.books.keys():
        venDict = venmurasuDBConnect.getRoot()
        folder = dl.venmurasuFolder+"/"+book

        if os.path.isfile(folder+"/"+book+".durus"):
            os.remove(folder+"/"+book+".durus")

        connect = durusCommit(folder, book)
        consolidateWordsForBook(connect, book, chapterCollect=True)
        bookRoot = connect.getRoot()
        for word in bookRoot[book][book]:
            if word in venDict:
                venDict[word] += bookRoot[book][book][word]
            else:
                venDict[word] = bookRoot[book][book][word]
        venmurasuDBConnect.connectionCommit()
        print book, " --- Now completed"
        print 'Keys in %s : %s'%(book, len(bookRoot[book][book].keys()))
        print 'Keys now in %s : %s'%('Venmurasu', len(venDict.keys()))

    venDict = venmurasuDBConnect.getRoot()
    with open('VenmurasuWord_'+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'.csv', 'w') as totalFile:
        for word in venDict:
            totalFile.write(word+','+str(venDict[word])+'\n')

def writeVenmurasuDurusasFile():
    venmurasuDBConnect = durusCommit(dl.venmurasuFolder, 'venmurasu')
    venDict = venmurasuDBConnect.getRoot()
    with open('VenmurasuWord_'+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'.csv', 'w') as totalFile:
        for word in venDict:
            totalFile.write(word+','+str(venDict[word])+'\n')


def consolidateWordsForBook(connect, book, chapterCollect=True):
    bookDict = {}
    bookRoot = connect.getRoot()
    aKey = book
    folder = dl.venmurasuFolder+"/"+aKey
    currentdate = getStartDate(aKey)
    enddate = getEndDate(aKey)
    print 'Folder name: ',folder
    while currentdate <= enddate:
        try:
            if chapterCollect:
                collectChapter(currentdate, book, folder, connect)
            chapterDateTuple = tuple(currentdate.strftime('%Y-%m-%d').split('-'))
            print chapterDateTuple, len(bookRoot[book][chapterDateTuple]['wordsDict'].keys())
            for word in bookRoot[book][chapterDateTuple]['wordsDict'].keys():
                if word in bookDict:
                    bookDict[word] += bookRoot[book][chapterDateTuple]['wordsDict'][word]
                else:
                    bookDict[word] = bookRoot[book][chapterDateTuple]['wordsDict'][word]
            currentdate += datetime.timedelta(days=1)
        except:
            print "date key missing"
            currentdate += datetime.timedelta(days=1)
    bookRoot[book][book] = bookDict
    print "Book unique words: ", len(bookRoot[book][book].keys())
    connect.connectionCommit()


def collectChapter(currentdate, book, folder, connect):
    checkRoot = connect.getRoot()

    dateTuple = tuple(currentdate.strftime('%Y-%m-%d').split('-'))
    if checkRoot.get(book) and dateTuple in checkRoot[book]:
        chapterDict = checkRoot[book][dateTuple]
    else:
        chapterDict = makeChapterDict(currentdate, folder)
    #print chapterDict
    if not isinstance(chapterDict, str):
        commitChapterWord(connect, currentdate, book, chapterDict)

if __name__ == '__main__':
    writeVenmurasuDurusasFile()
    '''
    #makeCharacterChapterList()
    
    # Either download or consolidate - for now - for DB lock reasons
    download = False
    if download:
        chapter = True
        if not chapter:
            completeDownloadAndThreeSteps()
            completeConsolidateVenmurasu()
        if chapter:
            book = 'Mudharkanal'
            folder = '/home/raghav/Desktop/venmurasuWords/venbooks/content/Mudharkanal'
            connect = durusCommit(folder, book)
            consolidateWordsForBook(connect, book)
            #chapterDownloadAndThreeSteps(datetime.date(2016,4,29), book, folder)
            
    if not download:
        completeConsolidateVenmurasu()
    #'''
