import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json

import authenticate
import datehandler
import contacthandler

attendees = []
time = None
weekday = None
length = '1'
summary = ''

#this thing is pretee uglee
def parseArguments(argv):
	iterator = iter(argv)
	for i in iterator:
		if i == '-s':
			summary = next(iterator)
		elif i == '-w':
			weekday = next(iterator)
		elif i == '-t':
			time = next(iterator)
		elif i == '-l':
			length = next(iterator)
		elif i == '-c':
			attendees.append({'email': contacthandler.getEmail(next(iterator))})
		elif i == '-viewcontacts':
			contacthandler.displayContacts()
		elif i == '-addcontact':
			contacthandler.addContacts(next(iterator), next(iterator))

	print(time)
	createAndUploadEvent()

def createAndUploadEvent():
	print(time)
	if checkArguments():
		event = readTemplate()
		date = datehandler.getDateForDayOfWeek(weekday)
		starttime = datehandler.startTime(date, time)
		endtime = datehandler.endTime(starttime, length)
		event['start']['dateTime'] = starttime.isoformat()
		event['end']['dateTime'] = endtime.isoformat()
		event['attendees'] = attendees
		checkEvent(event)
		uploadEvent()

def uploadEvent(event):
	service = authenticate.createService()
	service.events().insert(calendarId='primary', body=event).execute()

def readTemplate():
	with open('default.json') as f:
			default = json.load(f)	
			return default

def checkArguments():
	if time == None:
		print('Event not created missing time.')
		return False
	if weekday == None:
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