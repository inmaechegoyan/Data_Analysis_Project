#!/usr/bin/env python3


###### Function to extract all the informaiton from each person in the file ######

from data.clean_data_class import People
from src.read_people_info import read_people_info



# All variables: 


##### QUESTION 1 #####



# QUESTION 1: Is the age and gender distribution normal/sensible in the database? A yes/no answer is not good enough.
age_intervals = [(0,10), (10,20), (20,30),(30,40),(40,50),(50,60),(60,70),(70,80),(80,90),(90,100)]

def question_1(): 
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
