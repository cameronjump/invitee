import json

def readContacts():
	try:
		with open('./src/contacts.json') as f:
			contacts = json.load(f)	
			return contacts
	except Exception as e:
		print('Creating contact file.')
		contacts = {"example": "name@example.com"}
		writeContacts(contacts)
		return contacts

def writeContacts(contacts):
	with open('./src/contacts.json', 'w') as f:
		json.dump(contacts, f)

def addContacts(name, email):
	contacts = readContacts()
	contacts[name] = email
	writeContacts(contacts)
	print('Updated contact list\n'+str(contacts))

def getEmail(name):
	try:
		return readContacts()[name]
	except Exception as e:
		raise Exception('Contact '+name+' is not in your contact book.')

def displayContacts():
	print(readContacts())
