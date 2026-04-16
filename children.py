from clean_data_class import People
from read_people_info import read_people_info

# 5. Is the distribution of first-time motherhood age normal/sensible? A yes/no answer is not good enough.
parent = 0
for person in read_people_info('people.db'):
    if(person.children):
        parent += 1
        print(person.cpr)

print(parent)

    
  
    

