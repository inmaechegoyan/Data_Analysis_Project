#!/usr/bin/env python3

from src.people_class import People
from src.functions import read_people_info
from src.functions import height_category
from src.functions import possible_child_blood
from src.functions import possible_child_rh
from src.functions import can_donate_blood
from src.functions import bmi_category


##################################
###### Compelexity Notation ######
##################################

"""
n = total number of people in the database
k = average number of children / familily relation per person 
m = total numeber of parent-child relationships

"""


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
father_counts = [0] * 100
max_age_father = 0
min_age_father = 99
age_count_father = 0 
total_father = 0


# Q4
mother_counts = [0] * 100
total_mother = 0
max_age_mother = 0
min_age_mother = 99
age_count_mother = 0


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
fat_intervals = ["Underweight", "Normal weight", "Preobese", "Obese"]
people_fat = [0] * len(fat_intervals)
children_fat = [0] * len(fat_intervals)
bmi_category_by_cpr = {}
bmi_couple_type = {}


# Q15
blood_type_by_cpr = dict()


#####################
### SINGLE PASSS ###
####################

# read_people_info go through the database only once : O(n)

for person in read_people_info('data/people.db'):   # O(n)
    
    cpr = person.cpr                                # O(1)
    all_people.add(cpr)                             # O(1)
    total_people += 1                               # O(1)

    # Store basic attibutes for fast later access
    gender_by_cpr[cpr] = person.gender              # O(1)
    height_category_by_cpr[cpr] = height_category(person)    # O(1)
    parent_to_children[cpr] = person.children       # O(1)
    age_by_cpr[cpr] = person.age
    blood_type_by_cpr[cpr] = person.blood_type      # O(1)

    # Q1: Age and gender distribution 
    # age_interval has a fixed size (10)
    # Assing person to an age interval 
    for i, (low,high) in enumerate(age_intervals):       # O(1)
        if low <= person.age < high: 
            if person.gender == 'F': 
                total_female += 1
                female_counts[i] += 1
            else:
                total_male += 1
                male_counts[i] += 1
            break
    
    # Q2 & Q3: Age at first child (fathers) 
    age_fc = person.age_first_child()
    if person.gender == "M" and age_fc is not None:
        age_count_father += age_fc
        total_father += 1
        max_age_father = max(max_age_father, age_fc)
        min_age_father = min(min_age_father, age_fc)
        father_counts[age_fc] += 1
    
    # Q4 & Q5 & Q6: Mothers and people without children 
    if person.gender == "F":
        if age_fc is not None:
            age_count_mother += age_fc
            total_mother += 1
            max_age_mother = max(max_age_mother, age_fc)
            min_age_mother = min(min_age_mother, age_fc)

            mother_counts[age_fc] += 1
            
        # Women without children 
        if not person.children:
            woman_without_children += 1
    else:
        # Men without children 
        if not person.children:
            men_without_children += 1

    
    # Create dict child_to_parents (Q7 base)
    for child in person.children:             # O(k)
        if child not in child_to_parents:     # O(1)
            child_to_parents[child] = []      # O(1)
        child_to_parents[child].append(cpr)   # O(1)

    
    # Q10: First child gender distribution 

    first_child_cpr = person.first_child_cpr()  # O(1)
    if(person.children):
        if int(first_child_cpr[-1]) % 2 == 0:
            girls += 1
        else: boys +=1

    # Q14: BMI categories 

    bmi = person.bmi()                         # O(1)
    if bmi is None:
        continue
        
    # Classify BMI into categories
    if(bmi < 18.5):
        people_fat[0] += 1
        if(person.children):
            children_fat[0] += 1
    elif( bmi < 24.99):
        people_fat[1] += 1
        if(person.children):
            children_fat[1] += 1
    elif(bmi < 29.99):
        people_fat[2] += 1
        if(person.children):
            children_fat[2] += 1
    elif( 29.9 < bmi):
        people_fat[3] += 1
        if(person.children):
            children_fat[3] += 1  
    bmi_category_by_cpr[cpr] = bmi_category(person)

    


#####################
### POST-PROCESS ###
####################

# Q2 & Q4: Average parental age at first child
avg_age_father = age_count_father / total_father if total_father else 0
avg_age_mother = age_count_mother / total_mother if total_mother else 0

# Q6: percentage of people without children
percent_women = (woman_without_children / total_female)*100 if total_female else 0
percent_men = (men_without_children / total_male)*100 if total_male else 0

# Q7: age difference between parents  

age_difference = []

