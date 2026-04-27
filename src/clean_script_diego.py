from data.clean_data_class import People
from src.read_people_info import read_people_info
from src.functions_diego import analyze_age_gender_distribution
from src.functions_diego import count_gender_totals

# exercise 1 #
# age and gender distribution

people = list(read_people_info('data/people.db'))
print(people)

total_female, total_male = count_gender_totals(people)

age_intervals = [(0,10), (10,20), (20,30),(30,40),(40,50),(50,60),(60,70),(70,80),(80,90),(90,100)]
female_p, male_p = analyze_age_gender_distribution(people, age_intervals)

####################
### PRINT RESULT ###
####################
print("Age and gender distribution in the dataset: ")
print(f"{'Age Range':<13} {'Female %':<12} {'Male %':<10}")

for i, (low,high) in enumerate(age_intervals):
    female_percentage = female_p[i]
    male_percentage = male_p[i] 
    print(f'{low}-{high:<13} {female_percentage:<9.2f} {male_percentage:<9.2f}')

####################
### PRINT RESULT ###
####################
total_people = total_female + total_male
print("")
print("Gender distribution in the dataset: ")
print("Percentage of males in the dataset: "f'{(total_male/total_people)*100}'"%")
print("Percentage of females in the dataset: "f'{(total_female/total_people)*100}'"%")