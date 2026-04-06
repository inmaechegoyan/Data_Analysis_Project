#!/usr/bin/env python3


import pandas as pd


filename = 'people.db'

def extract_info_file(filename): 
    people = dict()
    current_cpr = None

    try: 
        with open(filename, 'r') as infile: 
            for line in infile: 
                line = line.strip()

                if not line: 
                    continue

                # Detect CPR
                if line.upper().startswith('CPR'): 
                    current_cpr = line.split(':', 1)[1].strip()
                    people[current_cpr] = {}
                    continue
                # Parse key-value lines
                if ': ' in line and current_cpr is not None: 
                    key, value = line.split(': ', 1)
                    key_lower = key.lower()

                    # Normalize keys and types
                    if key_lower == 'first name': 
                        people[current_cpr]['first_name'] = value 
                    elif key_lower == 'last name':
                        people[current_cpr]['last_name'] = value 
                    elif key_lower == 'height':
                        people[current_cpr]['height'] = int(value) 
                    elif key_lower == 'weight':
                        people[current_cpr]['weight'] = int(value) 
                    elif key_lower == 'eye color':
                        people[current_cpr]['eye color'] = value 
                    elif key_lower == 'blood type':
                        people[current_cpr]['blood_type'] = value 
                    elif key_lower == 'children':
                        people[current_cpr]['children'] = value.split()
         
            print(people)
            return people

    except IOError as error: 
        print(f'Cannot open file.Reason: {error}')
        

                    
people_dict = extract_info_file(filename)    



df = pd.DataFrame.from_dict(people_dict, orient='index')
df.index.name = 'CPR'

print(df)

df.to_csv('people_clean.csv')

