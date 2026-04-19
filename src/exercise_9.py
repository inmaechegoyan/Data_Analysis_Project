#!/usr/bin/env python3

# Exercise 9: How many has at least one cousin in the data set? What is the average number of cousins based on those who have cousins?
# Note: This number is historically difficult to compute right, but here are some thoughts to help you out in verifying your count.
# You have to construct a method for finding cousin pairs. Any cousin pair you identify, can be written as a tuple (cpr1, cpr2) in a list.
# a) There should be no duplicate tuples in the list - you are not cousins with the same person more than once.
# b) There should be no tuple with the same cpr on position 1 and 2 - you are not cousins with yourself.
# c) Because of symmetry, it is expected that for any (cpr1, cpr2) tuple there is a (cpr2, cpr1) tuple - when you are cousins with somebody, 
# somebody is cousins with you. This has natural consequences: Set(cpr1) == Set(cpr2), Sorted_list(cpr1) == Sorted_list(cpr2).
# d) This list does NOT discover sibling pairs inserted as cousins, however there should be no overlap of this list and a similar list covering sibling pairs.
# e) The length of the list of cousin tuples is the num


# Import the class and function 

from data.clean_data_class import People
from src.read_people_info import read_people_info

