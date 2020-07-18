#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from collections import OrderedDict

folder = '../venbooks'
if not os.path.exists(folder):
    os.makedirs(folder, mode=0777)

venmurasufolder = os.path.join(folder, 'venmurasu_in')
jeyamohanfolder = os.path.join(folder, 'jeyamohan_in')
imagefolder = os.path.join(folder, 'images')

venmurasuInText = 'வெண்முரசு '

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
                     ('PanniruPadaikaLam',[(2016,03,26),(2016,06,22)]),
                     ('Solvalarkadu',[(2016,07,20),(2016,9,17)]),
                     ('Kraatham',[(2016,10,20),(2017,1,10)]),
                     ('Maamalar',[(2017,2,1),(2017,5,6)]),
                     ('Neerkolam',[(2017,5,25),(2017,8,29)]),
                     ('Ezhuthazhal', [(2017,9,15),(2017,12,2)]),
                     ('Kuruthisaral', [(2017,12,17),(2018,3,5)]),
                     ('Imaikanam', [(2018,3,25),(2018,5,16)]),
                     ('Sennavengai', [(2018,6,1),(2018,8,21)]),
                     ('ThisaitherVellam', [(2018,9,10),(2018,11,28)]),
                     ('Karkadal',[(2018,12,25),(2019,3,22)]),
                     ('Irutkani',[(2019,4,10),(2019,6,14)]),
                     ('TheeyinEdai',[(2019,7,1),(2019,8,26)]),
                     ('Neersudar', [(2019,9,15),(2019,11,15)]),
                     ('KalitrruYanaiNirai', [(2019,12,1),(2020,2,18)]),
                     ('Kalporusirunurai', [(2020,3,15),(2020,6,9)]),
                     ('MudhalaVin', [(2020,7,1),(2020,7,16)]),
                   ])

booksTamilNames = {
                    'Mudharkanal' : 'முதற்கனல்',
                    'Mazhaipadal' : 'மழைப்பாடல்',
                    'Vannakadal' : 'வண்ணக்கடல்',
                    'Neelam' : 'நீலம்',
                    'Prayagai' : 'பிரயாகை',
                    'VenmugilNagaram' : 'வெண்முகில் நகரம்',
                    'Indraneelam' : 'இந்திரநீலம்',
                    'Kandeepam' : 'காண்டீபம்',
                    'Veyyon' : 'வெய்யோன்',
                    'PanniruPadaikaLam' : 'பன்னிரு படைக்களம்',
                    'Solvalarkadu' : 'சொல்வளர்காடு',
                    'Kraatham' : 'கிராதம்',
                    'Maamalar' : 'மாமலர்',
                    'Neerkolam' : 'நீர்க்கோலம்',
                    'Ezhuthazhal' : 'எழுதழல்',
                    'Kuruthisaral' : 'குருதிச்சாரல்',
                    'Imaikanam' : 'இமைக்கணம்',
                    'Sennavengai' : 'செந்நா வேங்கை',
                    'ThisaitherVellam' : 'திசைதேர் வெள்ளம்',
                    'Karkadal' : 'கார்கடல்',
                    'Irutkani' : 'இருட்கனி',
                    'TheeyinEdai' : 'தீயின் எடை',
                    'Neersudar' : 'நீர்ச்சுடர்',
                    'KalitrruYanaiNirai' : 'களிற்றியானை நிரை',
                    'Kalporusirunurai' : 'கல்பொருசிறுநுரை',
                    'MudhalaVin' : 'முதலாவிண்',
                  }                        


