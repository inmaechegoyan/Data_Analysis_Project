from Data_Analysis_Project.src.people_class import People
from Data_Analysis_Project.src.functions import read_people_info

def load_data(filename):
    people_by_cpr = {}
    child_to_parents = {}
    parent_to_children = {}

    for person in read_people_info(filename):
        people_by_cpr[person.cpr] = person
        parent_to_children[person.cpr] = person.children

        for child_cpr in person.children:
            if child_cpr not in child_to_parents:
                child_to_parents[child_cpr] = []

            child_to_parents[child_cpr].append(person)
    
    return people_by_cpr, child_to_parents, parent_to_children

load_data('data/people.db')