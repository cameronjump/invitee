import datetime
import time

#input day of week string
#output date for next occurence of that day
def getDateForDayOfWeek(dayofweek):
	date = datetime.datetime.now()
	dayofweek = dayofweek.lower()
	weekday = {'monday':0,'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5, 'sunday':6}
	try:
		while date.weekday() != weekday[dayofweek]:
			date += datetime.timedelta(days=1)
	except Exception as e:
		print('Given weekday invalid.')
		raise e
	return date

#input timezone string
#output coresponding timezone string
def getTimeZone(timezone):
	timezone = timezone.lower()
	zones = {'central':'America/Chicago','pacific':'America/Los_Angeles','mountian':'America/Denver','eastern':'America/New_York'}
	try:
		return zones[timezone]
	except Exception as e:
		print('Given weekday invalid. Using default timezone American/Chicago.')
		return 'America/Chicago'

def startTime(date, time):
	split= time.split(':')
	date = date.replace(hour=int(split[0]),minute=int(split[1]))
	return date

def endTime(date, length):
	date += datetime.timedelta(hours=int(length))
	
	return date
	

def test():
	date = getDateForDayOfWeek('saturday')
	print(date)

	zone = getTimeZone('pacific')
	print(zone)

test()