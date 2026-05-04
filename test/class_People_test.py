from src.people_class import People
from pytest import approx

# test gender = female by cpr number
def test_gender_female():
    p = People("010180-1234")
    assert p.gender == "F"

# test gender = male by cpr number
def test_gender_male():
    p = People("010180-1235")
    assert p.gender == "M"

# test age by cpr number
def test_age():
    p = People("010180-1234")
    assert p.age == 20

# test age_first_children if she/he has no children
def test_age_first_child_no_children():
    p = People("010170-1235")
    assert p.age_first_child() is None

# test age_first_children 
def test_age_first_child_with_children():
    p = People("0101601235")   # age 40
    p.children = ["0101901234", "0101851235"]  # ages 10 and 15
    assert p.age_first_child() == 25

# test first_child_cpr
def test_first_child_cpr():
    p = People("0101601235")
    p.children = ["0101901234", "0101851235"]
    assert p.first_child_cpr() == "0101851235"

# test calculation of bmi
def test_bmi():
    p = People("0101801234")
    p.height = 170
    p.weight = 70
    assert p.bmi() == approx(24.22, rel=1e-2)

# test calculation of bmi with missing data
def test_bmi_missing_data():
    p = People("010180-1234")
    assert p.bmi() is None