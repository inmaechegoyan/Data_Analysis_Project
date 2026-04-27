from data.clean_data_class import People
from src.read_people_info import read_people_info

def count_gender_totals(people):
    total_female = 0
    total_male = 0

    for person in people:
        if person.gender == 'F':
            total_female += 1
        elif person.gender == 'M':
            total_male += 1

    return total_female, total_male

def analyze_age_gender_distribution(people, age_intervals):
    female_counts = [0] * len(age_intervals)
    male_counts = [0] * len(age_intervals)

    total_female = 0
    total_male = 0

    for person in people:
        age = person.age
        gender = person.gender

        for i, (low, high) in enumerate(age_intervals):
            if low <= age < high:
                if gender == 'F':
                    total_female += 1
                    female_counts[i] += 1
                elif gender == 'M':
                    total_male += 1
                    male_counts[i] += 1
                break

    female_percentages = [
        (female_counts[i]/total_female)*100 if total_female > 0 else 0
        for i in range(len(age_intervals))
    ]

    male_percentages = [
        (male_counts[i]/total_male)*100 if total_male > 0 else 0
        for i in range(len(age_intervals))
    ]

    return female_percentages, male_percentages