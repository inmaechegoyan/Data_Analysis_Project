from clean_data_class import People
from read_people_info import read_people_info

# 2. At what age does the men become fathers first time (max age, min age, average age)?
max_age = 0
min_age = 99
age_count = 0 
total_father = 0
for person in read_people_info('people.db'):
    age_first_child = person.age_first_child()
    if person.gender == "M" and age_first_child is not None:
        age_count += age_first_child
        total_father += 1
        if age_first_child > max_age:
            max_age = age_first_child
        if age_first_child < min_age:
            min_age = age_first_child
avg_age = age_count / total_father

print(f"Maximum age of first-time fathers: {max_age:.2f}")
print(f"Minimum age of first-time fathers:{min_age:.2f}")
print(f"Average age of first-time fathers::{avg_age:.2f}")

# 3. Is the distribution of first-time fatherhood age normal/sensible? A yes/no answer is not good enough.
age_intervals = [(15, 19), (20, 24), (25, 29), (30, 34), (35, 39), (40, 99)]
male_counts = [0] * len(age_intervals)
total_father = 0
for person in read_people_info('people.db'):
    if person.gender == "M":
        age = person.age_first_child()
        if age is not None:
            total_father += 1

            for i, (low, high) in enumerate(age_intervals):
                if low <= age <= high:
                    male_counts[i] += 1
                    break
print(f"{'Age range':<10} {'Male %':<10}")

for i, (low, high) in enumerate(age_intervals):
    male_percentage = (male_counts[i] / total_father) * 100 if total_father > 0 else 0
    print(f"{low}-{high:<8} {male_percentage:<10.2f}") 

# 4. At what age does the women become mothers first time (max age, min age, average age)?
max_age = 0
min_age = 99
age_count = 0 
total_mother = 0
for person in read_people_info('people.db'):
    age_first_child = person.age_first_child()
    if person.gender == "F" and age_first_child is not None:
        age_count += age_first_child
        total_mother += 1
        if age_first_child > max_age:
            max_age = age_first_child
        if age_first_child < min_age:
            min_age = age_first_child
avg_age = age_count / total_mother

print(f"Maximum age of first-time mothers: {max_age:.2f}")
print(f"Minimum age of first-time mothers:{min_age:.2f}")
print(f"Average age of first-time mothers:{avg_age:.2f}")

      

# 5. Is the distribution of first-time motherhood age normal/sensible? A yes/no answer is not good enough.
age_intervals = [(15, 19), (20, 24), (25, 29), (30, 34), (35, 39), (40, 99)]
female_counts = [0] * len(age_intervals)
total_mother = 0
for person in read_people_info('people.db'):
    if person.gender == "F":
        age = person.age_first_child()
        if age is not None:
            total_mother += 1

            for i, (low, high) in enumerate(age_intervals):
                if low <= age <= high:
                    female_counts[i] += 1
                    break
print(f"{'Age range':<10} {'Female %':<10}")

for i, (low, high) in enumerate(age_intervals):
    female_percentage = (female_counts[i] / total_mother) * 100 if total_mother > 0 else 0
    print(f"{low}-{high:<8} {female_percentage:<10.2f}") 

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





        




    
  
    