for parents in child_to_parents.values():      # O(n)
    if len(parents) >= 2:
        for i in range(len(parents)):
            for j in range(i+1, len(parents)):
                age1 = age_by_cpr[parents[i]]
                age2 = age_by_cpr[parents[j]]
                diff = abs(age1 - age2)
                age_difference.append(diff)

avg_difference = sum(age_difference) / len(age_difference) if age_difference else 0

# Q8 : people with grandparents 

for p in all_people:                             # O(n)
    parents = child_to_parents.get(p, [])
    for parent in parents:                       # O(k)
        if child_to_parents.get(parent):
            people_with_grandparents += 1
            break

percentage_granparents = (people_with_grandparents /total_people) * 100

# Q9 : cousins pairs 

cousins_pair = []

for person in all_people:                          # O(n)
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
# Remove duplicate cousin pairs
cousins_pair = list(set(cousins_pair))

# Number of cousin pairs
number_cousin_pairs = len(cousins_pair)

# People who have at least one cousin
people_with_cousins = set()

for person, cousin in cousins_pair:
    people_with_cousins.add(person)
    people_with_cousins.add(cousin)

number_people_with_cousins = len(people_with_cousins)

# Average number of cousins only among people who have cousins
cousins_per_person = {}

for person, cousin in cousins_pair:
    if person not in cousins_per_person:
        cousins_per_person[person] = set()
    cousins_per_person[person].add(cousin)

avg_cousins = (
    sum(len(cousins) for cousins in cousins_per_person.values()) 
    / len(cousins_per_person)
    if cousins_per_person else 0
)






# Q10 : Child gender percentages
total_children = boys + girls
boys_percentage = (boys / total_children)*100 if total_children else 0
girls_percentage = (girls / total_children)*100 if total_children else 0



# Q11 : Partnet relationships among parents 
person_to_partner = {}

for parents in child_to_parents.values():
    if len(parents) < 2:
        continue

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

men_more_partner = (male_pluspartner / male_total) * 100 if male_total > 0 else 0
women_more_partner = (female_pluspartner / female_total) * 100 if female_total > 0 else 0




# Q12 : Couple heigth 


count_couple_type = dict()

for parents in child_to_parents.values():          # O(n)
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

for child, parents in child_to_parents.items():       # O(n)
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

# Q14

for parents in child_to_parents.values():
    if len(parents) < 2:
        continue

    for i in range(len(parents)):
        for j in range(i + 1, len(parents)):

            b1 = bmi_category_by_cpr.get(parents[i], 'unknown')
            b2 = bmi_category_by_cpr.get(parents[j], 'unknown')

            if b1 == 'unknown' or b2 == 'unknown':
                continue

            couple = tuple(sorted([b1, b2]))
            bmi_couple_type[couple] = bmi_couple_type.get(couple, 0) + 1

total_bmi_couples = sum(bmi_couple_type.values())

# Q15

incompatible_children = []

for child, parents in child_to_parents.items():            # O(n)

    if child not in blood_type_by_cpr:
        continue

    if len(parents) != 2:
        continue

    parent1 = parents[0]
    parent2 = parents[1]

    parent1_blood = blood_type_by_cpr[parent1][:-1]
    parent2_blood = blood_type_by_cpr[parent2][:-1]
    child_blood = blood_type_by_cpr[child][:-1]

    parent1_rh = blood_type_by_cpr[parent1][-1]
    parent2_rh = blood_type_by_cpr[parent2][-1]
    child_rh = blood_type_by_cpr[child][-1]

    possible_blood = possible_child_blood(parent1_blood, parent2_blood)
    possible_rh = possible_child_rh(parent1_rh, parent2_rh)

    if child_blood not in possible_blood or child_rh not in possible_rh:
        incompatible_children.append(child)



# Q16

father_son_donations = []

for son, parents in child_to_parents.items():                   # O(n)

    if son not in blood_type_by_cpr:
        continue

    if gender_by_cpr.get(son) != "M":
        continue

    son_blood = blood_type_by_cpr[son]

    if not son_blood:
        continue

    for parent in parents:                                       # O(k)

        if gender_by_cpr.get(parent) != "M":
            continue

        father_blood = blood_type_by_cpr[parent]

        if not father_blood:
            continue

        possible_receivers = can_donate_blood(father_blood)

        if son_blood in possible_receivers:
            father_son_donations.append(
                (parent, father_blood, son, son_blood)
            )

unique_fathers = set()
unique_sons = set()

for father, father_blood, son, son_blood in father_son_donations:
    unique_fathers.add(father)
    unique_sons.add(son)


