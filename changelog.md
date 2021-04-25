4/13/2021 - 6.2 hours
Start of Project Coding
 - create classes for project (aircraft, airport)
 - create basic display of aircraft
 - create heading to 2d vector conversion

4/14/2021 - 4.3 hours
basic interface
 - sidebar displays aircraft information
 - create aircraft selection feature
 - aircraft dragging feature (debugging)
 - link airlines with hub airports for routes of new aircraft generation
 - create wind display to use for future "special events"

4/15/2021 - 4.4 hours
create arrival generator
 - generates speed
 - generates position and heading based on side of board
 - generates flight number
 - create basic command interface with live typing feature

4/16/2021 - 5.8 hours
 - work on command recognition and execution module
 - create safety ring
 - bug fix bank direction selection
 - vector to heading implementation
 - simplify callsign, airline, flight number conversion with new class attribute
 - bug fix aircraft not stopping on commanded parameters

4/17/2021 - 8 hours
 - polish runway class for implementation
 - bug fix safety rings
 - modify ils interception
 - create ILS beacon for runway class
 - create waypoint class for future
 - change direct waypoint mehthod (needs fixing)
 - use distance function for simplification
 - change naming from aircrafts to flights to add aircraft class
 - create aircraft class and game data with types and data
 - added size limit for airport and size classes for aircraft
 - added aircraft type generation

 4/18/2021 - 11.5 hours
 - created list scroll function using arrow keys
 - fixed non-linked hub generation bug
 - improved visual information of flight data
 - structurized airport generation
 - created ILS wing visual
 - fix command execution bug
 - fix object indexing error for macOS
 - create objects for runways
 - create random airport and runway generation (TODO: create more realistic runway placement)
 - temporarily reverted to static length

 4/19/2021 - 6.2 hours
 - divided flights to departure and arrival classes for future feature implementation
 - added direct to waypoint feature
 - added trajectory visualizer
 - changed waypoint name generation so first letter does not equal airport's first letter
 - runway heading bug fixed
 - created takeoff feature for departure class aircraft
 - departure aircraft now have objective waypoints that pass the flight on to a different controller

 4/20/2021 - 5.5 hours
 - fixed runway heading bug that caused ILS to not recognize beacon
 - simplified heading direction algorithm
 - added fuel features corresponding to aircraft type
 - added details pane to side bar
 - added path drawing feature to aircraft
 - added weather based runway closures to airports
 - improved waypoint direction algorithm
 - added low fuel scenario to unsafe states
 - added new airlines to game
 - fixed departure speed and altitude bugs

 4/21/2021 - 2.1 hours
 - added debug command mode to change flight attributes
 - simplified runway heading generation
 - wind generation fix

 4/23/2021 - 5.1 hours
 - divided overall design structure for better management
 - created typo ratio based typo correction in the command recognition
 - added limit to addable flights
 - added pro mode, easy mode division
 - bug fixes to detail pane
 - calculation updates to landing glideslope calculation
 - changed route structure for departures
 - changed visual bug where waypoint is shown over command prompt
 - added land, sent states for aircraft that have completed objective
 - aircraft now feature transponder codes with special cases (mayday, hijacking)
 - added landing probabilities based on weather states (visibility, crosswinds)
 - new colors for departing and arriving aircraft
 
4/24/2021 - 5.6 hours
- moved draw functions to seperate file for simplicity
- added number only callsign recognition
- added basic typo correction to command recognition

4/25/2021 - 
- added basic control panel to sidebar
- added waypoint selection feature
- added scoring system