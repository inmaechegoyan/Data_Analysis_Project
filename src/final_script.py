#!/usr/bin/env python3

from data.clean_data_class import People
from src.read_people_info import read_people_info


########################
# FUNCTIONS
######################## igual tenemos que ponerla en otro lado

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


########################
####### VARIABLES ######
########################


# Q1
age_intervals = [(0,10), (10,20), (20,30),(30,40),(40,50),(50,60),(60,70),(70,80),(80,90),(90,100)]
female_counts = [0] * len(age_intervals)
male_counts = [0] * len(age_intervals)
total_female = 0 
total_male = 0 

# Q2
max_age_father = 0
min_age_father = 99
age_count_father = 0 
total_father = 0

# Q3
father_counts = [0] * len(age_intervals)

# Q4
total_mother = 0
max_age_mother = 0
min_age_mother = 99
age_count_mother = 0

# Q5
mother_counts = [0] * len(age_intervals)

# Q6
woman_without_children = 0
men_without_children = 0

# Q7 + RELATIONS
child_to_parents = dict()
parent_to_children = dict()
age_by_cpr = dict()


# Q8
people_with_grandparents = 0
total_people = 0
all_people = set()

# Q10
boys = 0
girls = 0

# Q11–13
gender_by_cpr = dict()
height_category_by_cpr = dict()

# Q14
fat_intervals = ["Underweight", "Normal weight", "Overweight", "Obese"]
people_fat = [0] * len(fat_intervals)
children_fat = [0] * len(fat_intervals)



#####################
### SINGLE PASSS ###
####################


for person in read_people_info('data/people.db'):
    
    cpr = person.cpr
    all_people.add(cpr)
    total_people += 1

    gender_by_cpr[cpr] = person.gender
    height_category_by_cpr[cpr] = height_category(person)
    parent_to_children[cpr] = person.children
    age_by_cpr[cpr] = person.age

    # Q1
    for i, (low,high) in enumerate(age_intervals): 
        if low <= person.age < high: 
            if person.gender == 'F': 
                total_female += 1
                female_counts[i] += 1
            else:
                total_male += 1
                male_counts[i] += 1
            break
    
    # Q2 & Q3
    age_fc = person.age_first_child()
    if person.gender == "M" and age_fc is not None:
        age_count_father += age_fc
        total_father += 1
        max_age_father = max(max_age_father, age_fc)
        min_age_father = min(min_age_father, age_fc)

        for i,(l,h) in enumerate(age_intervals):
            if l <= age_fc < h:
                father_counts[i] += 1
                break
    
    # Q4 & Q5 & Q6
    if person.gender == "F":
        if age_fc is not None:
            age_count_mother += age_fc
            total_mother += 1
            max_age_mother = max(max_age_mother, age_fc)
            min_age_mother = min(min_age_mother, age_fc)

            for i,(l,h) in enumerate(age_intervals):
                if l <= age_fc < h:
                    mother_counts[i] += 1
                    break

        if not person.children:
            woman_without_children += 1
    else:
        if not person.children:
            men_without_children += 1

    
    # Create dict child_to_parents (Q7 base)
    for child in person.children: 
        if child not in child_to_parents: 
            child_to_parents[child] = []
        child_to_parents[child].append(cpr)
    
    # Q10

    first_child_cpr = person.first_child_cpr()
    if(person.children):
        if int(first_child_cpr[-1]) % 2 == 0:
            girls += 1
        else: boys +=1

    # Q14

    bmi = person.bmi()
    if bmi is None:
        continue
    if(bmi < 18.5):
        people_fat[0] += 1
        if(person.children):
            children_fat[0] += 1
    elif( bmi < 24.9):
        people_fat[1] += 1
        if(person.children):
            children_fat[1] += 1
    elif(bmi < 29.9):
        people_fat[2] += 1
        if(person.children):
            children_fat[2] += 1
    elif( 29.9 < bmi):
        people_fat[3] += 1
        if(person.children):
            children_fat[3] += 1  

    


#####################
### POST-PROCESS ###
####################

# Q2 & Q4
avg_age_father = age_count_father / total_father if total_father else 0
avg_age_mother = age_count_mother / total_mother if total_mother else 0

# Q6
percent_women = (woman_without_children / total_female)*100 if total_female else 0
percent_men = (men_without_children / total_male)*100 if total_male else 0

# Q7 

age_difference = []

