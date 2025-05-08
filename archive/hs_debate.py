import requests
import bs4
import pandas as pd

URLS = {
    2015: "https://www.speechanddebate.org/2015-national-champions/",
    2016: "https://www.speechanddebate.org/2016-national-champions/",
    2017: "https://www.speechanddebate.org/2017-national-champions/",
    2018: "https://www.speechanddebate.org/2018-national-champions/",
    2019: "https://www.speechanddebate.org/2019-national-champions/",
    2020: "https://www.speechanddebate.org/2020-national-champions/",
    2021: "https://www.speechanddebate.org/2021-national-champions/",
    2022: "https://www.speechanddebate.org/2022-national-champions/",
    2023: "https://www.speechanddebate.org/2023-national-speech-debate-champions/",
    2024: "https://www.speechanddebate.org/2024-national-speech-debate-champions/"
}

def get_hs_debate_participants(year: int, url: str):

    response = requests.get(url)
        
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    
    # Find the debate events section
    debate_section = soup.find('div', class_='et_pb_section_5')
    if not debate_section:
        return []
    
    participants = []
    
    # Find all text modules containing participant information
    text_modules = debate_section.find_all('div', class_='et_pb_text_inner')
    
    for module in text_modules:
        # Skip the header module
        if module.find('h3', string='Debate Events'):
            continue
            
        # Get the event name
        event_name = module.find('h3')
        if not event_name:
            continue
            
        # Get the participant text
        participant_text = module.find('div')
        if not participant_text:
            continue
            
        # Extract names and schools
        text = participant_text.get_text()
        if 'from' in text:
            name_part = text.split('from')[0].strip()
            school_part = text.split('from')[1].split('Coached by')[0].strip()
            
            # Handle multiple names (for team events)
            # First split by comma, then split each part by 'and'
            names = []
            for part in name_part.split('and '):
                names.extend([n.strip() for n in part.split(',')])
            
            for name in names:
                if name == "":
                    continue
                participants.append({
                    'name': name,
                    'school': school_part,
                    'event': event_name.get_text()
                })
    
    return participants

def get_all_years_data(start_year: int = 2015, end_year: int = 2024) -> pd.DataFrame:
    all_participants = []
    
    for year in range(start_year, end_year + 1):
        print(f"Fetching data for {year}...")
        participants = get_hs_debate_participants(year, URLS[year])
        
        for p in participants:
            all_participants.append({
                'Name': p['name'],
                'School': p['school'],
                'Year': year,
                'Country': 'United States'  # Assuming all participants are from the US
            })
    
    return pd.DataFrame(all_participants)

# Get data for all years and create DataFrame
df = get_all_years_data()

# Save to CSV
df.to_csv('debate_participants_2015_2024.csv', index=False)

# Display the first few rows
print("\nFirst few rows of the DataFrame:")
print(df.head())