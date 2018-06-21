import hashlib, string, random, os, sys, getpass
from functools import wraps
from flask import request, redirect, url_for

passwordHashFilePath = os.path.join(sys.path[0], "passwordhash")
Tokens = []
try:
	passwordHashFile = open(passwordHashFilePath, 'r')
	passwordHashOnFile = passwordHashFile.read()
	passwordHashFile.close()
	requiresPassword = True
except Exception:
	requiresPassword = False

def randomString(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for m in range(length))

def inputPassword():
	password = getpass.getpass()
	print("Re-enter")
	repassword = getpass.getpass()

	if password != repassword:
		print("Passwords don't match. Try again")
		return inputPassword()
	return password

def generatePasswordHash(password):
	h = hashlib.new('sha256')
	h.update(password.encode('utf-8'))
	passwordhash = h.hexdigest()
	return passwordhash

def generatePasswordHashFile(password=''):
	if password == '':
		password = inputPassword()
	passwordhash = generatePasswordHash(password)
	passwordHashFile = open(passwordHashFilePath, 'w+')
	passwordHashFile.write(passwordhash)
	passwordHashFile.close()
	os.chmod(passwordHashFilePath, 0o600)

def checkPassword(password):
	passwordHash = generatePasswordHash(password)
	if passwordHash == passwordHashOnFile:
		return True
	return False

def generateToken(password):
	if checkPassword(password):
		token = randomString(40)
		Tokens.append(token)
		return token
	return

def isAuthenticated():
	if not requiresPassword:
		return True
	try:
		token = request.cookies.get('token')
		if token in Tokens:
			return True
		return False
	except Exception:
		return False

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if isAuthenticated():
			return f(*args, **kwargs)
		return redirect(url_for('login'))
	return decorated_function

def removeToken():
	token = request.cookies.get('token')
	if token in Tokens:
		Tokens.remove(token)