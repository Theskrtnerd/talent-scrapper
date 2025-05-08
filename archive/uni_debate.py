import csv

# Data organized as [year, [teams]]
data = {
    2025: [
        ("Tejas Subramaniam & Elizabeth Li", "Stanford University"),
        ("Manav Mittal & Manuel Machorro", "Bates College"),
        ("Ambika Grover & Stephanie Chen", "Harvard University"),
        ("Molly Callaghan & Catherine Liu", "Harvard University")
    ],
    2023: [
        ("Jacquelynn Lin & Xiao-ke Lu", "Princeton University"),
        ("Matt Mauriello & Annushka Agarwal", "Harvard University"),
        ("Muzamil Godil & Justin Wu", "Johns Hopkins University"),
        ("Kaustubh Jain & Sheryar Ahmad", "Princeton University")
    ],
    2022: [
        ("Arthur Lee & Tejas Subramaniam", "Stanford University"),
        ("Jane Mentzinger & Greg Weaving", "Princeton University"),
        ("Matt Song & Michael Ning", "Yale University"),
        ("Rohan Kapoor & Benny Nicholson", "University of Chicago")
    ],
    2020: [
        ("Xiao-ke Lu & Greg Weaving", "Princeton University"),
        ("Jay Gibbs & Jaewan Park", "University of Chicago"),
        ("Devesh Kodnani & Brian Li", "University of Chicago"),
        ("Preston Johnston & Shreyas Kumar", "Princeton University")
    ],
    2019: [
        ("Jenny Jiao & Salil Mitra", "Duke University"),
        ("Aditya Dhar & Michel Nehme", "Harvard University"),
        ("Ko Lyn Cheang & Lorenzo Pinasco", "Yale University"),
        ("Harry Meadows & Abby Westberry", "Bates College")
    ],
    2018: [
        ("Vedant Bahl & Mars He", "Harvard University"),
        ("Benjamin Muschol & Will Smith", "Northeastern University"),
        ("Harry Elliott & Bobbi Leet", "Stanford University"),
        ("William Arnesen & Charlie Barton", "Yale University")
    ],
    2017: [
        ("Archie Hall & Alex Wu", "Harvard University"),
        ("David Slater & Elana Leone", "Stanford University"),
        ("Harry Elliot & Bobbi Leet", "Stanford University"),
        ("Daniel Stoyell & Rebecca Blair", "Cornell University")
    ],
    2016: [
        ("Drew Latimer & Jeremy Chen", "Tufts University"),
        ("Dhruva Bhat & Danny DeBois", "Harvard University"),
        ("Evan Lynyak & Henry Zhang", "Yale University"),
        ("Harry Elliott & Taahir Munshi", "Stanford University")
    ],
    2015: [
        ("Tony Nguyen & Edwin Zhang", "Harvard University"),
        ("David Slater & Elana Leone", "Stanford University"),
        ("Harry Elliott & Taahir Munshi", "Stanford University"),
        ("Daniel Stoyell & Rebecca Blair", "Cornell University")
    ]
}

# Write to CSV
with open('usudc_results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Country', 'Year', 'University'])
    
    for year, teams in data.items():
        for names, university in teams:
            names = names.split(' & ')
            writer.writerow([names[0], 'United States', year, university])
            writer.writerow([names[1], 'United States', year, university])

print("CSV file has been created successfully!")