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
import bs4 as bs

venmurasuFolder = "/home/raghav/Desktop/venmurasuWords/venbooks/content"
#venmurasuFolder = "C:\\Users\\Rajasimhan\\Desktop\\venbooks"
books = OrderedDict([
                     ('Mudharkanal', [(2014, 1, 1), (2014, 2, 19)]), 
                     ('Mazhaipadal', [(2014, 2, 24), (2014, 5, 26)]),
                     ('Vannakadal', [(2014, 6, 1), (2014, 8, 10)]),
                     ('Neelam', [(2014, 8, 20), (2014, 9, 26)]),
                     ('Prayagai', [(2014, 10, 20), (2015, 1, 19)]),
                     ('VenmugilNagaram', [(2015, 2, 1), (2015, 5, 2)]),
                     ('Indraneelam', [(2015,6,1), (2015,8,31)]), 
                     ('Kandeepam', [(2015,9,15), (2015,11,27)]),
                     ('Veyyon',[(2015,12,20),(2016,3,6)]),
                     ('PanniruPadaikaLam',[(2016,3,26),(2016,6,22)]),
                     ('Solvalarkadu',[(2016,07,20),(2016,9,17)]),
                     ('Kraatham',[(2016,10,20),(2017,1,10)]),
                     ('Maamalar',[(2017,2,1),(2017,5,6)]),
                     ('Neerkolam',[(2017,5,25),(2017,8,29)]),
                     ('Ezhuthazhal', [(2017,9,15),(2017,12,2)]),
                     ('Kuruthisaral', [(2017,12,17),(2018,3,5)]),
                     ('Imaikanam', [(2018,3,25),(2018,5,16)]),
                     ('Sennavengai', [(2018,6,1),(2018,8,21)]),
                     ('ThisaitherVellam', [(2018,9,10),(2018,11,28)]),
                     ('Kaarkadal',[(2018,12,25),(2019,3,22)]),
                     ('Irutkani',[(2019,4,10),(2019,6,14)]),
                     ('TheeyinEdai',[(2019,7,1),(2019,8,26)]),
                     ('Neersudar', [(2019,9,15),(2019,10,05)]),
                        ])
#'''
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
        global venmurasuFolder
        self.books = books
        self.venmurasuFolder = venmurasuFolder
        
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
                contentImg = fl.read()
                soup = bs.BeautifulSoup(contentImg, 'html.parser')
                images = soup.findAll('img')
                imagesList = []
                for image in images:
                    imgLnk = image['src'].split('?')[0]
                    if not ('venmurasu' in imgLnk or 'jeyamohan' in imgLnk) :
                        continue
                    imagesList.append( imgLnk )

                print imagesList
                counter=0
                for imgItm in imagesList:
                    urllib.urlretrieve (imgItm, imgName+'_'+str(counter)+'.jpg')
                    counter+=1
        
    def downloadChapter(self, currentdate, folder):
        folderFileName = self.makeFileName(currentdate, folder)
        if not os.path.exists(folderFileName):
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
                
    def downloadBook(self, startDate, stopDate, folder, image=False, text=True, makeWordDict=True):
        currentdate = datetime.date(startDate[0], startDate[1], startDate[2])
        enddate = datetime.date(stopDate[0], stopDate[1], stopDate[2])
        while currentdate <= enddate:
            self.downloadChapter(currentdate, folder)
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
    
    
