1. Present the problem statement. For example, an average homeowner designing a new house wants to play with options for installing solar panels.

* A politically involved person wants to follow the progress of bills in the Washington State Legislature and keep track of hearings and meeting times, as well as keep organized notes on bills in progress.

1. Explain who the intended user is. It can be you or a fictitious entity you will represent. For example, the user is a homeowner building a new house.

* People who want to follow along with Washington state legislature actions.

1. Describe why the user has this problem. For example, there are decisions to make and many options, which are difficult to manage for the average user.

* It can be difficult and time consuming to keep track of meeting times and bills currently proceeding through the Washington State Legislature.

1. Describe how a solution would benefit the user. For example, maximizing the solar generation while minimizing the cost saves the homeowner money. Stay within the scope of the problem; e.g., do not consider climate change because the connection is too indirect.

* It would save time and accurately automate the process for gathering meeting information.

1. Describe the general flow for addressing the problem. The existing (or imagined) flow does not have to involve a computation solution. For example, the user defines the property and house layout and expected energy needs, then the system proposes solutions that best satisfy the criteria. This used to be done on paper by expensive expert contractors.

* The user sees a list of all the bills currently in progress. The user selects the bills they are interested in following. The software generates a list of all the relevant information on the bill, as well as any upcoming meeting times. The software displays the data. The software gives the user the option to export the data, as well as exposing a calendar feed that can be imported into a phone.

1. What is the general nature of the solution? For example, app, standalone program, website, plug-in.

* Website, and a RFC 5545/ICalendar compliant calendar API.

1. List the general software components you envision playing a role. For example, web server, database, game engine.

* Python for the backend and API.
* MariaDB for storing user and bill information.
* JavaScript/HTML/CSS website for user interaction.
* RFC 5545/ICalendar specification for synchronizing meetings with user's calendars.
* Docker for deployment and instance management.

1. List the general hardware components you envision playing a role. For example, drone, VR headset, tablet. You are responsible for your own hardware, so be reasonable.

* Server
* Device with internet access

1. Describe similar solutions, if any, and justify (or make up a justification) for why they are inadequate. For example, Project XYZ does something similar, but its cost and complexity are prohibitive. Do not get detailed with software engineering aspects. Requirements and specifications, for example, come later in the process, unless they are directly relevant to the proposal and have a justification. For example, an Android app because you have an Android device and want to become an app developer.

* The legislation website has some of these features, but does not provide an easy way to track multiple bills, does not let users export data, does not let users synchronize to their calendar, and does not let users add their own notes.