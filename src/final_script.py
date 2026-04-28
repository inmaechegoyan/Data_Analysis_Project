#!/usr/bin/env python3

from data.clean_data_class import People
from src.read_people_info import read_people_info
from src.read_people_info import height_category
from src.read_people_info import possible_child_blood
from src.read_people_info import possible_child_rh
from src.read_people_info import can_donate_blood


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

        for i,(low,high) in enumerate(age_intervals):
            if low <= age_fc < high:
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

# Q9 

cousins_pair = []

for person in all_people:
    # For each person get the parents: 
    parents = child_to_parents.get(person, [])

    # For each parent in the list, get their parents (grandparents)
    for parent in parents: 
        grandparents = child_to_parents.get(parent, [])

        # For each grandparent, obtain their kids (aunt/uncles + parents)
        for grandparent in grandparents: 
            siblings = parent_to_children.get(grandparent,[])

            for sibling in siblings: 
                # We dont want to take the parents of the current person, just the incles or aunties 
                if sibling == parent: 
                    continue

                # Kids from uncles and aunts: 
                cousins = parent_to_children.get(sibling,[])

                for cousin in cousins: 
                    # Cannot count the current person: 
                    if cousin != person: 
                        cousins_pair.append((person,cousin))

# We will have duplicates, so we have to do a set to erase them
cousins_pair = list(set(cousins_pair))
length = len(cousins_pair)

# calculate cousin average: 

counsin_per_person = {}
for a,b in cousins_pair: 
    if a not in counsin_per_person:
        counsin_per_person[a] = set()
    counsin_per_person[a].add(b)

avg = sum(len(v) for v in counsin_per_person.values()) / len(counsin_per_person)





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

# Q13

tall_and_tall = 0
parent_tall_total = 0

for child, parents in child_to_parents.items():
    if len(parents) < 2: 
        continue

    # obtain parents height
    parent_categories = []

    for parent in parents: 
        parent_categories.append(height_category_by_cpr[parent])

    # check if all the parents of a child are tall 
    all_parents_tall  = True

    for p in parent_categories: 
        if p != 'tall':
            all_parents_tall = False
            break

    # check if both parents are tall: 
    if all_parents_tall: 
        parent_tall_total += 1

        # check if the kid is also tall 
        if height_category_by_cpr[child] == 'tall': 
            tall_and_tall += 1



###################
##### PRINTS #####
##################

# Q1
print('\nQ1\n')

for i, (low,high) in enumerate(age_intervals):
    female_porcentage = ((female_counts[i]/total_female) * 100) if total_female > 0 else 0
    male_porcentage = (((male_counts[i]/total_male) * 100)) if total_male > 0 else 0 
    print(f'{low}-{high:<8} {female_porcentage:<10.2f} {male_porcentage:10.2f}')



# Q2

print('\nQ2\n')

print(f"Maximum age of first-time fathers: {max_age_father:.2f}")
print(f"Minimum age of first-time fathers:{min_age_father:.2f}")
print(f"Average age of first-time fathers::{avg_age_father:.2f}")

# Q3

print('\nQ3\n')

print(f"{'Age range':<10} {'Male %':<10}")

for i, (low, high) in enumerate(age_intervals):
    male_percentage = (father_counts[i] / total_father) * 100 if total_father > 0 else 0
    print(f"{low}-{high:<8} {male_percentage:<10.2f}") 


# Q4
print('\nQ4\n')

print(f"Maximum age of first-time mothers: {max_age_mother:.2f}")
print(f"Minimum age of first-time mothers:{min_age_mother:.2f}")
print(f"Average age of first-time mothers:{avg_age_mother:.2f}")


# Q5 
print('\nQ5\n')

print(f"{'Age range':<10} {'Female %':<10}")

for i, (low, high) in enumerate(age_intervals):
    female_percentage = (mother_counts[i] / total_mother) * 100 if total_mother > 0 else 0
    print(f"{low}-{high:<8} {female_percentage:<10.2f}") 

# Q6

print('\nQ6\n')

print(f"Women without children: {percent_women:.2f}%")
print(f"Men without children: {percent_men:.2f}%")

# Q7
print('\nQ7\n')
print(f'The age difference between the parents with a common kid is {avg_difference:.2f} years')

# Q8 
print('\nQ8\n')
print(f'The number of people that has at least one grandparent is {people_with_grandparents} which correspnd to the {percentage_granparents:.2f}% of the people in the database')

# Q9

print('\nQ9\n')
print(f'The number of people that have cousins is {length} people')

print(f'The average number of cousins per person is {avg:.2f}')

# Q10
print('\nQ10\n')

print(f"Firstborn likely to be female: {girls_percentage:.2f}%")
print(f"Firstborn likely to be male: {boys_percentage:.2f}%")
   
# Q11
print('\nQ11\n')

print(f"{'':25}{'Men':5}{'Women':5}")
print(f"{'Multiple partners (%)':25}{men_more_partner:5}{women_more_partner:5}")
print(f"{'Total':25}{male_total:5}{female_total:5}")


# Q12

print('\nQ12\n')

print(f"{'Couple Type':20} {'Percentage':>10}")
for couple, count in count_couple_type.items(): 
    percentage_couple_types = (count/total_couples)*100
    print(f'{str(couple):20}: {percentage_couple_types:8.2f}%')

# Q13

print('\nQ13\n')

if parent_tall_total > 0 : 
    probability = tall_and_tall / parent_tall_total
    print(f'P(tall child | tall parents) = {probability:.2f}')
else: 
    print('There is no enought data')

# Q14

print('\nQ14\n')

print("Distribution of people according to their weight and bmi")
for i, label in enumerate(fat_intervals):
    fat_percentage = (people_fat[i] / total_people) * 100 if total_people > 0 else 0
    print(f"{label}  {fat_percentage:.2f}%  ({people_fat[i]}/{total_people})") 

print("")
print("Distribution of people having children according to their weight and bmi")
for i, label in enumerate(fat_intervals):
    children_fat_percentage = (children_fat[i] / people_fat[i]) * 100 if total_people > 0 else 0
    print(f"{label}  {children_fat_percentage:.2f}%  ({children_fat[i]}/{people_fat[i]})") 


