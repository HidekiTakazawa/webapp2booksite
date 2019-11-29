# coding: UTF-8
import webapp2

import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.db import Key

# DWW
import os
from google.appengine.ext.webapp import template
import urllib

# DEAN
import logging
#import re
###


class BooksData(db.Model):
    bookname = db.StringProperty()
    author = db.StringProperty()
    publisher = db.StringProperty()
    purchasedate = db.StringProperty()
    price = db.StringProperty()
    memo = db.StringProperty()
class MainPage(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/toppage.html')
        template_values = {}
        self.response.out.write(template.render(path, template_values))
  
class StoreAValue(webapp2.RequestHandler):    

    def post(self):
        
        bookname = self.request.get('bookname')
        author = self.request.get('author')
        publisher = self.request.get('publisher')
        purchasedate = self.request.get('purchasedate')
        price = self.request.get('price')
        memo = self.request.get('memo')
        bookdata = BooksData(bookname=bookname, author=author, publisher=publisher, purchasedate=purchasedate, price=price, memo=memo)
        bookdata.put()
        template_values = {"bookname":bookname, "author": author, "publisher":publisher, "purchasedate":purchasedate, "price":price, "memo":memo}
        path = os.path.join(os.path.dirname(__file__), 'templates/databaseAdd.html')
        self.response.out.write(template.render(path, template_values))
class GetValueHandler(webapp2.RequestHandler):
    def get(self):
        #booksData = BooksData.query().fetch()
        booksData = db.GqlQuery("Select * from BooksData")
        template_values = {"booksData":booksData}
        path = os.path.join(os.path.dirname(__file__), 'templates/databaseAll.html')
        self.response.out.write(template.render(path, template_values))
class DeleteEntry(webapp2.RequestHandler):
    def post(self):
        bookdata_key = self.request.get('bookdata_key')
        key = db.Key(bookdata_key)
        db.run_in_transaction(dbSafeDelete,key)
        self.redirect('/database_all')
####
def dbSafeDelete(key):
  	db.delete(key)
  
### Assign the classes to the URL's

app = webapp2.WSGIApplication ([('/', MainPage),
                           ('/database_all', GetValueHandler),
			   ('/database_new', StoreAValue),
		           ('/database_delete', DeleteEntry)

                           ])

    