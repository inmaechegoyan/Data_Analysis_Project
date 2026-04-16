from clean_data_class import People
from read_people_info import read_people_info

# 5. Is the distribution of first-time motherhood age normal/sensible? A yes/no answer is not good enough.

for person in read_people_info('people.db'):
    if(person.children) and person.gender == "F": # if the person is mother
        oldest_child_age = 0
        for element in person.children:
            child_age = 100 - int(element[4:6])
            if(child_age > oldest_child_age):
                oldest_child_age = child_age
        age_first_motherhood = person.age - oldest_child_age
        print(age_first_motherhood)
    
# 6. How many men and women do not have children (in percent)? 
woman_without_children = 0
men_without_children = 0

total_women = 0
total_men = 0
for person in read_people_info('people.db'):
    if person.gender == "F":
        total_women += 1
        if person.children == []:
            woman_without_children += 1
    else:
        total_men += 1
        if person.children == []:
            men_without_children += 1

# calculate percentages
percent_women = (woman_without_children / total_women) * 100
percent_men = (men_without_children / total_men) * 100

print(f"Women without children: {percent_women:.2f}%")
print(f"Men without children: {percent_men:.2f}%")





        




    
  
    

