from collections import OrderedDict

print "Gurubhyo Namaha"

books = OrderedDict([('Mudharkanal', [(2014, 1, 1), (2014, 2, 19)]), 
             ('Mazhaipadal', [(2014, 2, 24), (2014, 5, 26)]),
             ('Vannakadal', [(2014, 6, 1), (2014, 8, 10)]),
             ('Neelam', [(2014, 8, 20), (2014, 9, 26)]),
             ('Prayagai', [(2014, 10, 20), (2015, 1, 19)]),
             ('VenmugilNagaram', [(2015, 2, 1), (2015, 2, 20)]),
             ]
            )

for aKey in books.keys():
    print aKey, books[aKey]
    