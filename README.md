# Air-Traffic-Control-Simulator
# tp-atc

This project is an “Air Traffic Control Simulator” that simulates the real-world air traffic control radar from towers use to manage flights near airports. As a simulator, it mimics the verbal commands controllers use to direct aircraft while having the game aspect of having objectives of directing arrivals and departures. 

Features:
- intelligent airport, runway, flight generation for fresh gameplay
- warnings and constraints based on proximity, fuel, weather (TRY THEM OUT THEY'RE REALLY COOL!)
    - fuel: below 30 seconds of fuel left, game crash at 5 seconds
    - proximity: within safety rings and 1500 altitude difference, game crash when altitude difference is less than 500
    - weather: in the red part of storm, low probability of crashing
- autopilot features including ILS localizer(horizontal), glideslope(vertical), direct, headings, go arounds
- verbal and non-verbal text based command recognition, handling, and execution for flights with typo recognition based on dissimilarity indices
- weather engine with a wind map as well as visual storm features
- weather based airport, aircraft scenarios such as go-arounds, and runway closures

Background Knowledge:

Basic Aviation Vocab

- Heading: Magnetic Bearing of Aircraft (clockwise rotation starting from 12 o'clock at 0 degrees)
- Altitude: use feet units
- Speed: use knot units
- ILS: Instrument Landing System
- Go-Around: Redo Landing After Failed Attempt
- Localizer: Horizontal Landing Guidance
- Glideslope: Vertical Landing Guidance

This project is very specific in detailing in real word aviation. Many codes, and names are real names of airline, aircraft, airport, and procedures guided by the ICAO (International Civil Aviation Organization). This readme provides basic knowledge on the aviation procedures, names, and codes used in this program which should help the user play or even enjoy the game. Aviation vocabulary and abbreviations are referenced in the code to help the user better understand the objective of the code.

Installation and Execution:
All files contained are connected to the main atc_simulator file
Run the atc_simulator python file to start

Libraries:
Python Defaults, PIL

Shortcuts:

command prompt keyword "debug":
use this word to instantly change values

+: Adds new arrival flight
-: Removes the last flight on the list
Up and Down: Scroll through flight list on the sidebar
y: debug mode for dragging planes
x: disable weather visualization
p: pause game
r: new round