for parents in child_to_parents.values():
    if len(parents) >= 2:
        for i in range(len(parents)):
            for j in range(i+1, len(parents)):
                age1 = age_by_cpr[parents[i]]
                age2 = age_by_cpr[parents[j]]
                diff = abs(age1 - age2)
                age_difference.append(diff)

avg_difference = sum(age_difference) / len(age_difference) if age_difference else 0

# Q8 

for p in all_people: 
    parents = child_to_parents.get(p, [])
    for parent in parents: 
        if child_to_parents.get(parent):
            people_with_grandparents += 1
            break

percentage_granparents = (people_with_grandparents /total_people) * 100

# Q10
total_children = boys + girls
boys_percentage = (boys / total_children)*100 if total_children else 0
girls_percentage = (girls / total_children)*100 if total_children else 0



# Q11
person_to_partner = {}

for parents in child_to_parents.values(): 
    if len(parents) < 2: 
        continue    # There is no co-parenting 
    
    for i in range(len(parents)):
        for j in range(len(parents)):
            if i == j: 
                continue    # someone can not have kids with themselfs
            
        for i in range(len(parents)):
            for j in range(len(parents)):
                if i != j:
                    person_to_partner.setdefault(parents[i], set()).add(parents[j])

male_total = 0
female_total = 0

male_pluspartner = 0
female_pluspartner = 0

for cpr, g in gender_by_cpr.items():
    partners = person_to_partner.get(cpr, set())

    if g == 'M':
        male_total += 1
        if len(partners) > 1:
            male_pluspartner += 1
    elif g == 'F': 
        female_total += 1
        if len(partners) > 1: 
            female_pluspartner += 1


men_more_partner = (male_pluspartner/male_total)*100 if male_total > 0 else 0 
women_more_partner = (female_pluspartner/female_total)*100 if female_total > 0 else 0 


# Q12


count_couple_type = dict()

for parents in child_to_parents.values():
    if len(parents) < 2: 
        continue


    for i in range(len(parents)):
        for j in range(i+1,len(parents)):
            h1 = height_category_by_cpr[parents[i]]
            h2 = height_category_by_cpr[parents[j]]
            couple = tuple(sorted([h1,h2]))
            count_couple_type[couple] = count_couple_type.get(couple,0)+1

total_couples = sum(count_couple_type.values())






#####################
####### PRINTS #####
####################

# Q1

for i, (low,high) in enumerate(age_intervals):
    female_porcentage = ((female_counts[i]/total_female) * 100) if total_female > 0 else 0
    male_porcentage = (((male_counts[i]/total_male) * 100)) if total_male > 0 else 0 
    print(f'{low}-{high:<8} {female_porcentage:<10.2f} {male_porcentage:10.2f}')



# Q2

print(f"Maximum age of first-time fathers: {max_age_father:.2f}")
print(f"Minimum age of first-time fathers:{min_age_father:.2f}")
print(f"Average age of first-time fathers::{avg_age_father:.2f}")

# Q3

print(f"{'Age range':<10} {'Male %':<10}")

for i, (low, high) in enumerate(age_intervals):
    male_percentage = (father_counts[i] / total_father) * 100 if total_father > 0 else 0
    print(f"{low}-{high:<8} {male_percentage:<10.2f}") 


# Q4

print(f"Maximum age of first-time mothers: {max_age_mother:.2f}")
print(f"Minimum age of first-time mothers:{min_age_mother:.2f}")
print(f"Average age of first-time mothers:{avg_age_mother:.2f}")


# Q5 
print(f"{'Age range':<10} {'Female %':<10}")

for i, (low, high) in enumerate(age_intervals):
    female_percentage = (mother_counts[i] / total_mother) * 100 if total_mother > 0 else 0
    print(f"{low}-{high:<8} {female_percentage:<10.2f}") 

# Q6
print(f"Women without children: {percent_women:.2f}%")
print(f"Men without children: {percent_men:.2f}%")

# Q7

print(f'The age difference between the parents with a common kid is {avg_difference:.2f} years')

# Q8 
print(f'The number of people that has at least one grandparent is {people_with_grandparents} which correspnd to the {percentage_granparents:.2f}% of the people in the database')


# Q12

print(f"{'Couple Type':20} {'Percentage':>10}")
for couple, count in count_couple_type.items(): 
    percentage_couple_types = (count/total_couples)*100
    print(f'{str(couple):20}: {percentage_couple_types:8.2f}%')

