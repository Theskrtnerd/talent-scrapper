import csv

# Data for 2020 winners
data = [
    {
        'Name': 'Rachel Eizner',
        'School': 'Monte Vista',
        'Year': 2020,
        'Country': 'United States'
    },
    {
        'Name': 'Manu Onteeru',
        'School': 'Thomas Jefferson HSST',
        'Year': 2020,
        'Country': 'United States'
    },
    {
        'Name': 'Jo Spurgeon',
        'School': 'St Mary\'s',
        'Year': 2020,
        'Country': 'United States'
    },
    {
        'Name': 'Saif-Ullah Salim',
        'School': 'Heritage Hall School',
        'Year': 2020,
        'Country': 'United States'
    },
    {
        'Name': 'Sam Ring',
        'School': 'Heritage Hall School',
        'Year': 2020,
        'Country': 'United States'
    },
    {
        'Name': 'Sasha Haines',
        'School': 'Chagrin Falls High School',
        'Year': 2020,
        'Country': 'United States'
    },
    {
        'Name': 'Magge Mills',
        'School': 'Chagrin Falls High School',
        'Year': 2020,
        'Country': 'United States'
    },
    {
        'Name': 'Caroline Greenstone',
        'School': 'Team Lone Star Green',
        'Year': 2020,
        'Country': 'United States'
    },
    {
        'Name': 'Jothi Gupta',
        'School': 'Team Lone Star Green',
        'Year': 2020,
        'Country': 'United States'
    },
    {
        'Name': 'Cameron Kettles',
        'School': 'Team Lone Star Green',
        'Year': 2020,
        'Country': 'United States'
    },
    {
        'Name': 'Ashley Shan',
        'School': 'Team Lone Star Green',
        'Year': 2020,
        'Country': 'United States'
    },
    {
        'Name': 'Aimee Stachowiak',
        'School': 'Team Lone Star Green',
        'Year': 2020,
        'Country': 'United States'
    },
    {
        'Name': 'Michelle Ma',
        'School': 'Plano West Sr. High School',
        'Year': 2020,
        'Country': 'United States'
    }
]

# Write to CSV
with open('hs_debate_2020.csv', 'w', newline='') as csvfile:
    fieldnames = ['Name', 'School', 'Year', 'Country']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for participant in data:
        writer.writerow(participant)

print("CSV file has been created successfully!") 