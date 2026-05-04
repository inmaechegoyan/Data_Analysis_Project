#!/usr/bin/env python3

# Import the class and function 

from Data_Analysis_Project.src.people_class import People
from Data_Analysis_Project.src.functions import read_people_info




# QUESTION 1: Is the age and gender distribution normal/sensible in the database? A yes/no answer is not good enough.
age_intervals = [(0,10), (10,20), (20,30),(30,40),(40,50),(50,60),(60,70),(70,80),(80,90),(90,100)]

# Create the counts
female_counts = [0] * len(age_intervals)
male_counts = [0] * len(age_intervals)

total_female = 0 
total_male = 0 

# Call the function to extract the age and the gender 
for person in read_people_info('data/people.db'):
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


####################
### PRINT RESULT ###
####################
print(f"{'Age Range':<10} {'Female %':<10} {'Male %':<10}")

for i, (low,high) in enumerate(age_intervals):
    female_porcentage = ((female_counts[i]/total_female) * 100) if total_female > 0 else 0
    male_porcentage = (((male_counts[i]/total_male) * 100)) if total_male > 0 else 0 
    print(f'{low}-{high:<8} {female_porcentage:<10.2f} {male_porcentage:10.2f}')



