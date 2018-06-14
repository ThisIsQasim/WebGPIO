import os, sys, yaml

configPath = os.path.join(sys.path[0], "config.yml")
try:
	with open(configPath, 'r') as ymlfile:
	    cfg = yaml.load(ymlfile)
except Exception:
	print("Config file not found or invalid. Please provide a valid config.yml file. See exampleconfig.yml for reference")
	exit()

try:
	rooms = cfg['Rooms']
except Exception:
	print("config.yml file is not valid. See exampleconfig.yml for reference")
	exit()

if 'Settings' in cfg:
	settings = cfg['Settings']
else:
	settings = {}

if 'Host' not in settings:
	settings['Host'] = '0.0.0.0' 

if 'Port' not in settings:
	settings['Port'] = 8000

if 'Threaded' not in settings:
	settings['Threaded'] = True 

if 'Debug' not in settings:
	settings['Debug'] = False 

if 'SSL' in settings:
	if 'Path' in settings['SSL']:
		if settings['SSL']['Path'] != 'default':
			settings['cerPath']=settings['SSL']['Path'] + settings['SSL']['Certificate']
			settings['keyPath']=settings['SSL']['Path'] + settings['SSL']['Key']
	else:
		settings['cerPath']=os.path.join(sys.path[0], settings['SSL']['Certificate'])
		settings['keyPath']=os.path.join(sys.path[0],  settings['SSL']['Key'])
else:
	settings['SSL']= { 'Enabled': False }

if 'RefreshRate' not in settings:
	settings['RefreshRate'] = 5

if 'GPIOMode' not in settings:
	settings['GPIOMode'] = "BCM"

if 'Make' not in settings:
	settings['Make'] = "RaspberryPi"


if 'Inverted' in settings:
	GlobalActiveState = 1 - int(settings['Inverted'])
else:
	GlobalActiveState = 1

for i, room in enumerate(rooms):
	for j, accesory in enumerate(room['Accesories']):
		if 'Inverted' in accesory:
			rooms[i]['Accesories'][j]['ActiveState'] = 1 - int(accesory['Inverted'])
		else:
			rooms[i]['Accesories'][j]['ActiveState'] = GlobalActiveState