import webapp2
import os
import csv
from google.appengine.ext import ndb

class Asxdata(ndb.Model):
    """Sub model for representing an stock price entry."""
    code = ndb.StringProperty()
    date = ndb.StringProperty()
    open = ndb.StringProperty(indexed=False)
    high = ndb.StringProperty(indexed=False)
    low = ndb.StringProperty(indexed=False)
    close = ndb.StringProperty(indexed=False)
    volume = ndb.StringProperty(indexed=False)
			
class LoadStocks(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Doing the loading!')

        filecount = 0
        totalcount = 0
        for filename in os.listdir(os.path.join(os.path.dirname(__file__))):
            counter = 0
            if filename.endswith(".txt"):
                filecount = filecount + 1			
                self.response.out.write("\n")					
                self.response.write(filename)
                inputfile = os.path.join(os.path.dirname(__file__), filename)
                reader = csv.reader(open(inputfile, 'rb'), delimiter=',', quotechar='"')

                for row in reader:
                    asx_key_value = row[0] + row[1]
                    asx_key = ndb.Key(Asxdata, asx_key_value)
                    stockrecord = Asxdata()
                    stockrecord.key = asx_key
                    stockrecord.code = row[0]
                    stockrecord.date = row[1]
                    stockrecord.open = row[2]
                    stockrecord.high = row[3]
                    stockrecord.low = row[4]
                    stockrecord.close = row[5]
                    stockrecord.volume = row[6]
                    stockrecord.put()
                    counter = counter + 1	
                    totalcount = totalcount + 1	
                self.response.out.write('\n%s records added' % (str(counter)))
        self.response.out.write('\n\n%s dates added' % (str(filecount)))
        self.response.out.write('\n%s total records added' % (str(totalcount)))
        self.response.out.write('\n%s records per date average' % (str(totalcount / filecount)))
