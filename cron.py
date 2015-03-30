#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from crontab import CronTab
from db import Database

class Daemon:

	def __init__(self):
		self.db = Database('users.db.sqlite')
		self.settings = self.db.getSettings()
		user = self.settings[0][2]
		self.cron = CronTab(user)

	def setCron(self, each_minutes = 5):

		self.each_minutes = each_minutes
		self.time = {'minutes': each_minutes}

	def startCron(self):
		cmd = 'cd ' + self.settings[0][1] + ' && python ' + self.settings[0][1] + 'autobot.py'
		cron_job = self.cron.new(cmd)
		cron_job.minute.every(self.time['minutes'])
		#writes content to crontab
		self.cron.write()

	def printCrons(self):
		jobs = []
		for job in self.cron:
			jobs.append(job)
		return jobs

	def getCron(self):
		jobs = self.printCrons()
		if jobs:
			return True
		else:
			return False
