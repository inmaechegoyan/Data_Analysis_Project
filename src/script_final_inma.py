#!/usr/bin/env python3

# Import the class and function 

from data.clean_data_class import People
from src.read_people_info import read_people_info


#### VARIABLES FOR ALL THE QUESTION ####

##### QUESTION 1 #####

# Create the intervals 
age_intervals = [(0,10), (10,20), (20,30),(30,40),(40,50),(50,60),(60,70),(70,80),(80,90),(90,100)]
# Create the counts
female_counts = [0] * len(age_intervals)
male_counts = [0] * len(age_intervals)

total_female = 0 
total_male = 0 

##### QUESTION 2 #####

max_age_father = 0
min_age_father = 99
age_count_father = 0 
total_father = 0


##### QUESTION 3 #####

father_counts = [0] * len(age_intervals)

##### QUESTION 4 #####

total_mother = 0
max_age_mother = 0
min_age_mother = 99
age_count_mother = 0

##### QUESTION 5 #####.     TODAS ESTAN INCLUIDAS EN OTRAS ACT (LO QUE NO SE ES SI HABRA QUE RESTART ALGUNAS VARIABLES DURANTE EL CODE)

mother_counts = [0] * len(age_intervals)

##### QUESTION 6 #####

woman_without_children = 0
men_without_children = 0

##### QUESTION 7 #####
child_to_parents = dict()
age_difference = []

##### QUESTION 8 #####
people_with_grandparents = 0
total_people = 0



##### QUESTION 10 #####
boys = 0
girls = 0


##### QUESTION 14 #####
fat_intervals = ["Underweight", "Normal weight", "Overweight", "Obese"]
people_fat = [0] * len(fat_intervals)
children_fat = [0] * len(fat_intervals)



for person in read_people_info('data/people.db'):   # THIS CAN ONLY APPEAR ONE IN THE SCRIPT!!!!!!!
    person_cpr = person.cpr
    # Q1
    person_age = person.age
    person_gender = person.gender
    for i, (low,high) in enumerate(age_intervals): 
        if low <= person_age < high: 
            if person_gender == 'F': 
                total_female += 1
                female_counts[i] += 1
            elif person_gender == 'M':
                total_male += 1
                male_counts[i] += 1
            break
    

    # Q2
    age_first_child = person.age_first_child()
    if person.gender == "M" and age_first_child is not None:
        age_count_father += age_first_child
        total_father += 1
        if age_first_child > max_age_father:
            max_age_father = age_first_child
        if age_first_child < min_age_father:
            min_age_father = age_first_child

    # Q3
    if person.gender == "M":
        age = person.age_first_child()
        if age is not None:
            for i, (low, high) in enumerate(age_intervals):
                if low <= age <= high:
                    father_counts[i] += 1
                    break
            
    # Q4
    if person.gender == "F" and age_first_child is not None:
        age_count_mother += age_first_child
        total_mother += 1
        if age_first_child > max_age_mother:
            max_age_mother = age_first_child
        if age_first_child < min_age_mother:
            min_age_mother = age_first_child
    

    # Q5 y Q6
    if person.gender == "F":
        age = person.age_first_child()
        if age is not None:

            for i, (low, high) in enumerate(age_intervals):
                if low <= age <= high:
                    mother_counts[i] += 1
                    break
        if person.children == []:
            woman_without_children += 1
    else: 
        if person.children == []:
            men_without_children += 1


    # Create dict child_to_parents
    for child in person.children: 
        if child not in child_to_parents: 
            child_to_parents[child] = []
        child_to_parents[child].append(person)


    # Q8
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


    





##### CALCULATIONS AT THE END OF THE LOOP #### 

# Q2
avg_age_father = age_count_father / total_father

# # Q4
avg_age_mother = age_count_mother / total_mother

# Q6 
percent_women = (woman_without_children / total_female) * 100
percent_men = (men_without_children / total_male) * 100

# Q7 
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

# Q8
percentage_grandparents = (people_with_grandparents/total_people) * 100

# Q10
total_children = boys + girls







###### PRINT OF RESULTS ######

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
print(f'The number of people that has at least one grandparent is {people_with_grandparents} which correspnd to the {percentage_grandparents:.2f}% of the people in the database')

# Q10
boys_percentage = (boys / total_children) *100
girls_percentage =(girls / total_children) *100
print(f"Firstborn likely to be female: {girls_percentage:.2f}%")
print(f"Firstborn likely to be male: {boys_percentage:.2f}%")

# Q14
print("Distribution of people according to their weight and bmi")
for i, label in enumerate(fat_intervals):
    fat_percentage = (people_fat[i] / total_people) * 100 if total_people > 0 else 0
    print(f"{label}  {fat_percentage:.2f}%  ({people_fat[i]}/{total_people})") 

print("")
print("Distribution of people having children according to their weight and bmi")
for i, label in enumerate(fat_intervals):
    children_fat_percentage = (children_fat[i] / people_fat[i]) * 100 if total_people > 0 else 0
    print(f"{label}  {children_fat_percentage:.2f}%  ({children_fat[i]}/{people_fat[i]})") 