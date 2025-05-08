from bs4 import BeautifulSoup
import requests
import csv
import time
import pandas as pd

# def get_icpc_standings(year: int):
#     url = f"https://cphof.org/standings/icpc/{year}"
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an exception for bad status codes
        
#         return response.text
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching the webpage: {e}")


# def get_us_participants(year: int):
#     # Assuming the HTML content is stored in a variable called 'html_content'
#     soup = BeautifulSoup(get_icpc_standings(year), 'html.parser')

#     # Find all table rows
#     rows = soup.find_all('tr')

#     us_participants = []

#     for row in rows:
#         # Find country cell
#         country_cell = row.find('td', {'style': 'width:10rem'})
#         if country_cell:
#             # Check if the country is United States
#             if 'United States' in country_cell.get_text():
#                 # Find the team members cell
#                 team_cell = row.find_all('td')[2]
#                 # Get the university name (it's the text before the first <br> tag)
#                 university = team_cell.get_text().split('\n')[0].strip()
#                 # Extract all participant names
#                 participants = row.find_all('a', href=lambda x: x and '/profile/' in x)
#                 for participant in participants:
#                     us_participants.append({
#                         'name': participant.get_text().strip(),
#                         'university': university
#                     })

#     # Print unique participant names with their universities
#     print("Participants from United States:")
#     for participant in sorted(set(p['name'] for p in us_participants)):
#         # Find all universities for this participant
#         universities = [p['university'] for p in us_participants if p['name'] == participant]
#         print(f"{participant} ({', '.join(sorted(set(universities)))})")

#     # Save to CSV file
#     with open(f'icpc-{year}.csv', 'w', newline='') as csvfile:
#         fieldnames = ['name', 'university']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
#         writer.writeheader()
#         for participant in us_participants:
#             writer.writerow(participant)

#     print(f"\nData has been saved to icpc-{year}.csv")


# for year in range(2015, 2025):
#     get_us_participants(year)

COUNTRIES = ["United States", "Australia", "Canada", "United Kingdom", "New Zealand"]


def get_icpc_participants(year: int):
    url = f"https://cphof.org/standings/icpc/{year}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        time.sleep(1)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all table rows
        rows = soup.find_all('tr')
        us_participants = []
        
        for row in rows:
            # Find country cell
            country_cell = row.find('td', {'style': 'width:10rem'})
            if country_cell and any(country in country_cell.get_text() for country in COUNTRIES):
                # Find the team members cell
                team_cell = row.find_all('td')[2]
                # Get the university name (text before first <br> tag)
                university = team_cell.get_text().split('\n')[0].strip()
                
                # Extract all participant names
                participants = row.find_all('a', href=lambda x: x and '/profile/' in x)
                for participant in participants:
                    us_participants.append({
                        'Name': participant.get_text().strip(),
                        'Country': country_cell.get_text().strip(),
                        'University': university,
                        'Year': year
                    })
        
        df = pd.DataFrame(us_participants)
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for year {year}: {e}")
        return None

def main():
    all_participants = pd.DataFrame(columns=['Name', 'University', 'Year'])
    for year in range(2015, 2025):
        print(f"Fetching data for year {year}...")
        df = get_icpc_participants(year)
        if df is not None:
            all_participants = pd.concat([all_participants, df], ignore_index=True)

    unique_participants = all_participants.sort_values('Year', ascending=False).drop_duplicates(subset=['Name', 'University'])
    
    unique_participants.to_csv('icpc_participants_2015_2024.csv', index=False)
    

main()