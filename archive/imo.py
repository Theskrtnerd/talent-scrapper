import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

COUNTRIES = ["United States", "Australia", "Canada", "United Kingdom", "New Zealand"]

def get_imo_results(year):
    # URL for the IMO results page
    url = f"https://www.imo-official.org/year_individual_r.aspx?year={year}"
    
    # Add headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Make the request with a delay to be respectful
        time.sleep(1)  # Add a 1-second delay between requests
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the results table
        table = soup.find('table')
        
        # Initialize lists to store data
        participants = []
        countries = []
        years = []
        
        # Define allowed countries
        
        # Extract data from each row
        for row in table.find_all('tr')[1:]:  # Skip header row
            cols = row.find_all('td')
            if len(cols) >= 2:  # Ensure row has enough columns
                # Extract participant name
                participant = cols[0].find('a').text.strip()
                # Extract country
                country_cell = cols[1].find('a')
                country = country_cell.text.strip()
                
                # Only add if any of the COUNTRIES are in the country cell text
                if any(country in country_cell.get_text() for country in COUNTRIES):
                    participants.append(participant.strip())
                    countries.append(country.strip())
                    years.append(year)
        
        # Create DataFrame
        df = pd.DataFrame({
            'Name': participants,
            'Country': countries,
            'Year': years
        })
        
        return df
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for year {year}: {e}")
        return None

def main():
    # Initialize an empty DataFrame to store all results
    all_results = pd.DataFrame(columns=['Name', 'Country', 'Year'])
    
    # Loop through years 2015 to 2024
    for year in range(2015, 2025):
        print(f"Fetching data for year {year}...")
        df = get_imo_results(year)
        
        if df is not None:
            all_results = pd.concat([all_results, df], ignore_index=True)
    
    # Keep the row with the biggest year for each participant-country combination
    unique_results = all_results.sort_values('Year', ascending=False).drop_duplicates(subset=['Name', 'Country'])
    
    # Save to CSV
    unique_results.to_csv('imo_participants_2015_2024.csv', index=False)

if __name__ == "__main__":
    main()
