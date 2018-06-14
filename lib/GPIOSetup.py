from lib.setup import rooms, settings

if settings['Make'] == 'OrangePi':
	import OPi.GPIO as GPIO
else:
	import RPi.GPIO as GPIO

if settings['GPIOMode'] == 'BOARD':
	GPIO.setmode(GPIO.BOARD)
else:
	GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def initialState(active_value):
	if active_value == 0:
		return GPIO.HIGH
	else:
		return GPIO.LOW

for room in rooms:
	for accesory in room['Accesories']:
		if accesory['Type'] == 'GPIO':
			initial_state = initialState(accesory['ActiveState'])
			GPIO.setup(accesory['Pin'],
					   GPIO.OUT, 
					   initial= initial_state)