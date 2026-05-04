#!/usr/bin/env python3

# Import the class and function 

from Data_Analysis_Project.src.people_class import People
from Data_Analysis_Project.src.functions import read_people_info



#####################
#### EXERCISE 7 ####
####################

# EXERCISE 7: What is the average age difference between the parents (with a child in common obviously)?

child_to_parents = dict()

# Go thoroug all the people's children and add them as a key of a set, and add the parents as the values.
for person in read_people_info('data/people.db'):
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



#####################
#### EXERCISE 8 ####
####################

# Exercise 8: How many people has at least one grandparent that is still alive? A person is living if he/she is in the database. 
# State the number both in percent and as a real number.

people_with_grandparents = 0
total_people = 0

for person in read_people_info('data/people.db'):
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



#####################
#### EXERCISE 9 ####
####################

# Exercise 9: How many has at least one cousin in the data set? What is the average number of cousins based on those who have cousins?
# Note: This number is historically difficult to compute right, but here are some thoughts to help you out in verifying your count.
# You have to construct a method for finding cousin pairs. Any cousin pair you identify, can be written as a tuple (cpr1, cpr2) in a list.
# a) There should be no duplicate tuples in the list - you are not cousins with the same person more than once.
# b) There should be no tuple with the same cpr on position 1 and 2 - you are not cousins with yourself.
# c) Because of symmetry, it is expected that for any (cpr1, cpr2) tuple there is a (cpr2, cpr1) tuple - when you are cousins with somebody, 
# somebody is cousins with you. This has natural consequences: Set(cpr1) == Set(cpr2), Sorted_list(cpr1) == Sorted_list(cpr2).
# d) This list does NOT discover sibling pairs inserted as cousins, however there should be no overlap of this list and a similar list covering sibling pairs.
# e) The length of the list of cousin tuples is the num


###########################
#### Find cousins pairs ##
##########################

parent_to_children = dict()
cousins_pair = []

for person in read_people_info('data/people.db'):

    # Reuse the child_to_parents dict that i did for previous exercises (child : [parent1, parent2..])
    # Create another dict parent_to_children ( parent : [child1, child2... ])
    parent_to_children[person.cpr] = person.children

    # For each person get the parents: 
    parents = child_to_parents.get(person.cpr, [])

    # For each parent in the list, get their parents (grandparents)
    for parent in parents: 
        grandparents = child_to_parents.get(parent.cpr, [])

        # For each grandparent, obtain their kids (aunt/uncles + parents)
        for grandparent in grandparents: 
            siblings = parent_to_children.get(grandparent.cpr, [])

            for sibling in siblings: 
                # We dont want to take the parents of the current person just the uncles/auntis 
                if sibling == parent.cpr: 
                    continue

                # Kids form uncleas and aunts: 
                cousins = parent_to_children.get(sibling,[])

                for cousin in cousins: 
                    # Cannot count the current person: 
                    if cousin != person.cpr: 
                        cousins_pair.append((person.cpr, cousin))

# As we will have duplicates, we can do a set to erease them 
cousins_pair = list(set(cousins_pair))

length = len(cousins_pair)
print(f'The number of people that have cousins is {length} people')

# Cousins average 

cousin_per_person = {}
for a,b in cousins_pair: 
    if a not in cousin_per_person: 
        cousin_per_person[a] = set()
    cousin_per_person[a].add(b)

avg = sum(len(v) for v in cousin_per_person.values()) / len(cousin_per_person)
print(f'The average number of cousins per person is {avg:.2f}')




#####################
#### EXERCISE 11 ###
####################

# How many men/women (percentage) have children with more than one woman/man?


person_to_partner = {}

# create a¡
for parents in child_to_parents.values(): 
    if len(parents) < 2: 
        continue    # There is no co-parenting 
    
    for i in range(len(parents)):
        for j in range(len(parents)):

            if i == j: 
                continue    # someone can not have kids with themselfs
            
            parent1 = parents[i]
            parent2 = parents[j]

            if parent1.cpr not in person_to_partner: 
                person_to_partner[parent1.cpr] = set()  # Create a set so partners are not duplicated

            person_to_partner[parent1.cpr].add(parent2.cpr)     # if the person is already in the dict, add the partner

