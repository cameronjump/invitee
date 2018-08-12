import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json

import authenticate
import datehandler
import contacthandler

#this thing is pretee uglee
def parseArguments(argv):
	#used to build paramters
	config = {'time':None,'weekday':None,'length':'1'}

	#placed directly in to event
	param = {'attendees':[],'summary':'','location':''}

	iterator = iter(argv)
	for i in iterator:
		if i == '-s':
			param['summary'] = next(iterator)
		elif i == '-w':
			config['weekday'] = next(iterator)
		elif i == '-t':
			config['time'] = next(iterator)
		elif i == '-l':
			param['location'] = next(iterator)
		elif i == '-length':
			config['length'] = next(iterator)
		elif i == '-c':
			param['attendees'].append({'email': contacthandler.getEmail(next(iterator))})
		elif i == '-viewcontacts':
			contacthandler.displayContacts()
		elif i == '-addcontact':
			contacthandler.addContacts(next(iterator), next(iterator))
	createAndUploadEvent(config, param)

def createAndUploadEvent(config, param):
	if checkArguments(config):
		event = readTemplate()

		date = datehandler.getDateForDayOfWeek(config['weekday'])
		starttime = datehandler.startTime(date, config['time'])
		endtime = datehandler.endTime(starttime, config['length'])

		event.update(param)

		event['start']['dateTime'] = starttime.isoformat()
		event['end']['dateTime'] = endtime.isoformat()
	
		uploadEvent(event)

def uploadEvent(event):
	service = authenticate.createService()
	service.events().insert(calendarId='primary', body=event).execute()

def readTemplate():
	with open('./src/default.json') as f:
			default = json.load(f)	
			return default

def checkArguments(config):
	if config['time'] == None:
		print('Event not created missing time.')
		return False
	if config['weekday'] == None:
		print('Event not created missing weekday.')
		return False
	return True

def printNextEvent(service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting next event.')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    print(events[0])