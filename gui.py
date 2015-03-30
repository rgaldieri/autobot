import pygtk
import gtk
import cron
import os
from db import Database

class Gui:

	def __init__(self):
		self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.win.set_default_size(300,280)
		self.win.set_title('AutoBot')
		self.vbox = gtk.VBox(gtk.FALSE, 5)
		self.vbox2 = gtk.VBox(gtk.FALSE, 5)
		self.vbox3 = gtk.VBox(gtk.FALSE, 5)
		self.hbox = gtk.HBox(gtk.FALSE, 5)
		self.fixed = gtk.Fixed()
		self.fixed2 = gtk.Fixed()
		self.fixed3 = gtk.Fixed()
		self.fixed4 = gtk.Fixed()
		self.vbox.pack_start(self.fixed)
		self.vbox2.pack_start(self.fixed2)
		
		self.notebook = gtk.Notebook()
		self.show_tabs = True
		self.show_border = True
		self.notebook.show()
		self.notebook.append_page(self.vbox, gtk.Label('Account'))
		self.notebook.append_page(self.vbox2, gtk.Label('Settings'))
		self.notebook.append_page(self.vbox3, gtk.Label('Run Autobot'))
		# Connection
		self.labelConnection = gtk.Label('<b><big>Insert your login data</big></b>')
		self.labelConnection.set_use_markup(gtk.TRUE)
		self.button = gtk.Button('Save Data')
		self.username = gtk.Label('Username')
		self.password = gtk.Label('Password')
		self.resultConnection= gtk.Label()
		self.formUsername = gtk.Entry()
		self.formPassword = gtk.Entry()
		db = Database('users.db.sqlite')
		data = db.getData()
		if data:
			if(data[0][0]):
				self.formUsername.set_text(data[0][0])
			if(data[0][1]):
				self.formPassword.set_text(data[0][1])
		self.formPassword.set_visibility(False)
		self.start = gtk.Button('Start AutoBot')
		self.stop = gtk.Button('Stop Autobot')
		self.fixed.put(self.labelConnection, 15, 10)
		self.fixed.put(self.username,15,50)
		self.fixed.put(self.formUsername,90,45)
		self.fixed.put(self.password,15,90)
		self.fixed.put(self.formPassword,90,85)
		self.fixed.put(self.resultConnection, 15, 165)
		self.fixed.put(self.button, 15, 125)
		#=============================================

		# Settings
		datasettings = db.getSettings()
		self.labelSettings = gtk.Label('<b><big>Insert your settings</big></b>')
		self.labelSettings.set_use_markup(gtk.TRUE)
		self.directory = gtk.Entry()
		self.entryUserAgent = gtk.Entry()
		self.nameUser = gtk.Entry()
		self.minutes = gtk.Entry()
		self.minutes.set_text('5')
		self.labelMinutes = gtk.Label('Interval in Minutes')
		if datasettings:
			if(datasettings[0][0]):
				self.entryUserAgent.set_text(datasettings[0][0])
			if (datasettings[0][1]):
				self.directory.set_text(datasettings[0][1])
			if(datasettings[0][2]):
				self.nameUser.set_text(datasettings[0][2])
		self.labelDirectory = gtk.Label('Working Directory')
		self.labelUserAgent = gtk.Label('User Agent')
		self.labelUser = gtk.Label('OS Username')
		self.buttonSaveSettings = gtk.Button('Save settings')
		self.fixed2.put(self.labelSettings, 15, 10)
		self.fixed2.put(self.labelDirectory, 15,45)
		self.fixed2.put(self.directory, 120,40)
		self.fixed2.put(self.entryUserAgent,120,80)
		self.fixed2.put(self.labelUserAgent,15,85)
		self.fixed2.put(self.nameUser,120, 120)
		self.fixed2.put(self.labelUser,15,125)
		self.fixed2.put(self.labelMinutes, 15, 165)
		self.fixed2.put(self.minutes,120, 160)
		self.fixed2.put(self.buttonSaveSettings,12,200)
		
		# Run
		self.labelRun = gtk.Label("<b><big>RUN AUTOBOT</big></b>")
		Cron = cron.Daemon()
		isActiveCron = Cron.getCron()
		if not(isActiveCron):
			self.vbox3.pack_start(self.fixed3)
		else:
			self.vbox3.pack_start(self.fixed4)

		# if start
		self.labelToStart = gtk.Label("<big><b>Autobot</b> is not active. Just Run it!</big>")
		self.labelToStart.set_use_markup(gtk.TRUE)
		self.labelStart = gtk.Label("<b><big>START</big></b>")
		self.labelStart.set_use_markup(gtk.TRUE)
		self.resultStart= gtk.Label()
		self.fixed3.put(self.labelToStart, 15, 10)
		self.fixed3.put(self.labelStart, 15, 60)
		self.fixed3.put(self.start, 15, 90)
		self.fixed3.put(self.resultStart, 15, 120)
		# if stop
		self.labelToStop = gtk.Label("<big><b>Autobot</b> is already active. Stop it? Why!?!?</big>")
		self.labelToStop.set_use_markup(gtk.TRUE)
		self.labelStop = gtk.Label("<b><big>STOP</big></b>")
		self.labelStop.set_use_markup(gtk.TRUE)
		self.resultStop= gtk.Label()
		self.fixed4.put(self.labelToStop, 15, 10)
		self.fixed4.put(self.labelStop, 15, 60)
		self.fixed4.put(self.stop, 15, 90)
		self.fixed4.put(self.resultStop, 15, 120)
		# Functions Connections
		self.button.connect("clicked", self.saveData)
		self.start.connect("clicked", self.startBot)
		self.stop.connect("clicked", self.stopBot)
		self.buttonSaveSettings.connect("clicked", self.saveSettings)
		self.win.add(self.notebook)
		self.win.connect('destroy', self.on_destroy)
		self.win.show_all()

	def saveData(self, widget):
		db = Database('users.db.sqlite')
		self.setUsername = self.formUsername.get_text()
		self.setPassword = self.formPassword.get_text()
		
		data = db.getData()
		if data:
			db.updateData(self.setUsername, self.setPassword)
		else:
			db.saveData(self.setUsername, self.setPassword)

	def saveSettings(self, widget):
		db = Database('users.db.sqlite')
		directory = self.directory.get_text()
		userAgent = self.entryUserAgent.get_text()
		user = self.nameUser.get_text()
		data = db.getSettings()
		if data:
			db.updateSettings(userAgent, directory, user)
		else:
			db.saveSettings(userAgent, directory, user)


	def startBot(self, widget):
		# Autobot
		minutes = self.minutes.get_text()
		Cron = cron.Daemon()
		Cron.setCron(minutes)
		Cron.startCron()
		self.resultStart.set_text('Bot Started!')

	def stopBot(self, widget):
		os.system('crontab -r')
		self.resultStop.set_text('Bot Stopped!')
	
	def on_destroy(self, widget, user_data=None):
		# Exit the app
		gtk.main_quit()

	def main(self):
		gtk.main()

# Class that manages text
if __name__ == "__main__":
	gui = Gui()
	gui.main()
