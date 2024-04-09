# User Stories

- U1 Calendar Sync

As a politically involved person who needs to keep track of lots of meeting times, I want meeting information to be automatically synchronized to my phone so I can more easily keep track of what times I need to be at certain places and get reminders so I do not miss any meetings.

- U2 Notes

As a politically involved person who writes lots of notes, I want my notes to be attached to a always up-to-date source of information on the bills that I am taking notes on so I can easily see any information on the bill without having to search for it or go to a different website.

- U3 Data Export

As a politically involved person who has my own method of keeping track of bills, I want to export bill data so I can automatically update my information.

- U4 Bill Tracking

As a politically involved person I want to pay attention to a specified list of bills and be able to view current details on them with automatic updates.

# Requirements

- R1 (U1,2,3,4) The user shall be able to view a list of all bills in progress. It shall use a webserver fetching data from a database. That database will be regularly updated from an external information source.
- R2 (U1,2) The user shall be able to create an account and login to the service. This will be accomplished through the web-browser, by authenticating the user against data stored in a database.
- R3 (U1,2) The user shall be able to mark certain bills as ones they are interested in. This shall be accomplished through the web-browser, with the bills that the user has marked being stored in a database.
- R4 (U2,3,4) The user shall be able to filter bills based on their attributes. This shall be accomplished by converting data the user enters into the web-browser into queries on the database.
- R5 (U1) The user shall receive notifications through their phone’s calendar about upcoming meetings for bills they have marked. This shall be accomplished by a server offering a RFC 5545 compliant API that is backed by the information database (R1) and the bill marking database (R3)
- R6 (U2) The user shall be able to write notes on bills and save those notes to the server. This shall be accomplished through the web-browser, with the notes being stored on a database and connected to the user via their account (R2).
- R7 (U3) The user shall be able to export bill data into a portable file format that can be downloaded. This shall be accomplished through the web-browser using data stored in the bill database (R1) and controlled by user filters (R4)