#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
*
* 21 Feb 2015
* This file is used to read HTML and convert to text file with the data from http://www.venmurasu.in
* 
*
'''
import datetime

class parseHTMLToTamilTxt:
    def __init__(self):
        self.venmurasuFolder = "/home/raghav/Desktop/venmurasuBooks/VenmugilNagaram"

    def formatFileNameFromDate(self, chapterDate, currentBookFolder = ""):
        if isinstance(chapterDate, datetime):
            chapterDate = chapterDate.strftime('%Y-%m-%d').split('-')
        if not currentBookFolder:
            currentBookFolder = self.venmurasuFolder
        fileName = '-'.join(currentBookFolder)+'.html'
        self.convertHtmlToText(currentBookFolder+"/"+fileName)

    def convertHtmlToText(self, htmlFileName):
        textFileName = htmlFileName.replace('.html','.txt')
        with open(textFileName, 'w') as textFile:
            with open(htmlFileName, 'rb') as htmlFile:
                for aHTMLLine in htmlFile.xreadlines():
                    
                    if '<p' in aHTMLLine or '<h1' in aHTMLLine:
                        aHTMLLine = aHTMLLine.replace('</h1>','').replace('</p>','').replace('<strong>','').replace('<em>','').replace('</em>','').replace('</strong>','').split('>')[1].strip()
                        flag = False
                        for exceptWd in ['<', '>', 'Inbox', 'Join']:
                            if exceptWd in aHTMLLine:
                                flag = True
                                break
                        
                        if not flag:
                            if '<p' in aHTMLLine:
                                aHTMLLine = aHTMLLine.replace('</p>','').split('>')[1].strip()
                                flag = False
                                for exceptWd in ['<', '>', 'Inbox', 'Join']:
                                    if exceptWd in aHTMLLine:
                                        flag = True
                                        break
                                
                                if not flag:
                                    exceptLine = ''
                                    
                                    sentenceTamil = aHTMLLine
                                    if exceptLine != sentenceTamil:
                                        textFile.write(sentenceTamil)
                                        textFile.write('\n')
                                    else:
                                        print sentenceTamil
                                        print "Match!"
                    

if __name__ == "__main__":
    chapterDate = datetime.date(2015, 2, 21)
    
    prse = parseHTMLToTamilTxt()
    prse.formatFileNameFromDate((2015, 2, 21))
    
