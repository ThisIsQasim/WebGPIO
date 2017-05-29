from flask import Flask, render_template, redirect, request, Markup
import subprocess
import os
import datetime
import time
app = Flask(__name__)



outPin = [[6, 13, 19, 26]]
roomName = ['Bed Room', 'Server Room']
accName= [['Fan', 'Front Light', 'Back Light', 'Bright Light'], ['Champ']]

accState=[]

for i in range(len(roomName)):
	print("Initializing room: %d" % (i+1))
	accState.append([])
	for j in range(len(accName[i])):
		accState[i].append(0)
		print("Initializing accesory: %d" % (j+1))

privateIP= "0.0.0.0"
publicIP= "0.0.0.0"

def getState(roomNumber, accNumber):
	state=accState[roomNumber][accNumber]
	return state

def setState(roomNumber, accNumber, newState):
	return 0

def containerState(roomNumber, accNumber):
	if accState[roomNumber][accNumber] is 0:
		return 'containerOff'
	else:
		return 'containerOn'

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
				passer = passer + "<button class='%s' formaction='/pin/%d/%d/%d/'>%s</button>" % (containerState(i,j), i, j, accState[i][j], pinHtmlName)

		buttonGrid = Markup(passer)
		templateData = {
			'title' : 'WebGPIO',
			'time': timeString,
			'buttons' : buttonGrid
			}
		return render_template('main.html', **templateData)


@app.route("/pin/<int:roomNumber>/<int:accNumber>/<int:state>/")
def toggle(roomNumber, accNumber, state):
	state= 1 - state
	#setState(roomNumber, accNumber, state)
	registerState(roomNumber, accNumber, state)
	#subprocess.call(['./echo.sh'], shell=True)
	print(roomNumber, accNumber, state)
	return redirect("/", code=302)


@app.route("/ip/<string:lanIP>/")
def registerIP(lanIP):
	global privateIP
	privateIP=lanIP
	global publicIP
	publicIP=request.remote_addr
	print(privateIP, publicIP)
	return "IP addresses registered"

@app.route("/state/<int:roomNumber>/<int:accNumber>/<int:state>/")
def registerState(roomNumber, accNumber, state):
	global accState
	accState[roomNumber][accNumber]=state
	print(roomNumber, accNumber, state)
	return "State registered"


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
