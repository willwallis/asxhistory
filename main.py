import webapp2
import os
import csv
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'html')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
		
class MainPage(webapp2.RequestHandler):
    def get(self):
        template_head = JINJA_ENVIRONMENT.get_template('header.html')
        template_foot = JINJA_ENVIRONMENT.get_template('footer.html')
        template_values = ''
        self.response.write(template_head.render(template_values))
        self.response.write(template_foot.render(template_values))
                			
    def post(self):
        iserror = False
        error_message = ""
        filefound = False
        codefound = False
        # Define HTML templates	
        template_head = JINJA_ENVIRONMENT.get_template('header.html')
        template_foot = JINJA_ENVIRONMENT.get_template('footer.html')
        template_table = JINJA_ENVIRONMENT.get_template('body_table.html')
        template_error = JINJA_ENVIRONMENT.get_template('body_error.html')
        # Get query code and date (reformat)		
        querycode = str(self.request.get('code')).upper()
        querydate = self.request.get('date')[0:-6] + self.request.get('date')[5:-3] + self.request.get('date')[8:]
        queryyear = self.request.get('date')[0:-6]
        # Render HTML header including query components		 
        template_values = {
            'querycode': self.request.get('code'),			
            'querydate': self.request.get('date'),						
            }
        self.response.write(template_head.render(template_values))	
        # Verify that code and date have been populated
        if len(querycode) < 2:
            iserror = True
            error_message = "Please enter an ASX code.  "
        if len(querydate) < 8:	
            iserror = True
            error_message = error_message + "Please select a date."
        if int(queryyear) < 1997 or int(queryyear) > 2014:
            iserror = True
            error_message = error_message + "Please select a date between 1997 and 2014"			
        if iserror == False:		
        # Query from file
            queryfile = querydate + '.txt'
            for filename in os.listdir(os.path.join(os.path.dirname(__file__),'loaddata', queryyear)):
                if filename.endswith(queryfile):
                    filefound = True
                    inputfile = os.path.join(os.path.dirname(__file__), 'loaddata', queryyear, queryfile)
                    reader = csv.reader(open(inputfile, 'rb'), delimiter=',', quotechar='"')
                    for row in reader:
                        if row[0] == querycode:
                            codefound = True
                            template_values = {
                                'code': row[0],
                                'date': row[1],
                                'open': row[2],
                                'high': row[3],
                                'low': row[4],
                                'close': row[5],
                                'volume': row[6],			
                                }
                            self.response.write(template_table.render(template_values))	
            if codefound == False:
                iserror = True
                error_message = "ASX code not found at this date"	
            if filefound == False:
                iserror = True
                error_message = "No data found for this date. Check it isn't the weekend or outside source data range"					
        if iserror == True:	
        # Create error message
            template_values = {
               'error_message': error_message,
            }			
            self.response.write(template_error.render(template_values))						
        # Write footer		 
        self.response.write(template_foot.render(template_values))			
			
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)