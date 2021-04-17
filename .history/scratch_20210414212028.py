from airline_data import airlines

callsign = "DAL123"

airlines = dict()

code = ''
for letter in self.callsign:
    if letter.isalpha():
        code += letter
    airlines.get(code)
    return airlines[code]