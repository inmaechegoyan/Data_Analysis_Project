from data.clean_data_class import People
from src.read_people_info import read_people_info
from src.read_people_info import height_category
from src.read_people_info import possible_child_blood
from src.read_people_info import possible_child_rh
from src.read_people_info import can_donate_blood

################################################
####### TESTING READ_PEOPLE_INFO FUNCTION ######
################################################

# test read_people_info with two people
def test_read_people_info():
    people = list(read_people_info("test_data/test_people.db"))


    assert people[0].cpr == "020464-1734"
    assert people[0].first_name == "Elsebeth"
    assert people[0].last_name == "Nielsen"
    assert people[0].height == 171
    assert people[0].children == []
    assert people[0].weight == 62
    assert people[0].eye_color == "Green"
    assert people[0].blood_type == "O-"


    assert people[1].cpr == "230226-9781"
    assert people[1].first_name == "Anton"
    assert people[1].last_name == "Gade"
    assert people[1].height == 201
    assert people[1].children == ["081154-2786", "120853-1151", "050354-4664"]
    assert people[1].weight == 65
    assert people[1].eye_color == "Black"
    assert people[1].blood_type == "A+"

################################################
####### TESTING HEIGHT_CATEGORY FUNCTION #######
################################################

# test tall height category
def test_height_category_male_tall():
    p = People("010180-1235")
    p.height = 188
    assert height_category(p) == "tall"

# test normal height category
def test_height_category_male_normal():
    p = People("010180-1235")
    p.height = 173
    assert height_category(p) == "normal"

# test short height category
def test_height_category_female_short():
    p = People("010180-1234")
    p.height = 159
    assert height_category(p) == "short"



################################################
####### TESTING BLOOD FUNCTIONS ################
################################################

# test possible child blood with parents' blood A, O. 
def test_possible_child_blood_A_O():
    assert possible_child_blood("A", "O") == {"A", "O"}

# test possible child blood with parents' blood AB, O. 
def test_possible_child_blood_AB_O():
    assert possible_child_blood("AB", "O") == {"A", "B"}

# test possible child blood with parents' blood rh -, rh -. 
def test_possible_child_rh_negative_negative():
    assert possible_child_rh("-", "-") == {"-"}

# test who can donate if their blood type is O-.
def test_can_donate_O_negative():
    assert can_donate_blood("O-") == {"O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"}

# test who can donate if their blood type is AB+.
def test_can_donate_AB_positive():
    assert can_donate_blood("AB+") == {"AB+"}
