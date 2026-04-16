#!/usr/bin/env python3

# Import the class and function 

from clean_data_class import People
from read_people_info import read_people_info



# EXERCISE 7: What is the average age difference between the parents (with a child in common obviously)?

child_to_parents = dict()

# Go thoroug all the people's children and add them as a key of a set, and add the parents as the values.
for person in read_people_info('people.db'):
    for child in person.children: 
        if child not in child_to_parents: 
            child_to_parents[child] = []
        child_to_parents[child].append(person)

# Show all the kids CPR and their parents in a list
# for child, parents in child_to_parents.items():
#     print(child, [p.cpr for p in parents])

age_difference = []
for parents in child_to_parents.values(): 
    if len(parents) >= 2: 
        for i in range(len(parents)):
            for j in range(i+1, len(parents)): 
                diff = abs(parents[i].age - parents[j].age)
                age_difference.append(diff)
    
if len(age_difference) > 0: 
    avg_difference = sum(age_difference) / len(age_difference)
else: 
    avg_difference = 0
print(f'The age difference between the paretns with a common kid is {avg_difference:.2f} years')


# Exercise 8: How many people has at least one grandparent that is still alive? A person is living if he/she is in the database. 
# State the number both in percent and as a real number.

people_with_grandparents = 0
total_people = 0

for person in read_people_info('people.db'):
    total_people += 1

    # Find the parents: 
    parents = child_to_parents.get(person.cpr, [])

    # Find the grandparetns 
    has_grandparents = False

    for parent in parents : 
        grandparents = child_to_parents.get(parent.cpr, [])
        if len(grandparents) > 0:  
            has_grandparents = True
            break
    if has_grandparents: 
        people_with_grandparents += 1

percentage_grandparents = (people_with_grandparents/total_people) * 100

print(f'The number of people that has at least one grandparent is {people_with_grandparents} which correspnd to the {percentage_grandparents:.2f}% of the people in the database')