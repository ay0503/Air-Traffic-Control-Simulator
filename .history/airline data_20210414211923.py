airlines = dict()

for line in list:
    code, name = line.split(",")[0], line.split(",")[1]
    airlines[code] = name

airlineList = """ 

DAL, Delta Airlines
AAL, American Airlines
KAL, Korean Airlines

"""