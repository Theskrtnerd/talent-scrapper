import pandas as pd
from bs4 import BeautifulSoup
import requests

COUNTRIES = ["United States", "Australia", "Canada", "United Kingdom", "New Zealand"]

def get_ioi_results(year):
    # Construct URL
    url = f"https://stats.ioinformatics.org/results/{year}"
    
    # Get HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the results table
    table = soup.find('table')
    
    # Initialize lists to store data
    names = []
    countries = []
    years = []
    
    # Iterate through table rows
    for row in table.find_all('tr')[1:]:  # Skip header row
        cols = row.find_all('td')
        if len(cols) >= 3:  # Ensure row has enough columns
            # Get name and country
            name = cols[1].text.strip()
            country = cols[2].text.strip()
            
            # Skip empty rows or special cases
            if name and country and name != '–' and any(country in my_country for my_country in COUNTRIES):
                names.append(name.strip())
                countries.append(country.strip())
                years.append(year)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Name': names,
        'Country': countries,
        'Year': years
    })
    
    return df

def main():
    # Initialize an empty DataFrame to store all results
    all_results = pd.DataFrame(columns=['Name', 'Country', 'Year'])
    
    # Loop through years 2015 to 2024
    for year in range(2015, 2025):
        print(f"Fetching data for year {year}...")
        df = get_ioi_results(year)
        
        if df is not None:
            all_results = pd.concat([all_results, df], ignore_index=True)
    
    # Keep the row with the biggest year for each participant-country combination
    unique_results = all_results.sort_values('Year', ascending=False).drop_duplicates(subset=['Name', 'Country'])
    
    # Save to CSV
    unique_results.to_csv('ioi_participants_2015_2024.csv', index=False)

if __name__ == "__main__":
    main()
