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

if settings['ActiveValue'] == 0:
	initialState = GPIO.HIGH
else:
	initialState = GPIO.LOW

for room in rooms:
	for accesory in room['Accesories']:
		if accesory['Type'] == 'GPIO':
			GPIO.setup(accesory['Pin'], GPIO.OUT, initial=initialState)