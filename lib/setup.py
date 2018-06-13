import os, sys, yaml

configPath = os.path.join(sys.path[0], "config.yml")
try:
	with open(configPath, 'r') as ymlfile:
	    cfg = yaml.load(ymlfile)
except Exception:
	print("Config file not found. Please provide a valid config.yml file. See exampleconfig.yml for reference")
	exit()

try:
	rooms = cfg['Rooms']
except Exception:
	print("config.yml file is not valid. See exampleconfig.yml for reference")
	exit()

try:
	settings = cfg['Settings']    
except Exception:
	settings = {}

try:
	settings['Host']
except Exception:
	settings['Host'] = '0.0.0.0' 

try:
	settings['Port']
except Exception:
	settings['Port'] = 8000

try:
	settings['Threaded']
except Exception:
	settings['Threaded'] = True 

try:
	settings['Debug']
except Exception:
	settings['Debug'] = False 

try:
	try:
		if settings['SSL']['Path'] == 'default':
			raise Exception
		settings['cerPath']=settings['SSL']['Path'] + settings['SSL']['Certificate']
		settings['keyPath']=settings['SSL']['Path'] + settings['SSL']['Key']
	except Exception:
		settings['cerPath']=os.path.join(sys.path[0], settings['SSL']['Certificate'])
		settings['keyPath']=os.path.join(sys.path[0],  settings['SSL']['Key'])
except Exception:
	settings['SSL']= { 'Enabled': False }

try:
	settings['ActiveValue'] = 1 - int(settings['Inverted'])
except Exception:
	settings['ActiveValue'] = 1

try:
	settings['RefreshRate']
except Exception:
	settings['RefreshRate'] = 5

try:
	settings['GPIOMode']
except Exception:
	settings['GPIOMode'] = "BCM"

try:
	settings['Make']
except Exception:
	settings['Make'] = "RaspberryPi"