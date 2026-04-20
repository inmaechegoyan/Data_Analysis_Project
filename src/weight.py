#Do fat people marry (or at least get children together)? To answer that, 
#calculate the percentages of fat/fat, fat/normal, fat/slim, normal/normal, 
# normal/slim, and slim/slim couples. 
# Decide your own limits for fat, normal and slim. Calculate the BMI, 
# and let that be the fatness indicator.

# BMI = weight (kg)/(height(m))^2


from data.clean_data_class import People
from src.read_people_info import read_people_info



# 2. At what age does the men become fathers first time (max age, min age, average age)?
fat_intervals = ["Underweight", "Normal weight", "Overweight", "Obese"]
people_fat = [0] * len(fat_intervals)
children_fat = [0] * len(fat_intervals)
people = 0
for person in read_people_info('data/people.db'):
    bmi = person.bmi()
    if bmi is None:
        continue
    people += 1
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


print("Distribution of people according to their weight and bmi")
for i, label in enumerate(fat_intervals):
    fat_percentage = (people_fat[i] / people) * 100 if people > 0 else 0
    print(f"{label}  {fat_percentage:.2f}%  ({people_fat[i]}/{people})") 

print("")
print("Distribution of people having children according to their weight and bmi")
for i, label in enumerate(fat_intervals):
    children_fat_percentage = (children_fat[i] / people_fat[i]) * 100 if people > 0 else 0
    print(f"{label}  {children_fat_percentage:.2f}%  ({children_fat[i]}/{people_fat[i]})") 
