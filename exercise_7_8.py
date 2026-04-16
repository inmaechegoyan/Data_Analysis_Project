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
print(f'The age difference between the paretns with a common kid is {avg_difference:.2f} years')



# EXERCISE 9: How many has at least one cousin in the data set? What is the average number of cousins based on those who have cousins?

# Note: This number is historically difficult to compute right, but here are some thoughts to help you out in verifying your count.
# You have to construct a method for finding cousin pairs. Any cousin pair you identify, can be written as a tuple (cpr1, cpr2) in a list.
# a) There should be no duplicate tuples in the list - you are not cousins with the same person more than once.
# b) There should be no tuple with the same cpr on position 1 and 2 - you are not cousins with yourself.
# c) Because of symmetry, it is expected that for any (cpr1, cpr2) tuple there is a (cpr2, cpr1) tuple - when you are cousins with somebody, somebody is cousins with you. This has natural consequences: Set(cpr1) == Set(cpr2), Sorted_list(cpr1) == Sorted_list(cpr2).
# d) This list does NOT discover sibling pairs inserted as cousins, however there should be no overlap of this list and a similar list covering sibling pairs.
# e) The length of the list of cousin tuples is the number of cousin pairs, and the size of the set of cpr's is the number of people who have cousins.

