import sys
from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import authenticate
import datehandler

def main(argv):
    service = authenticate.createService()
    createEvent(service)

def createEvent(service):
	date = datehandler.getDateForDayOfWeek('saturday')
	summary = 'pizza'
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
      'summary': summary,
      'location': location,
      'description': description,
      'start': {
        'dateTime': starttime.isoformat(),
        'timeZone': timezone,
      },
      'end': {
        'dateTime': endtime.isoformat(),
        'timeZone': timezone,
      },
      'attendees': [
        {'email': 'cameronjump@gmail.com'},
      ],
      'reminders': {
        'useDefault': True,
      }
    }
	service.events().insert(calendarId='primary', body=event).execute()

def displayNextTen(service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == '__main__':
    main(sys.argv)