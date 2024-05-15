"""
functions to manage the calendar

Remember to use
# with caldav.DAVClient(
#         url=caldav_url,
#         username=username,
#         password=password,
#         headers=headers,  # Optional parameter to set HTTP headers on each request if needed
#     ) as client:
to create a client

see https://github.com/python-caldav/caldav/blob/master/examples/basic_usage_examples.py for more info.
"""
import caldav
# from datetime import date
from datetime import datetime
# from datetime import timedelta

## CONFIGURATION.  Edit here, or set up something in
## tests/conf_private.py (see tests/conf_private.py.EXAMPLE).
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