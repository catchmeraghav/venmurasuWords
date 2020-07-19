#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
*
* 21 Feb 2015
* This file is used to read HTML and convert to text file with the data from http://www.venmurasu.in
*
'''
import datetime
import os
import bs4 as bs
import codecs
htmlCodeToTxt = {'&#32;':' ',
                '&#33;':'!',
                '&#34;':'"',
                '&#35;':'#',
                '&#36;':'$',
                '&#37;':'%',
                '&#38;':'&',
                '&#39;':'\'',
                '&#40;':'(',
                '&#41;':')',
                '&#42;':'*',
                '&#43;':'+',
                '&#44;':',',
                '&#45;':'-',
                '&#46;':'.',
                '&#47;':'/',
                '&#58;':':',
                '&#59;':';',
                '&#60;':'<',
                '&#61;':'=',
                '&#62;':'>',
                '&#63;':'?',
                '&#91;':'[',
                '&#92;':'\\',
                '&#93;':']',
                '&#94;':'^',
                '&#95;':'_',
                '&#8211;':'–',
                '&#8212;':'—',
                '&#8216;':'‘',
                '&#8217;':'’',
                '&#8218;':'‚',
                '&#8220;':'“',
                '&#8221;':'”',
                '&#8222;':'„',
                '&#8224;':'†',
                '&#8225;':'‡',
                '&#8226;':'•',
                '&#8230;':'…',
                '&#8240;':'‰',
                '&#8364;':'€',
                '&#8482;':'™',
                '&nbsp' : ' '
                }
stopEndText = ( 'அனைத்து வெண்முரசு விவாதங்களும்',
                'மகாபாரத அரசியல் பின்னணி வாசிப்புக்காக',
                'வெண்முரசு வாசகர் விவாதக்குழுமம்',
                'Posted in'
              )
class parseHTMLToTamilTxt:
    def __init__(self):
        self.venmurasuFolder = "/home/raghav/Desktop/venbooks/VenmugilNagaram"
        self.chapterDate = '-'.join(['2015','02','21'])
        self.currentBookFolder = ""
        
    def convertChapterToText(self, chapterDate='', currentBookFolder=''):
        htmlFileName = self.formatFileNameFromDate(chapterDate, currentBookFolder)
        if htmlFileName:
            return self.convertUsingBS(htmlFileName)
            return self.convertVenmurasuHtmlToText(htmlFileName)
        return False        

    def formatFileNameFromDate(self, chapterDate, currentBookFolder = ""):
        'Format the filename, to be accessed and to be converted to text'
        
        if isinstance(chapterDate, tuple):
            chapterDate = datetime.date(chapterDate[0], chapterDate[1], chapterDate[2])
        if isinstance(chapterDate, datetime.date):
            self.chapterDate = chapterDate.strftime('%Y-%m-%d')    
            
        if currentBookFolder:
            self.currentBookFolder = currentBookFolder
        else:
            self.currentBookFolder = self.venmurasuFolder
            
        fileName = self.currentBookFolder+'/'+self.chapterDate+'.html'
        
        if os.path.exists(fileName):
            return fileName
        return False

    def convertVenmurasuHtmlToText(self, htmlFileName):
        '''
        *
        * Convert a given HTML file, in a folder, to a text file fetching just the Tamil content
        *
        * Writing a bad code, specific for fetching Tamil content from venmurasu.in
        *
        * I hope to write code very generic to get Tamil page content of any webpage
        *
        '''
        
        textFileName = htmlFileName.replace('.html','.txt')
        with open(textFileName, 'w') as textFile:
            with open(htmlFileName, 'rb') as htmlFile:
                for aHTMLLine in htmlFile.xreadlines():
                    if '<p' in aHTMLLine or '<h1' in aHTMLLine:
                        aHTMLLine = aHTMLLine.replace('</h1>','').replace('</p>','').replace('<strong>','').replace('<em>','').replace('</em>','').replace('</strong>','').split('>')[1].strip()
                        
                        for aKey in htmlCodeToTxt.keys():
                            if aKey in aHTMLLine:
                                aHTMLLine = aHTMLLine.replace(aKey, htmlCodeToTxt[aKey])
                        flag = False
                        for exceptWd in ['<', '>', 'Inbox', 'Join']:
                            if exceptWd in aHTMLLine:
                                flag = True
                                break        
                        ignore_lines = ['Post navigation',
                                         'பின்னூட்டங்கள் மூடப்பட்டுள்ளது.',
                                         'உங்கள் மின்னஞ்சல் இங்கே கொடுத்து அதன் வழி பதிவுகளைப் பெறவும்.',
                                         'வெண்முரசு அனைத்து விவாதங்களும்',
                                         'மகாபாரத அரசியல் பின்னணி வாசிப்புக்காக',
                                         'வெண்முரசு வாசகர் விவாதக்குழுமம்',
                                        ]

                        for itm in ignore_lines:
                            aHTMLLine.encode('utf-8').decode('utf-8').replace(itm.encode('utf-8').decode('utf-8'), '' )

                        sentenceTamil = aHTMLLine
                        textFile.write(sentenceTamil)
                        textFile.write('\n')
        return True
 
    def convertUsingBS(self, htmlFileName):
        '''
        *
        * Convert a given HTML file, in a folder, to a text file fetching just the Tamil content
        *
        * Writing a bad code, specific for fetching Tamil content from venmurasu.in
        *
        * I hope to write code very generic to get Tamil page content of any webpage
        *
        '''
        
        textFileName = htmlFileName.replace('.html','.txt')
        with codecs.open(textFileName, 'w', 'utf8') as textFile:
            with open(htmlFileName, 'rb') as htmlFile:
                htmlContent = htmlFile.read()
                soup = bs.BeautifulSoup(htmlContent,'lxml')
                text = []
                episodeFlag = False
                for paragraph in soup.find_all('p'):
                    txt = paragraph.string
                    if txt:
                        txt = txt.strip()
                        for aKey in htmlCodeToTxt.keys():
                            if aKey in text:
                                txt = txt.replace(aKey, htmlCodeToTxt[aKey])
                        text.append( txt )
                    if episodeFlag:
                        break
                text = '\n'.join( text )
                textFile.writelines(text)
                textFile.write('\n')
        return True                                       
if __name__ == "__main__":
    chapterDate = datetime.date(2015, 2, 27)
    
    prse = parseHTMLToTamilTxt()
    print prse.convertChapterToText((2015, 2, 27))
