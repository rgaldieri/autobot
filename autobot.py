import os
import sys
import codecs
import nltk
import urllib2
import json as simplejson
import urllib
import re
from BeautifulSoup import BeautifulSoup
import mechanize
import sqlite3 as lite
import random
from time import gmtime, strftime, sleep
from db import Database


class Autobot():
	def __init__(self):

		self.br = mechanize.Browser()
		# Options
		self.br.set_handle_equiv(True)
		self.br.set_handle_gzip(False)
		self.br.set_handle_redirect(True)
		self.br.set_handle_referer(True)
		self.br.set_handle_robots(False)
		
	def setOptions(self, options):
		
		self.options = options
		self.userAgent = self.options['userAgent']

		self.br.addheaders = [('User-agent', self.userAgent)]

		# Debug
		self.br.set_debug_http(self.options['debug'])
		self.br.set_debug_redirects(True)
		self.br.set_debug_responses(self.options['responses'])

		# Follows refresh 0 but not hangs on refresh > 0
		self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		self.br.set_handle_redirect(mechanize.HTTPRedirectHandler)

	def getOptions(self):
		return self.options

	def setUserAgent(self, userAgent):
		self.userAgent = userAgent

	def getUserAgent(self):
		return self.userAgent

	def login(self, username, password):

		# Grabbing website's URL
		r = self.br.open('https://www.blurum.it/Web/')

		# Submitting Login Button

		self.br.select_form(nr=0)

		for control in self.br.form.controls:
		   if control.type == "submit":
		       control.readonly = False

		# Username Form

		self.br.form['ctrl_LoginControl$loginView$c01$RPLogin$LoginView$Username'] = username

		# Password Form

		self.br.form['ctrl_LoginControl$loginView$c01$RPLogin$LoginView$Password'] = password

		# Submit Button

		self.br.submit(name='ctrl_LoginControl$loginView$c01$RPLogin$LoginView$LoginButton', label='Accedi')

		print "\n==> Getting Home Page .."
		if self.options['debug'] == True:
			print "THIS IS THE HOME PAGE I GOT"
			print self.br.response().read()
		print "\n.. done"

		print'\n==> Getting first submit button ..'
		self.br.select_form(nr=0)
		self.br.submit(label='Submit')
		self.html = self.br.response().read()
		if self.options['debug'] == True:
			print self.html
		print "\n.. done\n"

		soup_token = BeautifulSoup(self.html) #Soup instance	
		print'\n==> Getting second submit button ..'
		self.br.select_form(nr=0)
		print "\n.. done\n"
		for control in self.br.form.controls:
		   if control.type == "hidden":
		       control.readonly = False
		try:
			token = soup_token.find('input', {'name':'wresult'})
			print "\n==> Getting Token .. "
			if self.options['debug'] == True:
				print token['value']
			print "\n.. done\n"

			print "\n==> Logging in .."
			self.br['wresult'] = token['value']
			self.br.submit(label='Submit')
			self.html = self.br.response().read()
			print "\n==> Loading Source Code logged page .."
			if self.options['debug'] == True:
				print "THIS IS SELF.HTML"
				print self.html, '\n'
			print ".. done\n"


			# Login successfully done
			
			return True
		except:
			# Error
			print "THERE WAS AN ERROR LOGGING IN."
			return False

	def query(self, query):

		print "\n==> Sending the query .. "
		soup = BeautifulSoup(self.html) #Soup instance	
		text = soup.findAll("input", {"class": "search_bar_input"})

		bar_name2 = text[0]['name']
		bar_name = text[1]['name']

		if self.options['debug'] == True:
			print "Name della barra di ricerca\n"
			print bar_name

		button = soup.find("input", {"class": "search"})
		button_name = button['name']
		if self.options['debug'] == True:
			print "Name del submit di ricerca\n"
			print button_name

		#ERROR HERE
		self.br.select_form(nr=0)
		print "REACHED THIS"

		self.br[bar_name] = query
		self.br[bar_name2] = query
		print "\n==> Query \n"
		print query
		for control in self.br.form.controls:
		  		if control.type == "disabled":
		       			control.disabled = False
		self.br.submit()
		response = self.br.response().read()

		if self.options['debug'] == True:
			print response
			
		print "\n==> Query sent"

class Log:

	def __init__(self, name, query):
		self.query = query
		log = open(name, 'a')
		self.time1 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		self.interval = random.randrange(10, 40)
		sleep(self.interval)
		self.time2 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		self.s = "Query: \n"
		self.s += unicode(self.query).encode('utf-8')
		self.s += "\n\nInterval: \t"
		self.s += str(self.interval)
		self.s += "\nTime when the script started: \t"
		self.s += str(self.time1)
		self.s += "\nTime when the script ended: \t"
		self.s += str(self.time2)
		self.s += '\n------------------------------------------------\n'
		log.write(self.s)

	def getInterval(self):
		return self.s

def main():
	# Autobot
	bot = Autobot()

	db = Database('blurum.db')
	users = Database('users.db.sqlite')

	credentials = users.getData()
	settings = users.getSettings()

	BotOptions = {
		'userAgent': credentials[0][0],
		'debug': False,
		'responses': True
	}

	bot.setOptions(BotOptions)
	username = credentials[0][0]
	password = credentials[0][1]
	query = db.exec_query()

	if(bot.login(username, password)):
		# Login succesfully done
		print "\nLogged\n"

		# Log
		print "Print logs\n"
		log = Log('queries.log', unicode(query).encode('utf-8'))

		print "Query:\n"
		print unicode(query).encode('utf-8')
		# Send the query
		bot.query(unicode(query).encode('utf-8'))
		
	else:

		# Login failed
		print "Login Failed .. Fuck!"

main()
		
