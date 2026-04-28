
# function read people's info
from data.clean_data_class import People
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

def height_category(person): 
    if person.gender == 'M':
        if person.height > 187:
            return 'tall'
        elif person.height >= 173:
            return 'normal'
        else: 
            return 'short'
    else:
        if person.height > 175:
            return 'tall'
        elif person.height >= 160:
            return 'normal'
        else: 
            return 'short'
        

def possible_child_blood(parent1, parent2):
    if parent1 == "A" and parent2 == "A":
        return {"A", "O"}
    elif (parent1 == "A" and parent2 == "O") or (parent1 == "O" and parent2 == "A"):
        return {"A", "O"}
    elif (parent1 == "A" and parent2 == "B") or (parent1 == "B" and parent2 == "A"):
        return {"A", "B", "AB", "O"}
    elif parent1 == "B" and parent2 == "B":
        return {"B", "O"}
    elif (parent1 == "B" and parent2 == "O") or (parent1 == "O" and parent2 == "B"):
        return {"B", "O"}
    elif parent1 == "O" and parent2 == "O":
        return {"O"}
    elif (parent1 == "AB" and parent2 == "A") or (parent1 == "A" and parent2 == "AB"):
        return {"A", "B", "AB"}
    elif (parent1 == "AB" and parent2 == "B") or (parent1 == "B" and parent2 == "AB"):
        return {"A", "B", "AB"}
    elif parent1 == "AB" and parent2 == "AB":
        return {"A", "B", "AB"}
    elif (parent1 == "AB" and parent2 == "O") or (parent1 == "O" and parent2 == "AB"):
        return {"A", "B"}
    return set()

def possible_child_rh(parent1, parent2):
    if parent1 == "+" and parent2 == "+":
        return {"+", "-"}
    elif (parent1 == "+" and parent2 == "-") or (parent1 == "-" and parent2 == "+"):
        return {"+", "-"}
    elif (parent1 == "-" and parent2 == "-"):
        return {"-"}
    return set()

def can_donate_blood(blood_type):
    if blood_type == "A" :
        return {"A", "AB"}
    elif (blood_type == "B"):
        return {"B", "AB"}
    elif (blood_type == "AB"):
        return {"AB"}
    elif (blood_type == "O"):
        return {"A","B","O","AB"}
    return set()