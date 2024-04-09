# Project Description

Create a website for viewing details on upcoming Washington state legislature actions. The website will fetch data on
current bills from relevant websites and display that data in an easy-to-navigate manner. Users will be able to
synchronize legislature meeting times to their local calendar, track selected bills, follow various persons to
automatically track bills that they have created, and export collected data. Users will be able to search through
collected data using various filters. Users will be able to view the history of any bill, including what actions have
been taken on the bill, the current status of the bill, and people involved with the bill.

# User Stories

* As a politically involved person who needs to keep track of lots of meeting times, I want meeting information to be
  automatically synchronized to my phone so I can more easily keep track of what times I need to be at certain places
  and get reminders so I do not miss any meetings
* As a politically involved person who writes lots of notes, I want my notes to be attached to a always up-to-date
  source of information on the bills that I am taking notes on so I can easily see any information on the bill without
  having to search for it or go to a different website.
* As a politically involved person who has my own method of keeping track of bills, I want to export bill data so I can
  automatically update my information.

# Glossary

* WSL: [Washington State Legislature](https://leg.wa.gov/). The website that we will be fetching bill information from.
* RFC 5545/ICalendar: [Internet Calendaring and Scheduling Core Object Specification](https://datatracker.ietf.org/doc/html/rfc5545) The specification that we will use to synchronize meeting information with user's calendars.