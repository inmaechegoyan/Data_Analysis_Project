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

#age_intervals = [(15, 19), (20, 24), (25, 29), (30, 34), (35, 39), (40, 99)]    # PODRIAMOS USAR EL MISMO QUE EN EL 1??? 

##### QUESTION 4 #####

total_mother = 0
max_age_mother = 0
min_age_mother = 99
age_count_mother = 0

##### QUESTION 5 #####.     TODAS ESTAN INCLUIDAS EN OTRAS ACT (LO QUE NO SE ES SI HABRA QUE RESTART ALGUNAS VARIABLES DURANTE EL CODE)

##### QUESTION 6 #####

woman_without_children = 0
men_without_children = 0


for person in read_people_info('data/people.db'):   # THIS CAN ONLY APPEAR ONE IN THE SCRIPT!!!!!!!

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
            max_age = age_first_child
        if age_first_child < min_age_father:
            min_age_father = age_first_child

    # Q3
    if person.gender == "M":
        age = person.age_first_child()
        if age is not None:
            total_father += 1

            for i, (low, high) in enumerate(age_intervals):
                if low <= age <= high:
                    male_counts[i] += 1
                    break
            
    # Q4
    age_first_child = person.age_first_child()
    if person.gender == "F" and age_first_child is not None:
        age_count_mother += age_first_child
        total_mother += 1
        if age_first_child > max_age_mother:
            max_age_mother = age_first_child
        if age_first_child < min_age_mother:
            min_age_mother = age_first_child
    

    # # Q5 y Q6
    # if person.gender == "F":
    #     total_female += 1
    #     age = person.age_first_child()
    #     if age is not None:
    #         total_mother += 1

    #         for i, (low, high) in enumerate(age_intervals):
    #             if low <= age <= high:
    #                 female_counts[i] += 1
    #                 break
    #     if person.children == []:
    #         woman_without_children += 1
    # else: 
    #     total_male += 1
    #     if person.children == []:
    #         men_without_children += 1

    # Q5
    if person.gender == "F":
        age = person.age_first_child()
        if age is not None:
            # total_mother += 1

            for i, (low, high) in enumerate(age_intervals):
                if low <= age <= high:
                    # female_counts[i] += 1
                    break







##### CALCULATIONS AT THE END OF THE LOOP #### 

# Q2
avg_age_father = age_count_father / total_father

# Q4
avg_age_mother = age_count_mother / total_mother

# Q6 
percent_women = (woman_without_children / total_female) * 100
percent_men = (men_without_children / total_male) * 100







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
    male_percentage = (male_counts[i] / total_father) * 100 if total_father > 0 else 0
    print(f"{low}-{high:<8} {male_percentage:<10.2f}") 


# Q4

print(f"Maximum age of first-time mothers: {max_age_mother:.2f}")
print(f"Minimum age of first-time mothers:{min_age_mother:.2f}")
print(f"Average age of first-time mothers:{avg_age_mother:.2f}")


# Q5 
print(f"{'Age range':<10} {'Female %':<10}")

for i, (low, high) in enumerate(age_intervals):
    female_percentage = (female_counts[i] / total_mother) * 100 if total_mother > 0 else 0
    print(f"{low}-{high:<8} {female_percentage:<10.2f}") 

# Q6
print(f"Women without children: {percent_women:.2f}%")
print(f"Men without children: {percent_men:.2f}%")
