import datetime, json
from flask import Flask, render_template, request, redirect, Markup, make_response, url_for
from lib.cors import crossdomain
from lib.setup import rooms, settings
from lib.GPIOSetup import GPIO
from lib.appliance import Appliance
from lib import authentication
app = Flask(__name__)


def updateStates(rooms):
	for i, room in enumerate(rooms):
		for j, appliance in enumerate(room['Appliances']):
			current_appliance = Appliance(appliance)
			rooms[i]['Appliances'][j]['State'] = current_appliance.getState()
	return rooms

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)


@app.route("/")
@authentication.login_required
def home():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %I:%M %p")
	templateData = {
		'title' : 'WebGPIO',
		'time': timeString,
		'rooms' : updateStates(rooms),
		'refresh_rate' : settings['RefreshRate']*1000
	}
	return render_template('home.html', **templateData)

@app.route("/grid/")
@authentication.login_required
@crossdomain(origin='*')
def grid():
	templateData = {
		'title' : 'WebGPIO',
		'rooms' : updateStates(rooms)
	}
	return render_template('grid.html', **templateData)

@app.route("/button/<int:room_index>/<int:appliance_index>/")
@authentication.login_required
@crossdomain(origin='*')
def button(room_index, appliance_index):
	appliance = Appliance(rooms[room_index]['Appliances'][appliance_index])
	appliance.executeAction()
	templateData = {
		'title' : 'WebGPIO',
		'state' : appliance.getState(),
		'room_index' : room_index,
		'appliance_index' : appliance_index,
		'name' : appliance.name
	}
	return render_template('button.html', **templateData)

@app.route("/login/")
def login():
	return render_template('login.html')

@app.route("/authenticate/", methods=['GET', 'POST'])
def auth():
	if request.method == 'POST':
		password = request.form['password']
		token = authentication.generateToken(password)
		if token:
			expiry_date = datetime.datetime.now() + datetime.timedelta(days=30)
			response = make_response(redirect(url_for('.home')))
			response.set_cookie('token', token, expires=expiry_date, httponly=True, samesite='Lax')
			return response
	return redirect(url_for('.login'))

@app.route("/logout/")
def logout():
	authentication.removeToken()
	response = make_response(redirect(url_for('.login')))
	response.set_cookie('token', '', expires=0, httponly=True, samesite='Lax')
	return response

if __name__ == "__main__":
	if settings['SSL']['Enabled']:
		app.run(host = settings['Host'], 
				port = settings['Port'],
				threaded = settings['Threaded'], 
				debug = settings['Debug'], 
				ssl_context = (settings['cerPath'], settings['keyPath']))
	else:
		app.run(host = settings['Host'], 
				port = settings['Port'], 
				threaded = settings['Threaded'], 
				debug = settings['Debug'])