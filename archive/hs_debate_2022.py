import csv

# Data for 2022 winners
data = [
    {
        'Name': 'Parker De Deker',
        'High School': 'Neenah High School',
        'State': 'WI',
        'Event': 'Congressional Debate – House'
    },
    {
        'Name': 'Alex Zhang',
        'High School': 'Stratford High School',
        'State': 'TX',
        'Event': 'Congressional Debate – Senate'
    },
    {
        'Name': 'Hannah Owens Pierre',
        'High School': 'Edina High School',
        'State': 'MN',
        'Event': 'Lincoln-Douglas Debate'
    },
    {
        'Name': 'Jiyoon Park',
        'High School': 'Washburn Rural High School',
        'State': 'KS',
        'Event': 'Richard B. Sodikow Policy Debate'
    },
    {
        'Name': 'Zach Willingham',
        'High School': 'Washburn Rural High School',
        'State': 'KS',
        'Event': 'Richard B. Sodikow Policy Debate'
    },
    {
        'Name': 'Amanda Frank',
        'High School': 'NSU University School',
        'State': 'FL',
        'Event': 'Public Forum Debate'
    },
    {
        'Name': 'Maria Riofrio',
        'High School': 'NSU University School',
        'State': 'FL',
        'Event': 'Public Forum Debate'
    },
    {
        'Name': 'Katie Babb',
        'High School': 'West Los Angeles Violet',
        'State': 'CA',
        'Event': 'World Schools Debate'
    },
    {
        'Name': 'Nadia Chung',
        'High School': 'West Los Angeles Violet',
        'State': 'CA',
        'Event': 'World Schools Debate'
    },
    {
        'Name': 'Alex Lee',
        'High School': 'West Los Angeles Violet',
        'State': 'CA',
        'Event': 'World Schools Debate'
    },
    {
        'Name': 'Bodhi Silberling',
        'High School': 'West Los Angeles Violet',
        'State': 'CA',
        'Event': 'World Schools Debate'
    },
    {
        'Name': 'Sungjoo Yoon',
        'High School': 'West Los Angeles Violet',
        'State': 'CA',
        'Event': 'World Schools Debate'
    },
    {
        'Name': 'Ethan Boneh',
        'High School': 'Palo Alto High School',
        'State': 'CA',
        'Event': 'Big Questions Debate'
    }
]

# Write to CSV
with open('hs_debate_2022.csv', 'w', newline='') as csvfile:
    fieldnames = ['Name', 'School', 'Year', 'Country']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for participant in data:
        participant['Country'] = 'United States'
        participant['Year'] = 2022
        participant['School'] = participant['High School']
        del participant['High School']
        del participant['Event']
        del participant['State']
        writer.writerow(participant)

print("CSV file has been created successfully!") 