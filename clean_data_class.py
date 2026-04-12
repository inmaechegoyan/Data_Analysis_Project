#!/usr/bin/env python3


# Define a class for all the CPR

class People: 
    def __init__(self, cpr):
        self.cpr = cpr
        self.first_name = None
        self.last_name = None
        self.height = None
        self.weight = None
        self.eye_color = None
        self.blood_type = None
        self.children = []

        # Derived atributes: 
        self.gender = 'F' if int(cpr[-1]) % 2 == 0 else 'M'
        self.age = 100 - int(cpr[4:6])


# Create a generator to iterate through the data


def read_people_info(filename): 

    current_person = None

    try: 

        with open(filename, 'r') as infile: 
            for line in infile: 
                line = line.strip()

                if not line: 
                    continue
                

                if line.upper().startswith('CPR'): 

                    # yield the previous person 
                    if current_person: 
                        yield current_person

                    # if there is no current person: 
                    cpr = line.split(':', 1)[1].strip()
                    current_person = People(cpr)
                    continue
                
                if ': ' in line and current_person is not None: 
                    key, value = line.split(': ', 1)
                    key_lower = key.lower()

                    if key_lower == 'first name': 
                        current_person.first_name = value
                    elif key_lower == 'last name':
                        current_person.last_name = value
                    elif key_lower == 'height':
                        current_person.height = int(value)
                    elif key_lower == 'weight':
                        current_person.weight = int(value)
                    elif key_lower == 'eye color':
                        current_person.eye_color = value
                    elif key_lower == 'blood type':
                        current_person.blood_type = value
                    elif key_lower == 'children':
                        current_person.children = value.split()

    
            # yield last person 
            if current_person: 
                yield current_person

    except IOError as error: 
        print('Cannot open file.Reason: ' + str(error))


# Execute the program 
for person in read_people_info('people.db'):
    print(person.cpr)
    print(person.first_name)
    print(person.last_name)
    print(person.height)
    print(person.weight)
    print(person.eye_color)
    print(person.blood_type)
    print(person.children)
    print(person.age)
   
