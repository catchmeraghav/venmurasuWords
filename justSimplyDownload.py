#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import datetime
import pprint
import concurrent.futures
from functools import partial
import time
import os
from bs4 import BeautifulSoup

import urllib
urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'

from constants import venmurasufolder
from constants import jeyamohanfolder
from constants import books
from constants import booksTamilNames
from constants import venmurasuInText

createFolders = True
downloadFromJeyamohan = True


def calculateNumberOfEpisodes():
    total = 0
    print "Book\t\t\t\t", "StartDate\t\t", "EndDate\t\t", "Episodes"
    for key, val in books.items():
        endDate = datetime.date(val[1][0], val[1][1], val[1][2])
        startDate = datetime.date(val[0][0], val[0][1], val[0][2])
        delta = endDate - startDate 
        print key,"\t\t\t\t", startDate.strftime('%d-%m-%Y\t\t'), endDate.strftime("%d-%m-%Y\t\t"), delta.days +1, " episodes"
        total += delta.days+1

    print total, " episodes"
    return total

def makeVenmurasuLinks():
    completeLinks = []
    for key, val in books.items():
        endDate = datetime.date(val[1][0], val[1][1], val[1][2])
        startDate = datetime.date(val[0][0], val[0][1], val[0][2])
        currentDate = startDate
        while currentDate <= endDate:
            fileName = currentDate.strftime('%Y-%m-%d.html')
            if createFolders:
                fileName = os.path.join( venmurasufolder, key, currentDate.strftime('%Y-%m-%d.html'))
            linkName = currentDate.strftime('http://venmurasu.in/%Y/%m/%d')
            completeLinks.append( (linkName, fileName, currentDate))
            currentDate += datetime.timedelta(days=1)
    print len(completeLinks)
    return completeLinks

def downloadDateHTMLFromJeyamohan():
    start = time.time()
    completeLinks = []
    for key, val in books.items():
        print key
        tempLinks = []
        endDate = datetime.date(val[1][0], val[1][1], val[1][2])
        startDate = datetime.date(val[0][0], val[0][1], val[0][2])
        currentDate = startDate
        while currentDate <= endDate:
            tempfileName = currentDate.strftime('%Y-%m-%d.html')
            url = currentDate.strftime('http://jeyamohan.in/date/%Y/%m/%d')
            tempLinks.append( (url, tempfileName, currentDate))
            currentDate += datetime.timedelta(days=1)
        
        def downloadTempFiles(inputVal ):
            url, folderFileName, currentDate = inputVal[0], inputVal[1], inputVal[2]

            counter = 0
            while not os.path.isfile(folderFileName) or ( os.path.isfile(folderFileName) and os.path.getsize(folderFileName) < 102400 and counter < 3):
                print "\nDownloading - Jeyamohan Date -- ", url, folderFileName, "-- counter -- ", counter,"\n"
                urllib.urlretrieve (url, folderFileName)
                counter+=1
                    
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            executor.map( downloadTempFiles, tempLinks )
    stop = time.time()
    print "Downloaded all from Jeyamohan.in -- ", stop - start, " seconds"


def makeVenmurasuFromJeyamohanLinks():
    print "now downloading html of venmurasu by date in jeyamohan.in - it has links to venmurasu episodes"
    downloadDateHTMLFromJeyamohan()
    print "some files might be missed because of threading"
    downloadDateHTMLFromJeyamohan()
    print "now third time is the charm"
    downloadDateHTMLFromJeyamohan()
    print "starting to sleep"
    start = time.time()
    
    completeLinks = []
    for key, val in books.items():

        endDate = datetime.date(val[1][0], val[1][1], val[1][2])
        startDate = datetime.date(val[0][0], val[0][1], val[0][2])
        currentDate = startDate
        
        while currentDate <= endDate:
            linkName = ''
            tempfileName = currentDate.strftime('%Y-%m-%d.html')
            fileName = currentDate.strftime('%Y-%m-%d.html')
            if createFolders:
                fileName = os.path.join( jeyamohanfolder, key, currentDate.strftime('%Y-%m-%d.html'))

            soup = BeautifulSoup(open(tempfileName), "html.parser")
            counter = 0
            for elem in soup.find_all():
                linkText = elem.text.encode('utf-8').replace("'"," ").replace("‘"," ").replace("’"," ").replace("–", " ")
                if elem.name == 'a' and elem.text.strip() and venmurasuInText in linkText and booksTamilNames[key] in linkText:
                    linkName = elem['href']
                    completeLinks.append( (linkName, fileName, currentDate))
                    #print linkName, fileName, currentDate
                    break
            if not linkName:
                print "\n\n\n", currentDate, "\n\n\n"
            #os.remove(tempfileName)
            currentDate += datetime.timedelta(days=1)
    stop = time.time()
    print "Extracted all links from Jeyamohan.in -- ", stop - start, " seconds"
    print len(completeLinks)
    return completeLinks

def downloadOneLinkFileName( inputVal ):
    url, folderFileName, currentDate = inputVal[0], inputVal[1], inputVal[2]

    counter = 0
    while not os.path.isfile(folderFileName) or ( os.path.isfile(folderFileName) and os.path.getsize(folderFileName) < 10000 and counter < 3):
        print "\nDownloading -- ", url, folderFileName, "-- counter -- ", counter,"\n"
        urllib.urlretrieve (url, folderFileName)
        counter+=1

    if 'venmurasu' in folderFileName and currentDate > datetime.date(2013, 12, 31) and currentDate < datetime.date(2014, 2, 27):
        fl = open(folderFileName, 'rb')
        for line in fl:
            if 'more-link' in line and "href" in line:
                url = line.split('href')[1].split('"')[1]
                url = url.split('/#')[0]
                fl.close()
                del(fl)

                print "\nDownloading AGAIN --", url, folderFileName, "\n"
                urllib.urlretrieve (url, folderFileName)

                break

    if 'jeyamohan' in folderFileName:
        counter = 0
        while not os.path.isfile(folderFileName) or ( os.path.isfile(folderFileName) and os.path.getsize(folderFileName) < 10000 and counter < 3):
            print "\nDownloading Jeyamohan.in -- ", url, folderFileName, "-- counter -- ", counter,"\n"
            urllib.urlretrieve (url, folderFileName)
            counter+=1


def createBookFolders(completeLinks):
    for itm in completeLinks:
        folderName = '/'.join(itm[1].split('/')[:-1])
        if not os.path.exists(folderName):
            print 'creating folder', folderName
            os.makedirs(folderName, mode=0777)

def simultaneousDownload(createFolders = createFolders):
    start = time.time()
    completeLinks = makeVenmurasuLinks()
    
    if downloadFromJeyamohan:
        jLinks = makeVenmurasuFromJeyamohanLinks()
        completeLinks.extend(jLinks)

        #print "\n\n\n\n\n\n\n"
        #print completeLinks
        #print "\n\n\n\n\n\n\n"

    if createFolders:
        createBookFolders(completeLinks)
    print "\n\n\n"
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map( downloadOneLinkFileName, completeLinks)
    print "\n\n\n"
    time.sleep(15)
    print "\n\n\n"
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map( downloadOneLinkFileName, completeLinks)
    print "\n\n\n"
    time.sleep(15)
    print "\n\n\n"
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map( downloadOneLinkFileName, completeLinks)
    print "\n\n\n"

    stop = time.time()
    print stop-start, ' - seconds'

if __name__ == "__main__":
    calculateNumberOfEpisodes()

    print "starting to download ... "
    simultaneousDownload()
