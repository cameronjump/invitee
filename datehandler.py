import datetime

#input day of week string
#output date for next occurence of that day
def getDateForDayOfWeek(date, dayofweek):
	dayofweek = dayofweek.lower()
	weekday = {'monday':0,'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5, 'sunday':6}
	try:
		while date.weekday() != weekday[dayofweek]:
			date = date + datetime.timedelta(days=1)
	except Exception as e:
		print('Given weekday invalid.')
		raise e
	return date

def getTimeZone(timezone):
	timezone = timezone.lower()
	zones = {'central':'America/Chicago','pacific':'America/Los_Angeles','mountian':'America/Denver','eastern':'America/New_York'}
	try:
		return zones[timezone]
	except Exception as e:
		print('Given weekday invalid. Using default timezone American/Chicago.')
		return 'America/Chicago'

def test():
	date = getDateForDayOfWeek(datetime.datetime.today(), 'saturday')
	print(date)

	zone = getTimeZone('pacific')
	print(zone)

test()