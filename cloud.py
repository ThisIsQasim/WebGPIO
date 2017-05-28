from flask import Flask, render_template, redirect, request, Markup
import RPi.GPIO as GPIO
import subprocess
import os
import datetime
import time
app = Flask(__name__)



outPin = [[6, 13, 19, 26]]
roomName = ['Bed Room', 'Server Room']
accName= [['Fan', 'Front Light', 'Back Light', 'Bright Light'], ['Champ']]


privateIP= "0.0.0.0"
publicIP= "0.0.0.0"

def accState(roomNumber, accNumber):
	if roomNumber == 0:
		if GPIO.input(outPin[roomNumber][accNumber]) is 1:
			return 'containerOff'
		else:
			return 'containerOn'
	elif roomNumber > 0:
		#get the state of other accesories in other rooms
		return 'containerOff'

@app.route("/")
def main():
	print(request.remote_addr, publicIP)
	if request.remote_addr == publicIP:
		embededGrid="<iframe class='frame' src='http://%s:%d'> Use a modern browser please??? <iframe/>" % (privateIP, 8000)
		markedUpURL=Markup(embededGrid)
		templateData = {
			'title' : 'WebGPIO',
			'buttons' : embededGrid
		}
		return render_template('frame.html', **templateData)
	else:
		now = datetime.datetime.now()
		timeString = now.strftime("%Y-%m-%d %I:%M %p")
	
		passer = ''
		for i in range(len(roomName)):
			passer = passer + "<p class='roomtitle'>%s</p>" % (roomName[i])
			for j in range(len(accName[i])):
				pinHtmlName = accName[i][j].replace(" ", "<br>")
				passer = passer + "<button class='%s' formaction='/pin/%d/%d/'>%s</button>" % (accState(i,j), i, j, pinHtmlName)

		buttonGrid = Markup(passer)
		templateData = {
			'title' : 'WebGPIO',
			'time': timeString,
			'buttons' : buttonGrid
			}
		return render_template('main.html', **templateData)


@app.route("/pin/<int:roomNumber>/<int:accNumber>/")
def toggle(roomNumber, accNumber):
	if roomNumber == 0:
		state= not GPIO.input(outPin[roomNumber][accNumber])
		GPIO.output(outPin[roomNumber][accNumber],state)
	#subprocess.call(['./echo.sh'], shell=True)
	elif roomNumber > 0:
		#action for other rooms
		if accNumber == 0:
			subprocess.call(['./echo.sh'], shell=True)
	print(roomNumber, accNumber)
	return redirect("/", code=302)


@app.route("/IP/<string:lanIP>/<string:wanIP>/")
def registerIP(lanIP, wanIP):
	global privateIP
	privateIP=lanIP
	global publicIP
	publicIP=wanIP
	print(privateIP, publicIP)
	return "IP addresses registered"



if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
