from airlinedata import airlines

callsign = "DAL123"

def getAirline(callsign):
    code = ''
    for letter in callsign:
        if letter.isalpha():
            code += letter
    return airlines[code]

print(getAirline(callsign))