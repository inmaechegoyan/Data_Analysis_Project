# Using the knowledge of blood group type inheritance, are there any children
# in the database where you can safely say that at least one of the parents 
# are not the real parent. If such children exists, make a list of them. In the 
# report you must discuss how you determine that the parent(s) of the child are not 
# the "true" parents

from data.clean_data_class import People
from src.read_people_info import read_people_info

child_to_parents = dict()

# Go thoroug all the people's children and add them as a key of a set, and add the parents as the values.
for person in read_people_info('data/people.db'):
    for child in person.children: 
        if child not in child_to_parents: 
            child_to_parents[child] = []
        child_to_parents[child].append(person.cpr)

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


adopted_children = []
adopted_count = 0
not_adopted_count = 0
parent_cant_donate = []
cant_donate_count = 0
can_donate_count = 0

for child, parents in child_to_parents.items():

    blood_type_1 = ""
    blood_type_2 = ""
    rh1 = ""
    rh2 = ""
    if len(parents) != 2:
        continue
    # Look for parents blood type
    for person in read_people_info('data/people.db'):
        
        if person.cpr == parents[0]:
            blood_type_1 = person.blood_type[:-1]
            rh1 = person.blood_type[-1]
        elif person.cpr == parents[1]:
            blood_type_2 = person.blood_type[:-1]
            rh2 = person.blood_type[-1]

    # Calculate child possible blood types
    possible_blood = possible_child_blood(blood_type_1, blood_type_2)
    possible_rh = possible_child_rh(rh1, rh2)

    # Calculate who can the parents donate
    donate_parent1 = can_donate_blood(blood_type_1)
    donate_parent2 = can_donate_blood(blood_type_2)


    # Search child's blood type
    for person in read_people_info('data/people.db'):
        if person.cpr == child:
            child_blood = person.blood_type[:-1]
            child_rh = person.blood_type[-1]

            if (child_blood not in possible_blood) or (child_rh not in possible_rh):
                adopted_children.append(child)
                adopted_count += 1
            else: 
                not_adopted_count += 1
            
            if(child_blood not in donate_parent1):
                parent_cant_donate.append(parents[0])
                cant_donate_count += 1
            else: can_donate_count += 1
            if(child_blood not in donate_parent2):
                parent_cant_donate.append(parents[1])
                cant_donate_count += 1
            else: can_donate_count +=1




print(cant_donate_count)
print(can_donate_count)



# Make a list of fathers who can donate blood to their sons. The list must identify
# the father and the son(s) and their blood type. You must write the length of the 
# list in the report, together with the number of fathers and the number of sons.

