"""
functions to manage the calendar

Remember to use
# with caldav.DAVClient(
#         url=caldav_url,
#         username=username,
#         password=password,
#         headers=headers,  # Optional parameter to set HTTP headers on each request if needed
#     ) as client:
to create a client object and use it when calling the functions in this file.

see https://github.com/python-caldav/caldav/blob/master/examples/basic_usage_examples.py for more info.
"""
import caldav
# from datetime import date
from datetime import datetime
# from datetime import timedelta

## CONFIGURATION.
caldav_url = "localhost:5232"
username = "me"
password = "password1"





#get calendars
def get_calendars(client : caldav.DAVClient):
    calendars = client.principal().calendars()
    return calendars

#add event
def add_event(calendar : caldav.Calendar, start : datetime, end : datetime, summary : str, description : str) -> None:
    """
    example
        # Add an event with some certain attributes
        may_event = calendar.save_event(
            dtstart=datetime(2020, 5, 17, 6),
            dtend=datetime(2020, 5, 18, 1),
            summary="Do the needful",
            rrule={"FREQ": "YEARLY"}, 
        )
    """
    calendar.save_event(
        ical=f"""BEGIN:VCALENDAR
        BEGIN:VEVENT
        DTSTART:{start} 
        DTEND:{end}
        SUMMARY:{summary}
        DESCRIPTION:{description}
        END:VEVENT
        END:VCALENDAR"""
    )

def get_events(calendar : caldav.Calendar) -> list:
    return calendar.events()

def search_events(calendar : caldav.Calendar, summary : str, start : datetime = None, end : datetime = None) -> list:
    if start and end:
        return calendar.search(
            start=start,
            end=end,
            summary=summary,
            event=True,
            expand=True,
        )
    elif start:
        return calendar.search(
            start=start,
            summary=summary,
            event=True,
            expand=True,
        )
    elif end:
        return calendar.search(
            end=end,
            summary=summary,
            event=True,
            expand=True,
        )
    return calendar.search(
        summary=summary,
        event=True,
        expand=True,
    )
    