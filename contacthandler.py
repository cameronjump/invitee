import json

def readContacts():
	with open('contacts.json') as f:
		contacts = json.load(f)	
	return contacts

def writeContacts(contacts):
	with open('contacts.json', 'w') as f:
		json.dump(contacts, f)

def addContacts(name, email):
	contacts = readContacts()
	contacts[name] = email
	writeContacts(contacts)

def getEmail(name):
	return readContacts()[name]

def displayContacts():
	print(readContacts())
