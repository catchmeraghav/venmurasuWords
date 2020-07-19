#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import datetime
from downloadVenmurasu import downloadVenmurasu
import json
import codecs
from collections import OrderedDict
from durusCommit import durusCommit
from makeWords import makeWordsForChapter
import copy
from operator import itemgetter
import bs4 as bs
from collections import OrderedDict
import sqlite3
import time
import shutil
from bs4 import BeautifulSoup



dl = downloadVenmurasu()

characterList =[
"இசை",
"முழவு",
"பறை",
"தாளம்",
"பாணம்",
"விறலி",
"யாழ்",
"சுருதி",
"மீட்டல்",
"லயித்து",
] 

'''['ஹஸ்தி',]
                    "பீஷ்மர்",
                    "திருதராஷ்டிரர்",
                    "காந்தாரி",
                    "குந்தி",
                    "கர்ணன்",
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

'''

def getStartDate(book):
    aDate = dl.books[book][0]
    return datetime.date(aDate[0], aDate[1], aDate[2])

def getEndDate(book):
    aDate = dl.books[book][1]
    return datetime.date(aDate[0], aDate[1], aDate[2])

def makeChapterDict(currentdate, folder):
    mkWds = makeWordsForChapter(currentdate, folder)
    return mkWds.makeChapterDict()

def commitChapterWord(connect, currentdate, aKey, chapterDict):
    connect.makeChapterCommit(currentdate, aKey, chapterDict)

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
        #print 'Folder name: ',folder

        commaItems = {}
        nonCommaItems = {}
        with open(nocommaCollectionFile, 'a') as noncommacollectFile:
            with open(commaCollectionFile, 'a') as collectFile:
                while currentdate <= enddate:
                    #print currentdate
                    #print 'Date: ', currentdate.strftime('%Y-%m-%d')

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
                        ##print "Non comma item check: ", ''.join(utf8.get_letters(sentence))
                        chapterList.append(sentence)
    if chapterList:
        return chapterList
    else:
        return None        


