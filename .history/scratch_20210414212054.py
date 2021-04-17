from airline_data import airlines

callsign = "DAL123"

code = ''
for letter in self.callsign:
    if letter.isalpha():
        code += letter
    return airlines[code]