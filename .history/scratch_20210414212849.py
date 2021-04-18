from airlinedata import airlines

callsign = "DAL123"
code = ''

def getAirline(callsign):
    for letter in callsign:
        if letter.isalpha():
            code += letter
    return airlines[code]

print(getAirline(callsign))