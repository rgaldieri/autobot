#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import cron
import os
import subprocess
import sqlite3 as lite
from crontab import CronTab
from db import Database

class Menu:
	def __init__(self):
		print (sys.version)
		self.mainMenuOptions = { 'a': 'Account', 's': 'Settings', 'u': 'Autobot', 'q': 'Quit' }
		self.mainMenuActions = { 'a': self.account, 's': self.settings,'u': self.autobot, 'q': self.quit }
		self.userDB = Database('users.db.sqlite')		
		self.mainMenuDisplay()
		
	def mainMenuDisplay(self):
		self.terminal_width = self.get_terminal_width()
		self.menu_border = "\n"
		self.menu_options = "    "
		for i in range( 0, self.terminal_width - 4):
			self.menu_border += "-"
		print self.menu_border + "\n"
		for elem in self.mainMenuOptions.items():
			self.menu_options += elem[0] + ") " + elem[1] + "     "
		print self.menu_options + "\n" + self.menu_border + "\n"
		self.waitForAction(self.mainMenuOptions, self.mainMenuActions)

	def waitForAction(self, options, actions):
		self.userInput = raw_input("What option do you choose?\n")
		while(self.userInput  not in options):
			print "Not valid Option. Try Again.\n\n"
			self.userInput  = raw_input()
		print("You have chosen %s. About to execute it") %(self.userInput)
		actions[self.userInput]()
		
	def account(self):
		self.con = None
		try:
			self.con = lite.connect('users.db.sqlite')
			
			self.cur = self.con.cursor()    
			self.cur.execute('SELECT * FROM users')
			data = self.cur.fetchone()

			self.username = data[0]
			self.password = data[1]
			print "\nYour Username is %s and your password is %s.\n" %(self.username, self.password)
			self.account_options = { 'c': 'Change Details', 'h': 'Go back to Home', 'q': 'Quit' }
			self.account_actions = { 'c': self.change_account_settings, 'h': self.mainMenuDisplay, 'q': self.quit }
			print "You can now:\n"
			for elem in self.account_options.items():
				print elem[0] + ")  %s" %(elem[1]) 
			self.waitForAction(self.account_options, self.account_actions)
		except lite.Error, e:
			print "Error %s:" % e.args[0]
			sys.exit(1)
		finally:
			if self.con:
				print("Closing Connection HEREEE")
				self.con.close()

	def change_account_settings(self):
		newUsername = self.username
		newPassword = self.password
		userChanged = 0
		
		wannaChangeUser = raw_input('Do you want to change your username? (Y/N)\n')
		if(wannaChangeUser[0] == 'y' or wannaChangeUser[0] == 'Y'):
			newUsername = raw_input('Insert your new Username:\n')
			userChanged = 1
		wannaChangePswd = raw_input('Do you want to change your Password? (Y/N)\n')
		changed = 0
		passwordChanged = 0
		if(wannaChangePswd[0] == 'y' or wannaChangePswd[0] == 'Y'):
			attempts = 0
			while(attempts < 3 and passwordChanged == 0):
				newPasswordOne = raw_input('Insert your new Password\n')
				newPasswordTwo = raw_input('Confirm your new Password\n')
				if(newPasswordOne == newPasswordTwo):
					newPassword = newPasswordOne
					passwordChanged = 1
				else:
					print "\nThe two passwords don't match. Try again.\n"
					attempts += 1
		if(passwordChanged == 1 or userChanged == 1):
			query = "UPDATE users SET Username = \"%s\", Password = \"%s\"" %( newUsername, newPassword)
			print query
			self.cur.execute(query)
			self.con.commit()
			print("The query has been successfully executed\n")
			self.mainMenuDisplay()

	def settings(self):
		self.con = None
		try:
			self.con = lite.connect('users.db.sqlite')
			
			self.cur = self.con.cursor()    
			self.cur.execute('SELECT * FROM settings')
			data = self.cur.fetchone()
			self.userAgent = data[0]
			self.directory = data[1]
			self.linuxUser = data[2]
			print "\nYour userAgent is %s\n\nYour Folder is %s.\n\nYour Linux username is %s" %(self.userAgent, self.directory, self.linuxUser)
			self.settings_options = { 'c': 'Change Settings', 'h': 'Go back to Home', 'q': 'Quit' }
			self.settings_actions = { 'c': self.change_settings, 'h': self.mainMenuDisplay, 'q': self.quit }
			for elem in self.settings_options.items():
				print elem[0] + ")  %s" %(elem[1]) 
			self.waitForAction(self.settings_options,self.settings_actions)

		except lite.Error, e:
			print "Error %s:" % e.args[0]
			sys.exit(1)
		finally:
			if self.con:
				self.con.close()

	def change_settings(self):
		wannaChangeUserAgent = raw_input('Do you want to change your User Agent? (Y/N)\n')
		if(wannaChangeUserAgent[0] == 'y' or wannaChangeUserAgent[0] == 'Y'):
			self.userAgent = raw_input('Insert your new User Agent:\n')
		
		wannaChangeDir = raw_input('Do you want to change your Directory? (Y/N)\n')
		if(wannaChangeDir[0] == 'y' or wannaChangeDir[0] == 'Y'):
			self.directory = raw_input('Insert your new Directory:\n')
		
		wannaChangeUserName = raw_input('Do you want to change your System Username? (Y/N)\n')
		if(wannaChangeUserName[0] == 'y' or wannaChangeUserName[0] == 'Y'):
			self.linuxUser = raw_input('Insert your new Account User:\n')
		
		query = "UPDATE Settings SET userAgent = \"%s\", Directory = \"%s\", user = \"%s\"" % (self.userAgent, self.directory, self.linuxUser)
		print query
		self.cur.execute(query)
		self.con.commit()
		print("The query has been successfully executed\n")
		self.mainMenuDisplay()
		
	def autobot(self):
		Cron = cron.Daemon()
		isActiveCron = Cron.getCron()
		if not(isActiveCron):
			startCron = raw_input("There is no Cron running. Would you like to Start one? (Y/N)\n")
			if(startCron[0] == 'y' or startCron[0] == 'Y'):
				minutes = raw_input("What's the delay you wanna use? (Default=5)\n")
				Cron.setCron(minutes)
				Cron.startCron()
		else:
			stopCron = raw_input("There is a Cron running. Do you want to stop it? (Y/N)\n")
			if(stopCron[0] == 'y' or stopCron[0] == 'Y'):
				os.system('crontab -r')
				print('Bot Stopped!\n')
		self.mainMenuDisplay()

	def quit(self):
		return 0

	def get_terminal_width(self):
		command = ['tput', 'cols']
		try:
			width = int(subprocess.check_output(command))
		except OSError as e:
			print("Invalid Command '{0}': exit status ({1})".format(
				  command[0], e.errno))
		except subprocess.CalledProcessError as e:
			print("Command '{0}' returned non-zero exit status: ({1})".format(
				  command, e.returncode))
		else:
			return width

def main():
	menu = Menu()



main()



