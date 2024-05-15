"""
functions to manage the calendar
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
headers = {"X-MY-CUSTOMER-HEADER": "123"}






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
    

# def add_stuff_to_calendar_demo(calendar):
#     """
#     This demo adds some stuff to the calendar

#     Unfortunately the arguments that it's possible to pass to save_* is poorly documented.
#     https://github.com/python-caldav/caldav/issues/253
#     """
#     ## Add an event with some certain attributes
#     may_event = calendar.save_event(
#         dtstart=datetime(2020, 5, 17, 6),
#         dtend=datetime(2020, 5, 18, 1),
#         summary="Do the needful",
#         rrule={"FREQ": "YEARLY"},
#     )

#     ## not all calendars supports tasks ... but if it's supported, it should be
#     ## told here:
#     acceptable_component_types = calendar.get_supported_components()
#     assert "VTODO" in acceptable_component_types

#     ## Add a task that should contain some ical lines
#     ## Note that this may break on your server:
#     ## * not all servers accepts tasks and events mixed on the same calendar.
#     ## * not all servers accepts tasks at all
#     dec_task = calendar.save_todo(
#         ical_fragment="""DTSTART;VALUE=DATE:20201213
#         DUE;VALUE=DATE:20201220
#         SUMMARY:Chop down a tree and drag it into the living room
#         RRULE:FREQ=YEARLY
#         PRIORITY: 2
#         CATEGORIES: outdoor"""
#     )

#     # ical_fragment parameter -> just some lines
#     # ical parameter -> full ical object