import subprocess, time
from lib.GPIOSetup import GPIO
from lib.setup import settings

class accesoryObject:
	attributes = {}
	name = ""
	type = ""
	value = ""

	def __init__(self, dictionary):
		self.attributes = dictionary
		self.name = dictionary['Name']
		self.type = dictionary['Type']
		self.value = dictionary['Value']

	def getState(self):
		if self.type == 'GPIO':
			if GPIO.input(self.value) is settings['ActiveValue']:
				return 1
			else:
				return 0
		else:
			#get the state of other accesories in other rooms
			#not properly implemented yet
			try:
				timeout = "timeout "+str(attributes['Timeout'])+" "
			except Exception:
				timeout = "timeout 0.2 "
			returnCode = subprocess.call([timeout + self.value], shell=True)
			if returnCode == 0:
				return 1
			return 0

	def executeAction(self):
		if self.type == 'GPIO':
			original_state= GPIO.input(self.value)
			new_state = 1 - original_state
			GPIO.output(self.value, new_state)
			try:
				time.sleep(self.attributes['Duration'])
				GPIO.output(self.value, original_state)
			except Exception:
				pass