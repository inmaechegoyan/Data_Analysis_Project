#!/usr/bin/env python3


# Define a class for all the CPR

class People: 
    def __init__(self, cpr):
        self.cpr = cpr
        self.first_name = None
        self.last_name = None
        self.height = None
        self.weight = None
        self.eye_color = None
        self.blood_type = None
        self.children = []

        # Derived atributes: 
        self.gender = 'F' if int(cpr[-1]) % 2 == 0 else 'M'
        self.age = 100 - int(cpr[4:6])

    def age_first_child(self):
        if not self.children:
            return None
        
        oldest_child_age = max(100 - int(c[4:6]) for c in self.children)
        return self.age - oldest_child_age

   