# Q17

grandchild_grandparent_donations = []
seen_grandchildren = set()

for person in all_people:                                      # O(n)

    if person in seen_grandchildren:
        continue

    parents = child_to_parents.get(person, [])
    grandparents = set()

    for parent in parents:
        parent_parents = child_to_parents.get(parent, [])

        for grandparent in parent_parents:
            grandparents.add(grandparent)

    if not grandparents:
        continue

    person_blood = blood_type_by_cpr[person]  # e.g. "O-", "A+"
    possible_receivers = can_donate_blood(person_blood)

    for grandparent in grandparents:
        grandparent_blood = blood_type_by_cpr[grandparent]

        if grandparent_blood in possible_receivers:
            grandchild_grandparent_donations.append(
                (person, person_blood, grandparent, grandparent_blood)
            )
            seen_grandchildren.add(person)
            



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

print(f"{'Age':<10} {'Count':<10} {'Male %':<10}")

for age in range(10, 40):
    count = father_counts[age]
    male_percentage = (count / total_father) * 100 if total_father > 0 else 0
    print(f"{age:<10} {count:<10} {male_percentage:<10.2f}")


# Q4
print('\nQ4\n')

print(f"Maximum age of first-time mothers: {max_age_mother:.2f}")
print(f"Minimum age of first-time mothers:{min_age_mother:.2f}")
print(f"Average age of first-time mothers:{avg_age_mother:.2f}")


# Q5 
print('\nQ5\n')
print(f"{'Age':<10} {'Count':<10} {'Female %':<10}")

for age in range(10, 40):
    count = mother_counts[age]
    female_percentage = (count / total_mother) * 100 if total_mother > 0 else 0
    print(f"{age:<10} {count:<10} {female_percentage:<10.2f}")

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
print(f'The number of cousin pairs is {number_cousin_pairs}')
print(f'The number of people that have cousins is {number_people_with_cousins}')
print(f'The average number of cousins per person is {avg_cousins:.2f}')

# Q10
print('\nQ10\n')

print(f"Firstborn likely to be female: {girls_percentage:.2f}%")
print(f"Firstborn likely to be male: {boys_percentage:.2f}%")
   
# Q11
print('\nQ11\n')

print(f"{'':30}{'Men':>10}{'Women':>10}")
print(f"{'Multiple partners (%)':30}{men_more_partner:10.2f}{women_more_partner:10.2f}")
print(f"{'Total people':30}{male_total:10}{female_total:10}")
print(f"{'People with >1 partner':30}{male_pluspartner:10}{female_pluspartner:10}")


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



print("BMI Couple Analysis")
print(f"{'Couple Type':25} {'Percentage':>10}")

expected_bmi_couples = [
    ('fat', 'fat'),
    ('fat', 'normal'),
    ('fat', 'slim'),
    ('normal', 'normal'),
    ('normal', 'slim'),
    ('slim', 'slim')
]

for couple in expected_bmi_couples:

    sorted_couple = tuple(sorted(couple))

    count = bmi_couple_type.get(sorted_couple, 0)

    percentage = (
        (count / total_bmi_couples) * 100
        if total_bmi_couples > 0 else 0
    )

    print(f"{str(couple):25} {percentage:9.2f}%")

# Q15

print('\nQ15\n')

print("Children with incompatible blood type inheritance:")
for child in incompatible_children:
    print(f"{child} ({blood_type_by_cpr[child]})")

print(f"Number of possible non-biological children: {len(incompatible_children)}")

# Q16

print('\nQ16\n')

print("Fathers who can donate blood to their sons:")
for father, father_blood, son, son_blood in father_son_donations:
    print(f"{father} ({father_blood}) -> {son} ({son_blood})")

print(f"Length of the list: {len(father_son_donations)}")
print(f"Number of fathers: {len(unique_fathers)}")
print(f"Number of sons: {len(unique_sons)}")


# Q17

print('\nQ17\n')

print("People who can donate blood to at least one grandparent:")
for grandchild, grandchild_blood, grandparent, grandparent_blood in sorted(grandchild_grandparent_donations):
    print(f"{grandchild} ({grandchild_blood}) -> {grandparent} ({grandparent_blood})")

print(f"Length of the list: {len(grandchild_grandparent_donations)}")
print(f"Number of grandchildren: {len(seen_grandchildren)}")





##################################
####### Overall Complexity ######
#################################

# Worst case: O(n * k^4) 
# Expected case : O(n), assuming bounded family size 