# Variables: 

male_total = 0
female_total = 0

male_pluspartner = 0
female_pluspartner = 0

for person in read_people_info('data/people.db'):
    partner = person_to_partner.get(person.cpr, set())

    if person.gender == 'M':
        male_total += 1
        if len(partner) > 1:
            male_pluspartner += 1
    elif person.gender == 'F': 
        female_total += 1
        if len(partner) > 1: 
            female_pluspartner += 1

# Calculate percentages: 

men_more_partner = (male_pluspartner/male_total)*100 if male_total > 0 else 0 
women_more_partner = (female_pluspartner/female_total)*100 if female_total > 0 else 0 

## Display RESULT ##

print(f"{'':25}{'Men':5}{'Women':5}")
print(f"{'Multiple partners (%)':25}{men_more_partner:5}{women_more_partner:5}")
print(f"{'Total':25}{male_total:5}{female_total:5}")



#####################
#### EXERCISE 12 ###
####################

# Do tall people marry (or at least get children together)? To answer that, calculate the percentages of tall/tall, tall/normal, 
# tall/short, normal/normal, normal/short, and short/short couples. Decide your own limits for tall, normal and short, and if 
# they are the same for men and women.

# Classify the people according to their gender and height and return the classification accordin to it
def heigth_category(person): 
    if person.gender == 'M':
        if person.height > 187:
            return 'tall'
        elif person.height >= 173:
            return 'normal'
        else: 
            return 'short'
    elif person.gender == 'F':
        if person.height > 175:
            return 'tall'
        elif person.height >= 160:
            return 'normal'
        else: 
            return 'short'


# Identify the type of couples

count_couple_type = dict()

for parents in child_to_parents.values():
    if len(parents) < 2: 
        continue


    for i in range(len(parents)): 
        for j in range(i+1, len(parents)):
            parent1 = parents[i]
            parent2 = parents[j]

            height1 = heigth_category(parent1)
            height2 = heigth_category(parent2)

            couple = tuple(sorted([height1, height2]))

            if couple not in count_couple_type: 
                count_couple_type[couple] = 0
            count_couple_type[couple] += 1   # sum 1 according to the type of couple
    
total_couples = sum(count_couple_type.values())

# Display result:


print(f"{'Couple Type':20} {'Percentage':>10}")
for couple, count in count_couple_type.items(): 
    percentage_couple_types = (count/total_couples)*100
    print(f'{str(couple):20}: {percentage_couple_types:8.2f}%')





#####################
#### EXERCISE 13 ###
####################

# Do tall parents get tall children?

height_by_cpr = dict()
child_to_parents = dict()

for person in read_people_info('data/people.db'): 

    # Save the height of each person 
    height_by_cpr[person.cpr] = heigth_category(person)

    for child in person.children: 
        if child not in child_to_parents: 
            child_to_parents[child] = []
        child_to_parents[child].append(person.cpr)

    tall_and_tall = 0
    parent_tall_total = 0

for child, parents in child_to_parents.items():
    if len(parents) < 2: 
        continue
    
    # Obtain parents height 
    parent_categories = []

    for parent in parents: 
        parent_categories.append(height_by_cpr[parent])
    
    # Check if all the parents of a child are tall 

    all_parents_tall = True

    for p in parent_categories: 
        if p != 'tall': 
            all_parents_tall = False
            break 

    # check if both parents are tall
    if all_parents_tall: 
        parent_tall_total += 1

        # check if the kid is also tall 
        if height_by_cpr[child] == 'tall': 
            tall_and_tall += 1

#### DISPLAY RESULT ####

if parent_tall_total > 0 : 
    probability = tall_and_tall / parent_tall_total
    print(f'P(tall child | tall parents) = {probability:.2f}')
else: 
    print('There is no enought data')

