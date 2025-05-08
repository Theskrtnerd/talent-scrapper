import csv

# Data for 2021 winners
data = [
    {
        'Name': 'Alexandra Smith',
        'High School': 'East Ridge High School',
        'State': 'MN',
        'Event': 'Congressional Debate – House'
    },
    {
        'Name': 'Atharv Kulkarni',
        'High School': 'Jasper High School',
        'State': 'TX',
        'Event': 'Congressional Debate – Senate'
    },
    {
        'Name': 'Katie Jack',
        'High School': 'George Washington High School',
        'State': 'CO',
        'Event': 'Lincoln-Douglas Debate'
    },
    {
        'Name': 'Adarsh Hiremath',
        'High School': 'Bellarmine College Preparatory',
        'State': 'CA',
        'Event': 'Richard B. Sodikow Policy Debate'
    },
    {
        'Name': 'Surya Midha',
        'High School': 'Bellarmine College Preparatory',
        'State': 'CA',
        'Event': 'Richard B. Sodikow Policy Debate'
    },
    {
        'Name': 'Carina Guo',
        'High School': 'Richard Montgomery High School',
        'State': 'MD',
        'Event': 'Public Forum Debate'
    },
    {
        'Name': 'Jennifer Lin',
        'High School': 'Richard Montgomery High School',
        'State': 'MD',
        'Event': 'Public Forum Debate'
    },
    {
        'Name': 'Diego Castillo',
        'High School': 'Alief Elsik High School',
        'State': 'TX',
        'Event': 'World Schools Debate'
    },
    {
        'Name': 'Ebenezer Appiah',
        'High School': 'Alief Elsik High School',
        'State': 'TX',
        'Event': 'World Schools Debate'
    },
    {
        'Name': 'Rodrigo Trujillo',
        'High School': 'Alief Elsik High School',
        'State': 'TX',
        'Event': 'World Schools Debate'
    },
    {
        'Name': 'Anthony Hoang',
        'High School': 'Alief Elsik High School',
        'State': 'TX',
        'Event': 'World Schools Debate'
    },
    {
        'Name': 'Oam Patel',
        'High School': 'Mountain Home High School',
        'State': 'ID',
        'Event': 'Big Questions Debate'
    }
]

# Write to CSV
with open('hs_debate_2021.csv', 'w', newline='') as csvfile:
    fieldnames = ['Name', 'School', 'Year', 'Country']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for participant in data:
        participant['Country'] = 'United States'
        participant['Year'] = 2021
        participant['School'] = participant['High School']
        del participant['High School']
        del participant['Event']
        del participant['State']
        writer.writerow(participant)

print("CSV file has been created successfully!") 