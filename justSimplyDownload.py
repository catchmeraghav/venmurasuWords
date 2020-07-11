from collections import OrderedDict
import datetime
import pprint
import concurrent.futures
from functools import partial
import urllib
import time
import os

from constants import venmurasufolder
from constants import books
from constants import booksTamilNames
source = venmurasufolder
createFolders = True

def calculateNumberOfEpisodes():
    total = 0
    for key, val in books.items():
        endDate = datetime.date(val[1][0], val[1][1], val[1][2])
        startDate = datetime.date(val[0][0], val[0][1], val[0][2])
        delta = endDate - startDate 
        print key,"\t\t", delta.days +1, " episodes"
        total += delta.days+1

    print total, " episodes"
    return total

def makeVenmurasuLinks(source = source):
    completeLinks = []
    for key, val in books.items():
        endDate = datetime.date(val[1][0], val[1][1], val[1][2])
        startDate = datetime.date(val[0][0], val[0][1], val[0][2])
        currentDate = startDate
        while currentDate <= endDate:
            fileName = os.path.join(source, currentDate.strftime('%Y-%m-%d-.html'))
            if createFolders:
                fileName = os.path.join(source, key, currentDate.strftime('%Y-%m-%d-.html'))
            linkName = currentDate.strftime('http://venmurasu.in/%Y/%m/%d')
            completeLinks.append( (linkName, fileName, currentDate) )
            currentDate += datetime.timedelta(days=1)
    print len(completeLinks)
    return completeLinks

def downloadOneLinkFileName( inputVal ):
    url, folderFileName, currentDate = inputVal[0], inputVal[1], inputVal[2]

    counter = 0
    while not os.path.isfile(folderFileName) or ( os.path.isfile(folderFileName) and os.path.getsize(folderFileName) < 10000 and counter < 3):
        print "\nDownloading -- ", url, folderFileName, "\n"
        urllib.urlretrieve (url, folderFileName)
        counter+=1

    if 'venmurasu' in source and currentDate > datetime.date(2013, 12, 31) and currentDate < datetime.date(2014, 2, 27):
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

    if 'jeyamohan' in source:
        pass

def createBookFolders(completeLinks):
    for itm in completeLinks:
        folderName = '/'.join(itm[1].split('/')[:-1])
        if not os.path.exists(folderName):
            print 'creating folder', folderName
            os.makedirs(folderName, mode=0777)

def simultaneousDownload(createFolders = createFolders):
    start = time.time()
    completeLinks = makeVenmurasuLinks()

    if createFolders:
        createBookFolders(completeLinks)
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
