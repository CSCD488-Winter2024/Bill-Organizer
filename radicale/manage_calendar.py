"""
functions to manage the calendar
"""
import caldav


#get calendars
def get_calendars(client):
    calendars = client.principal().calendars()
    return calendars
