#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
*
* 20 Feb 2015
* This file is used to download the data from http://www.venmurasu.in
* Also attempting to download the images if available
* And making the html files access the images locally instead of the href
*
* This will be the first step, as this downloads the data, needed to parse
* Lets see how it goes about
*
'''

import datetime
import urllib
import fileinput
import sys
import os
from collections import OrderedDict
from bs4 import BeautifulSoup


from constants import venmurasufolder
from constants import jeyamohanfolder
from constants import books
from constants import booksTamilNames

class downloadVenmurasu(object):
    ''' 
    A origin or kickstart class
    Basic functionality is to download chapter and recursively books
    Further download images - if available and map them to local HTML
    
    writing this as a very generic class without any specific class variable
     
    '''
    
    def __init__(self):
        '''
        init of downloadVenmurasu
        writing this as a very generic class without any specific class variable
        '''
        global books
        global booksTamilNames
                
        self.books = books
        self.venmurasuFolder = venmurasufolder
        self.booksTamilNames = booksTamilNames

    def setVenmurasuFolder(self, folderName):
        self.venmurasuFolder = folderName

    def replaceSrc(self, currentdate, folder, replaceTxt):
        aChapter = self.makeFileName(currentdate, folder)
        for line in fileinput.input(aChapter, inplace=1):
            if "size-large wp-image" in line:
                oldLine = "<!-- "+ line + " -->"
                ln = line.split('src=')[0]
                ln2= line.split('src=')[1].split('"')
                ln2[1]=replaceTxt
                ln2 = '"'.join(ln2)
                line = 'src='.join([ln,ln2])
                line = line+"\n"+oldLine
            sys.stdout.write(line)
    
    @staticmethod        
    def makeFileName(currentdate, folder, extn='.html'):
        if isinstance(currentdate, tuple):
            currentdate = datetime.date(currentdate[0], currentdate[1], currentdate[2])
        fileName = currentdate.strftime('%Y-%m-%d')+extn
        return os.path.join(folder, fileName)

                
    def downloadChapterImage(self, imgDate, folder):
        imgName = imgDate.strftime('%Y-%m-%d')
        normalImgName = os.path.join(folder,imgName)
        bigImgName = os.path.join(folder,'big-'+imgName)
        
        if (os.path.exists(bigImgName) or os.path.exists(normalImgName)):
            pass
        else:
            folderFileName = self.makeFileName(imgDate, folder)
            imgFilesList = []
            with open(folderFileName, 'rb') as fl:
                for line in fl:
                    if ('<img' in line and "wp-image" in line) or ('<img' in line and ".jpg" in line):
                        img = line.split('src=')[1].split('"')[1]
                        img = img.split('?')[0] if '?' in img else img
                        #urllib.urlretrieve (img, normalImgName)
                        imgFilesList.append(img)
                        imgBig = line.split('href=')[1] if 'href'in line else None
                        if imgBig: 
                            imgBig = '' if '.jpg' not in imgBig else imgBig.split('"')[1]
                            if imgBig =='':
                                continue
                            #urllib.urlretrieve (imgBig, bigImgName) 
                            imgFilesList.append(imgBig)
                        #urllib.urlretrieve (imgBig, bigImgName)
            counter=0
            for imgItm in imgFilesList:
                urllib.urlretrieve (imgBig, imgName+'_'+str(counter)+'.jpg')
                counter+=1
            #if os.path.exists(bigImgName):
            #    self.replaceSrc(imgDate, folder, bigImgName)
            #    ##print imgName
            #elif os.path.exists(normalImgName):
            #    self.replaceSrc(imgDate, folder, normalImgName)
            #    ##print imgName
        
    def downloadChapter(self, currentdate, folder):

        folderFileName = self.makeFileName(currentdate, folder)
        if not (os.path.exists(folderFileName) and os.path.isfile(folderFileName)) :
            url = 'http://venmurasu.in/'+currentdate.strftime('%Y/%m/%d')
            urllib.urlretrieve (url,folderFileName)
            if currentdate > datetime.date(2013, 12, 31) and currentdate < datetime.date(2014, 5, 27):
                fl = open(folderFileName, 'rb')
                for line in fl:
                    if 'more-link' in line and "href" in line:
                        url = line.split('href')[1].split('"')[1]
                        url = url.split('/#')[0]
                        #print "The correct url:\n",url
                        fl.close()
                        del(fl)
                        urllib.urlretrieve (url,folderFileName)
                        break
    
    def downloadChapterFromJeyamohanDotIn(self, currentdate, folder):
        folderFileName = self.makeFileName(currentdate, folder)
        if not (os.path.exists(folderFileName) and os.path.isfile(folderFileName)) :
            url = 'http://jeyamohan.in/date/'+currentdate.strftime('%Y/%m/%d')
            urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
            urllib.urlretrieve (url,folderFileName)
            soup = BeautifulSoup(open(folderFileName), "html.parser")
            for elem in soup.find_all('a', href=True):
                if elem.name == 'a' and "‘வெண்முரசு’ –" in elem.text.encode('utf-8'):
                    url = elem['href']
                    break
            os.remove(folderFileName)
            urllib.urlretrieve (url,folderFileName)


    def downloadBook(self, startDate, stopDate, folder, image=True, text=True, makeWordDict=True):
        currentdate = datetime.date(startDate[0], startDate[1], startDate[2])
        enddate = datetime.date(stopDate[0], stopDate[1], stopDate[2])
        while currentdate <= enddate:
            #self.downloadChapter(currentdate, folder)
            self.downloadChapterFromJeyamohanDotIn(currentdate, folder)
            ##print 'Date: ', currentdate.strftime('%Y-%m-%d')
            if image:
                self.downloadChapterImage(currentdate, folder)
                ##print 'Image: ',image
                    
            currentdate += datetime.timedelta(days=1)
    
    def theStart(self, image=True, text=True, makeWordDict=True):
        #Loop on the books. If the folder does not exist create and start downloading
        for aKey in self.books.keys():
            fldr = self.venmurasuFolder+"/"+aKey
            if not os.path.exists(fldr):
                os.makedirs(fldr, mode=0777)


    
                                
if __name__=="__main__":
    #Download the entire Venmurasu - required for start of work
     
    dl = downloadVenmurasu()
    #dl.thestart() #this simply does everything. Will write a separate script to do everything 
    #dl.theStart(image=True, text=False) # does not download image and does not convert HTMLto Text
    
    #Download the required number chapters or just one chapter
    #dl.downloadChapter((2015, 2, 21),(2015, 2, 21),"/home/raghav/Desktop/venmurasuBooks/VenmugilNagaram/")
    
    
