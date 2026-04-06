file = "people.db"
people = {}

current_cpr = None

with open(file) as p:
    for line in p:
        line = line.strip() #remove spaces

        if not line: # for blank lines between people
            continue

        if line.startswith("CPR:"): 
            current_cpr = line.split(": ", 1)[1] 
            people[current_cpr] = {} # keys from principal dictionary (CPRs)

        else:
            if ": " in line:
                key, value = line.split(": ", 1)
                people[current_cpr][key] = value 

print(people)