import sqlite3 as lite

class Database:
	
	def __init__(self, dbName):
		self.dbName = dbName
		self.connection = lite.connect(self.dbName)
		self.cur = self.connection.cursor()

	def exec_query(self):
		self.cur.execute("SELECT Name FROM queries ORDER BY RANDOM() LIMIT 1")
		return self.cur.fetchone()[0]

	def close(self):
		self.connection.close()

	def saveData(self, username, password):
		self.cur.execute("INSERT INTO 'users'(`Username`, `Password`) VALUES ('"+ username +"', '" + password + "')")
		self.connection.commit()

	def getData(self):
		self.cur.execute("SELECT Username, Password FROM users")
		data = self.cur.fetchall()
		return data

	def updateData(self, username, password):
		self.cur.execute("UPDATE users SET Username = '"+ username +"', Password = '" + password + "' LIMIT 1")
		self.connection.commit()

	def saveSettings(self, userAgent, directory, user):
		self.cur.execute("INSERT INTO 'settings'(`userAgent`, `Directory`, `user`) VALUES ('"+ userAgent +"', '" + directory + "', + '" + user + "')")
		self.connection.commit()

	def getSettings(self):
		self.cur.execute("SELECT userAgent, Directory, user FROM settings")
		data = self.cur.fetchall()
		return data

	def updateSettings(self, userAgent, directory, user):
		self.cur.execute("UPDATE settings SET userAgent = '"+ userAgent +"', Directory = '" + directory + "', user = '" + user +"' LIMIT 1")
		self.connection.commit()