def fetchResultsForList():
    characterList = ['ஹஸ்தி',
                    "பீஷ்மர்",
                    "திருதராஷ்டிரர்",
                    "காந்தாரி",
                    "குந்தி",
                    "கர்ணன்",
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


def wordsRelations():
    venmurasuConnect =  durusCommit(dl.venmurasuFolder, 'venmurasu')
    venmurasuRoot =  venmurasuConnect.getRoot()
    for book in dl.books.keys():
        #print book
        folder = dl.venmurasuFolder+'/'+book 
        currentdate = getStartDate(book)
        enddate = getEndDate(book)
        currentTitle = ''

        bookConnect = durusCommit(folder, book)

        while currentdate <= enddate:
 
            currentdate += datetime.timedelta(days=1)    


def makeNeoThamizhan():

    completeJson = []
    sampleDict = {
	"novelno":0,
	"novelname":"",	
	"sectionno":0,
	"sectionname":"",	
	"chapter":0,
	"published_on":"",
	"url":"",
	"image":"",
	"tags":[]
    }

    
    venmurasuConnect =  durusCommit(dl.venmurasuFolder, 'venmurasu')
    venmurasuRoot =  venmurasuConnect.getRoot()
    for book in dl.books.keys():
        #print book
        folder = dl.venmurasuFolder+'/'+book 
        currentdate = getStartDate(book)
        enddate = getEndDate(book)
        currentTitle = ''

        bookConnect = durusCommit(folder, book)

        while currentdate <= enddate:
            htmlfileName = downloadVenmurasu.makeFileName(currentdate,folder, '.html')
            htmlChapterHeader = ""
            htmlChapterHeader, titleText = "", ""
            with open(htmlfileName, 'r') as htmlObj:
                htmlContent = htmlObj.read()
                bsContent = bs.BeautifulSoup(htmlContent, 'html.parser')
                htmlChapterHeader = bsContent.find_all('header', {"class": "entry-header"})[0].text

                titleText = [para.getText() for para in bsContent.find_all('p') if para.getText()]
                titleText = titleText[0].strip()
                titleText = titleText if (not  titleText.count(':')== 1 and titleText.count('.') <= 1) and  titleText.count(':')== 1 or titleText.count('.') <= 1 else ''
                currentTitle = titleText if titleText else currentTitle

            chapterDict = copy.deepcopy(sampleDict)
            chapterDict['novelno'] = dl.books.keys().index(book)+1
            chapterDict["novelname"] = dl.booksTamilNames.get(book, 'வெண்முரசு	 ')
            chapterDict["sectionno"] = 0
            chapterDict["sectionname"] = currentTitle

            delta = currentdate - getStartDate(book)
            chapterDict["chapter"] = delta.days +1
            chapterDict["published_on"] = currentdate.strftime("%d-%m-%Y")
            chapterDict["url"] = 'https://venmurasu.in/'+currentdate.strftime("%Y/%m/%d")
            
            chapterDict["image"] = ""
            chapterDict["tags"] = []

            bookRoot = bookConnect.getRoot()
            dateKey = tuple(currentdate.strftime('%Y-%m-%d').split('-'))
            wordsOnDate = bookRoot[book][dateKey]['wordsDict'].keys()
            for aWord in wordsOnDate:
                if aWord in venmurasuRoot['Venmurasu'] and venmurasuRoot['Venmurasu'][aWord] < 5735:
                    chapterDict["tags"].append(aWord)
            completeJson.append(chapterDict)
            currentdate += datetime.timedelta(days=1)    
    collectionFolder = dl.venmurasuFolder+"/collection/title/"
    if not os.path.exists(collectionFolder):
        os.makedirs(collectionFolder, mode=0777)
    with open(collectionFolder+'titles.txt', 'w') as titlefile:
        pass
        titlefile.write( str(completeJson) )
    with open(collectionFolder+'book-title-date.txt', 'w') as titlefile:
        pass
        for itm in completeJson:
            titlefile.write( str(itm['novelno']) + ' - ' + str(itm["chapter"]) + ' - ')
            titlefile.write( itm['novelname'].encode('utf8') )
            titlefile.write( itm['sectionname'].encode('utf8') )
            titlefile.write( '\n' )




    import pprint
    class MyPrettyPrinter(pprint.PrettyPrinter):
        def format(self, object, context, maxlevels, level):
            if isinstance(object, unicode):
                return (object.encode('utf8'), True, False)
            return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

    MyPrettyPrinter().pprint(completeJson)


def makeAllBooks():
    for book in dl.books.keys():
        ignore_texts = ['Post navigation',
                        u'பின்னூட்டங்கள் மூடப்பட்டுள்ளது.',
                        u'உங்கள் மின்னஞ்சல் இங்கே கொடுத்து அதன் வழி பதிவுகளைப் பெறவும்.',
                        u'வெண்முரசு அனைத்து விவாதங்களும்',
                        u'மகாபாரத அரசியல் பின்னணி வாசிப்புக்காக',
                        u'வெண்முரசு வாசகர் விவாதக்குழுமம்',
                        ]
        print book
        existingfolder = dl.venmurasuFolder+'/'+book
        folder = dl.venmurasuFolder+'/books/'
        if not os.path.exists(folder):
            os.makedirs(folder, mode=0777)
        
        bookFileName = folder+book+'.doc'
        currentdate = getStartDate(book)
        enddate = getEndDate(book)
  
        with open(bookFileName, 'wb') as outfile:
            while currentdate <= enddate:
                txtfileName = downloadVenmurasu.makeFileName(currentdate,existingfolder, '.html')
                episodeText = ''
                soup = BeautifulSoup(open(txtfileName), 'html.parser')
                for elem in soup.find_all():
                    if elem.name == 'footer':
                       break
                    if elem.name == 'p':

                        extacted_text = elem.get_text().strip()
                        if elem.find('a'):
                            extacted_text = '--\t\t'+extacted_text
                        episodeText += extacted_text
                        episodeText += '\n\n'
                outfile.write('\n\n')
               
                for itm in ignore_texts:
                    episodeText.replace(itm, '')

                outfile.write(episodeText.encode('utf-8'))
                currentdate += datetime.timedelta(days=1) 

def makeBookAndTitle():
    for book in dl.books.keys():
        folder = dl.venmurasuFolder+'/'+book 
        currentdate = getStartDate(book)
        enddate = getEndDate(book)
        
        printList = OrderedDict()
        while currentdate <= enddate:
            htmlfileName = downloadVenmurasu.makeFileName(currentdate,folder, '.html')
            htmlChapterHeader = ""
            htmlChapterHeader, titleText = "", ""
            with open(htmlfileName, 'r') as htmlObj:
                htmlContent = htmlObj.read()
                bsContent = bs.BeautifulSoup(htmlContent, 'html.parser')
                htmlChapterHeader = bsContent.find_all('header', {"class": "entry-header"})[0].text

                titleText = [para.getText() for para in bsContent.find_all('p') if para.getText()]
                titleText = titleText[0].strip()
                titleText = titleText if (not  titleText.count(':')== 1 and titleText.count('.') <= 1) and  titleText.count(':')== 1 or titleText.count('.') <= 1 else ''
                if titleText not in printList:
                    printList[ titleText ] = ( currentdate, htmlChapterHeader )
            currentdate += datetime.timedelta(days=1)    
        strOut =  "=================================================\n"
        strOut += book
        strOut += "\n=================================================\n"
        for i in printList:
            strOut += '\n\t'
            strOut += i 
            strOut +=' --- '
            strOut += printList[i][0].strftime("%m-%d-%Y")
            strOut +=' --- '
            strOut += printList[i][1].strip()
        strOut +=  "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
       
        with open('titles.txt', 'w') as titleFile:
            pass
            #titleFile.write( strOut )
        print strOut



def makeWordSearch(word):
    characterList = [ word ] 
    outStr = ''
    for book in dl.books.keys():
        folder = dl.venmurasuFolder+'/'+book 
        currentdate = getStartDate(book)
        enddate = getEndDate(book)
        characItems = { book : OrderedDict({itm : [] for itm in characterList }) }
        while currentdate <= enddate:
            fileName = downloadVenmurasu.makeFileName(currentdate,folder, '.txt')
            
            htmlfileName = downloadVenmurasu.makeFileName(currentdate,folder, '.html')
            htmlChapterHeader = ""
            htmlChapterHeader, titleText = "", ""
            with open(htmlfileName, 'r') as htmlObj:
                htmlContent = htmlObj.read()
                bsContent = bs.BeautifulSoup(htmlContent, 'html.parser')
                htmlChapterHeader = bsContent.find_all('header', {"class": "entry-header"})[0].text

                titleText = [para.string  for para in bsContent.find_all('p') if para.string]
                titleText = titleText[0]
                titleText = titleText if titleText.count(':') else ''
            htmlChapterHeader = htmlChapterHeader.encode('utf-8', 'ignore')
            titleText = titleText.encode('utf-8', 'ignore')

            with open(fileName, 'rb') as aTxtChapter:
                chapterContent = aTxtChapter.read().replace('\n', '').split('.')
                for item in characterList:
                    firstOccurFlag = False
                    completeList={}

                    for sentence in chapterContent:
                        
                        # searching 2/3 of the word instead of the whole word
                        # but the results are not great
                        searchWord = item if len(item) < 20 else item[ : (len(item)*2/3)+1]  
                        
                        # searching only the word 
                        searchWord = item # if len(item) < 20 else item[ : (len(item)*2/3)+1]
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
                                completeList= OrderedDict([('book', dl.booksTamilNames.get(book, 'வெண்முரசு       ')),
                                                          ( 'chapter' , str(currentdate)), 
                                                          ( 'link' , '<a href = "http://www.venmurasu.in/'+str(currentdate).replace('-','/')+'" target="_blank" rel="noopener noreferrer" >click</a>'),
                                                          ( 'count' , sentence.count(item)),
                                                          ( 'sentence' , '.'.join(sentence3)),
                                                          ( 'header' , htmlChapterHeader),
                                              ])
                                if titleText:
                                    completeList['title'] = titleText
                                firstOccurFlag = True
                            else:
                                completeList['count'] += sentence.count(item)
                    try:
                        completeList['count'] = str(completeList['count'])
                    except:
                        pass

                    characItems[book][ item ].append(completeList) 
            currentdate += datetime.timedelta(days=1)    
    
        for item in characItems:
            for name in characterList:
                if characItems[item][name]:
                    for itm in characItems[item][name]:
                        for key, val in itm.items():
                            outStr += key +':\t\t'+str(val).strip() + '\n'
        outStr +="\n\n"
    return outStr  

def makeCharacterChapterList(characterList):
    
    conn = sqlite3.connect('test'+datetime.datetime.now().strftime("%d_%B_%Y_%I_%M_")+'.db')
    #print "Opened database successfully";
    
    for book in dl.books.keys():
        folder = dl.venmurasuFolder+'/'+book 
        collectionFolder = dl.venmurasuFolder.replace('content','results')+"/characters/"
        collectionFolderJSON = dl.venmurasuFolder.replace('content','results')+"/characters/json/"
        if not os.path.exists(collectionFolder):
            os.makedirs(collectionFolder, mode=0777)
        if not os.path.exists(collectionFolderJSON):
            os.makedirs(collectionFolderJSON, mode=0777)
        characterCollectionFile = collectionFolder+book+'_characters.txt'
        characterCollectionFileJSON = collectionFolderJSON+book+'_characters_json.txt'

        currentdate = getStartDate(book)
        enddate = getEndDate(book)
        #print 'Folder name: ',folder

        characItems = { book : OrderedDict({itm : [] for itm in characterList }) }

        while currentdate <= enddate:
            fileName = downloadVenmurasu.makeFileName(currentdate,folder, '.txt')
            
            htmlfileName = downloadVenmurasu.makeFileName(currentdate,folder, '.html')
            htmlChapterHeader = ""
            htmlChapterHeader, titleText = "", ""
            with open(htmlfileName, 'r') as htmlObj:
                htmlContent = htmlObj.read()
                bsContent = bs.BeautifulSoup(htmlContent, 'html.parser')
                htmlChapterHeader = bsContent.find_all('header', {"class": "entry-header"})[0].text

                titleText = [para.string  for para in bsContent.find_all('p') if para.string]
                titleText = titleText[0]
                titleText = titleText if titleText.count(':') else ''
            htmlChapterHeader = htmlChapterHeader.encode('utf-8', 'ignore')
            titleText = titleText.encode('utf-8', 'ignore')

            with open(fileName, 'rb') as aTxtChapter:
                chapterContent = aTxtChapter.read().replace('\n', '').split('.')
                for item in characterList:
                    firstOccurFlag = False
                    completeList={}

                    for sentence in chapterContent:
                        
                        # searching 2/3 of the word instead of the whole word
                        # but the results are not great
                        searchWord = item if len(item) < 20 else item[ : (len(item)*2/3)+1]  
                        
                        # searching only the word 
                        searchWord = item # if len(item) < 20 else item[ : (len(item)*2/3)+1]
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
                                completeList= OrderedDict([( 'chapter' , str(currentdate)), 
                                                          ( 'link' , 'www.venmurasu.in/'+str(currentdate).replace('-','/')),
                                                          ( 'count' , sentence.count(item)),
                                                          ( 'sentence' , '.'.join(sentence3)),
                                                          ( 'header' , htmlChapterHeader),
                                              ])
                                if titleText:
                                    completeList['title'] = titleText
                                firstOccurFlag = True
                            else:
                                completeList['count'] += sentence.count(item)
                    try:
                        completeList['count'] = str(completeList['count'])
                    except:
                        pass

                    characItems[book][ item ].append(completeList) 
            currentdate += datetime.timedelta(days=1)    

        with open( characterCollectionFileJSON, 'w') as collectFile:
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
                                outStr += tabStr + key + ':\t' + str(val).strip() + '\n'

                            outStr += '\n.......................................................\n'
                    outStr +='\n________________________________________________________\n'
                outStr +='\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
            collectFile.write( outStr )
    
        writeCharacterToDB(conn, characItems, characterList)
    conn.close()




def writeCharacterToDB(conn, characItems, characterList):
     

    conn.execute('''CREATE TABLE if not exists  CHARACTERSEARCH
             (ID            INTEGER PRIMARY KEY    NOT NULL,
             book           TEXT    NOT NULL,
             character      TEXT    NOT NULL,
             chapter        TEXT    NOT NULL,
             link           TEXT    NOT NULL,
             header         TEXT    NOT NULL,
             title          TEXT    NULL,
             sentence       TEXT    NOT NULL,
             count          TEXT    NOT NULL);''')

    conn.commit()


    for book in characItems:
        for name in characterList:
            for itm in characItems[book][name]:
                if itm:
                    rowDict = { 'book' : str(book), 'character': str(name), }
                    
                    for i in itm:
                        rowDict[i] = str(itm[i]).strip()
                    queryStr = "INSERT INTO CHARACTERSEARCH %s VALUES ("%(str(tuple(rowDict.keys())))
                    for val in rowDict.values():
                        queryStr += "'"
                        queryStr += str(val)
                        queryStr += "'"
                        queryStr += ', '
                    queryStr = queryStr[:-2]+');'
                    conn.execute( queryStr )
        conn.commit()

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
    #print 'Venmurasu keys: ', len(venDict.keys())
    venmurasuDBConnect.connectionCommit()


def makeConcise():
    venmurasuDBConnect = durusCommit(dl.venmurasuFolder, 'venmurasu')
    venRoot = venmurasuDBConnect.getRoot()

    #print 'Venmurasu keys: ', len(venRoot['Venmurasu'].keys())
    
    venDict = {i.strip() : {'count' : j} for i,j in venRoot['Venmurasu'].items() }
    venDict = OrderedDict(sorted(venDict.iteritems() , key= lambda x: x[1]['count'] ))
    
    for runNum in range(5):
        #print "This is run : ", runNum
        venNew = {}
        for i in venDict:
            count = 0
            venTemp = copy.deepcopy(venNew)
            for k in venTemp:
                if (len(k) < len(i)) and ( i.count(k) and i.index(k)==0 ) : # or ( len(k) > 20 and i.count(k[: (len(k)*(2/3))+1]) )):
                    venNew[k]['count'] +=venDict[i].get('count')  
                    if venNew.get(k).get('aggregate'):
                        venNew[k]['aggregate'].append(i)
                    else:
                        venNew[k]['aggregate'] = [i]
                    
                    if venDict[i].get('aggregate'):
                        venNew[k]['aggregate'].extends(venDict[i].get('aggregate'))
                    
                    count += 1
            if not count:
                venNew[i] = {'count' : venDict[i]['count']}

            #save every 10000 words 
            if len(venNew) % 10000 == 0:
                #print len(venNew)
                with open( 'concise.csv' , 'w') as fileOut:
                    for itm in venNew:
                        if venNew[itm].get('aggregate') :
                            strOut = ', '.join([itm, str(venNew[itm]['count']), '['+ '|'.join(venNew[itm]['aggregate']) + ']'])
                        else:
                            strOut = ', '.join([itm, str(venNew[itm]['count']), ''])
                        fileOut.write( strOut + '\n' )
        venDict = venNew


      
    venmurasuNewDB = durusCommit(dl.venmurasuFolder, 'venmurasuConcise')
    venRoot = venmurasuNewDB.getRoot()
    venRoot['Venmurasu'] = venNew
    #print 'Venmurasu keys: ', len(venDict.keys())
    venmurasuDBConnect.connectionCommit()
    

def writeToFileVenmurasuWords():
    venmurasuDBConnect = durusCommit(dl.venmurasuFolder, 'venmurasu')
    venRoot = venmurasuDBConnect.getRoot()
    venDict = venRoot['Venmurasu']
    
    with open( dl.venmurasuFolder+'/words.csv', 'w') as fileOut:
        for k, j in venDict.items():
            fileOut.write( k+','+j+'\n'  )

def consolidateWordsForBook(connect, book):
    #print " Book: ", book, " --- "
    bookDict = {}
    bookRoot = connect.getRoot()
    folder = dl.venmurasuFolder+"/"+book
    currentdate = getStartDate(book)
    enddate = getEndDate(book)
    #print 'Folder name: ',folder
    
    while currentdate <= enddate:
        collectChapter(currentdate, book, folder, connect)
        chapterDateTuple = tuple(currentdate.strftime('%Y-%m-%d').split('-'))
        #print chapterDateTuple, len(bookRoot[book][chapterDateTuple]['wordsDict'].keys())
        for word in bookRoot[book][chapterDateTuple]['wordsDict'].keys():
            if word in bookDict:
                bookDict[word] += bookRoot[book][chapterDateTuple]['wordsDict'][word]
            else:
                bookDict[word] = bookRoot[book][chapterDateTuple]['wordsDict'][word]
        currentdate += datetime.timedelta(days=1)
    #print "Book unique words: ", len(bookRoot[book][book].keys())
    bookRoot[book][book] = bookDict
    connect.connectionCommit()


def collectChapter(currentdate, book, folder, connect):
    checkRoot = connect.getRoot()
    #print "Chapter : ", currentdate
    dateTuple = tuple(currentdate.strftime('%Y-%m-%d').split('-'))
    if checkRoot.get(book) and dateTuple in checkRoot[book]:
        chapterDict = checkRoot[book][dateTuple]
    else:
        chapterDict = makeChapterDict(currentdate, folder)
    #print chapterDict
    if not isinstance(chapterDict, str):
        commitChapterWord(connect, currentdate, book, chapterDict)
    mergeChapterWordsInToBook(currentdate, book, folder, connect)

def mergeChapterWordsInToBook(currentdate, book, folder, connect):
    bookRoot = connect.getRoot()
    
    if not bookRoot.get(book).get(book):
        bookRoot[book][book] = {}
    bookDict = bookRoot.get(book).get(book)

    chapterDateTuple = tuple(currentdate.strftime('%Y-%m-%d').split('-'))
    for key in bookRoot[book][chapterDateTuple]['wordsDict'].keys():
        if key in bookDict:
            bookDict[key] += bookRoot[book][chapterDateTuple]['wordsDict'][key]
        else:
            bookDict[key] = bookRoot[book][chapterDateTuple]['wordsDict'][key]
    bookRoot[book][book] = bookDict
    connect.connectionCommit()
    
if __name__ == '__main__':
    #completeConsolidateVenmurasu() 
    #getVenmurasuWords()
    #makeConcise()
    
    start = time.time()
    #makeCharacterChapterList(characterList)
    #makeBookAndTitle()
    #makeAllBooks()
    makeNeoThamizhan()
    stop = time.time()
    print stop - start
