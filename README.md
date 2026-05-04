# Data_Analysis_Project

# Overview

This project performs a complete analysis of a population dataset stores in a database ('people.db'). In processes demographic, family realtionship, and blood compatibility data to generate statistical insights. 

The analysis is performed in a sinfle pass over the dataset to ensure efficiency and scalability 


# Project Structure
Data_Analysis_Project
│
├── data/
│ └── people.db # Database containing all people information
│
├── src/
│ ├── functions.py # Core analysis functions
│ ├── main.py # Main script (entry point)
│ ├── people_class.py # People class definition
│
├── test/
│ ├── class_People_test.py
│ ├── functions_test.py
|
│── test_data/
│ ├── test_people.db
|
├── README.md
└── pyproject.toml


# Requirements
 
Python 3.11 or higher 

No external libraries are required 


# How to run 
python -m src.main

# Authors 

Inmaculada Ehegoyan Venegas
Diego Medina Castelló