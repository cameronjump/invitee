from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import authenticate

def main():
    service = authenticate.authenticate()
    createEvent(service)

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

def createEvent(service):
	event = {
      'summary': 'Google I/O 2015',
      'location': '800 Howard St., San Francisco, CA 94103',
      'description': 'A chance to hear more about Google\'s developer products.',
      'start': {
        'dateTime': str(datetime.datetime.now() + datetime.timedelta(hours=2)),
        'timeZone': 'America/Chicago',
      },
      'end': {
        'dateTime': str(datetime.datetime.now() + datetime.timedelta(hours=4)),
        'timeZone': 'America/Chicago',
      },
      'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=1'
      ],
      'attendees': [
        {'email': 'cameronjump@gmail.com'},
      ],
      'reminders': {
        'useDefault': True,
      }
    }
	service.events().insert(calendarId='primary', body=event).execute()

if __name__ == '__main__':
    main()