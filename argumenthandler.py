import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json

import authenticate
import datehandler
import contacthandler


def passArgument(argv):
	service = authenticate.createService()
	event = buildEvent(argv)
	service.events().insert(calendarId='primary', body=event).execute()

def buildEvent(argv):
	#event = {}
	with open('default.json') as f:
		event = json.load(f)
	attendees = []
	time = ''
	weekday = ''
	length = '1'
	iterator = iter(argv)
	for i in iterator:
		if i == '-s':
			event['summary'] = next(iterator)
		elif i == '-w':
			weekday = next(iterator)
		elif i == '-t':
			time = next(iterator)
		elif i == '-l':
			length = next(iterator)
		elif i == '-c':
			attendees.append({'email': contacthandler.getEmail(next(iterator))})
	date = datehandler.getDateForDayOfWeek(weekday)
	starttime = datehandler.startTime(date, time)
	endtime = datehandler.endTime(starttime, length)
	event['start']['dateTime'] = starttime.isoformat()
	event['end']['dateTime'] = endtime.isoformat()
	event['attendees'] = attendees
	return event

def createEvent(service, summary):
	date = datehandler.getDateForDayOfWeek('sunday')
	description = ''
	location = 'my house'
	weekday = 'saturday'
	timezone = datehandler.getTimeZone('central')
	time = '12:30'
	length = '1'
	date = datehandler.getDateForDayOfWeek(weekday)
	starttime = datehandler.startTime(date, time)
	endtime = datehandler.endTime(starttime, length)
	event = {
	  'kind': 'calendar#event',
	  'summary': summary,
	  'location': 'my house',
	  'start': {
	    'dateTime': '2018-08-11T10:30:00-05:00',
	    'timeZone': 'America/Chicago'
	  },
	  'end': {
	    'dateTime': '2018-08-11T11:30:00-05:00',
	    'timeZone': 'America/Chicago'
	  },
	  'sequence': 0,
	  'attendees': [
	    {
	      'email': 'cameronjump@gmail.com',
	    },
	    {
	      'email': 'crjump@ostatemail.okstate.edu',
	    }
	  ],
	  'reminders': {
	    'useDefault': False,
	    'overrides': [
	      {
	        'method': 'popup',
	        'minutes': 30
	      }
	    ]
	  }
	}
	service.events().insert(calendarId='primary', body=event).execute()

def printNextEvent(service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting next event.')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    print(events[0])