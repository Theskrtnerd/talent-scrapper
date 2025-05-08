import pandas as pd
import requests
import json
import os
import time
from pathlib import Path
import dotenv
import numpy as np

dotenv.load_dotenv()

# Read the CSV file
df = pd.read_csv('final_db.csv')

# Apollo API configuration
APOLLO_API_KEY = os.getenv('APOLLO_API_KEY')  # Replace with your actual API key
APOLLO_BASE_URL = 'https://api.apollo.io/v1/people/match'

# Function to search Apollo for a LinkedIn profile
def search_apollo(linkedin_url):
    headers = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'x-api-key': APOLLO_API_KEY,
        'Accept': 'application/json',
    }
    
    params = {
        'linkedin_url': linkedin_url
    }
    
    try:
        response = requests.post(APOLLO_BASE_URL+'?linkedin_url='+linkedin_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error searching for {linkedin_url}: {e}")
        return None
    
# row = df.iloc[0]
# linkedin_url = row['LinkedIn_Profile']
# print(linkedin_url)
# response = search_apollo(linkedin_url)
# print(response)

# df['Email'] = None
# df['Apollo_Name'] = None
# df['Apollo_Response'] = None

apollo_df = pd.read_csv('archive/all_participants_with_apollo.csv')
# Create mapping with individual columns
mapping = {
    row['LinkedIn_Profile']: {
        'apollo_email': row['apollo_email'],
        'apollo_name': row['apollo_name'],
        'apollo_response': row['apollo_response']
    }
    for _, row in apollo_df.iterrows()
}

# Process each LinkedIn profile
for index, row in df.iloc[230:330].iterrows():
    linkedin_url = row['LinkedIn_Profile']
    print(f"Processing {index + 1}/{len(df)}: {linkedin_url}")

    if not pd.isna(linkedin_url): 
        if linkedin_url in mapping:
            print("Found in mapping")
            existing_data = mapping[linkedin_url]
            df.at[index, 'Email'] = existing_data['apollo_email']
            df.at[index, 'Apollo_Name'] = existing_data['apollo_name']
            df.at[index, 'Apollo_Response'] = existing_data['apollo_response']
        else:
            print("Not found in mapping")
            response = search_apollo(linkedin_url)
            if response and 'person' in response:
                person = response['person']
                df.at[index, 'Email'] = person.get('email')
                df.at[index, 'Apollo_Name'] = person.get('name')
                df.at[index, 'Apollo_Response'] = json.dumps(response)
    
    if index % 5 == 0:
        print(f"Saving at {index + 1}/{len(df)}")
        df.to_csv('final_db.csv', index=False)
        # Save subset with specific columns
        subset_df = df[['Name', 'University', 'Year', 'Source', 'Country', 'LinkedIn_Profile', 'Email']]
        subset_df.to_csv('final_db_subset.csv', index=False)
    
    time.sleep(0.5)

# Save updated DataFrame
df.to_csv('final_db.csv', index=False)
# Save final subset
subset_df = df[['Name', 'University', 'Year', 'Source', 'Country', 'LinkedIn_Profile', 'Email']]
subset_df.to_csv('final_db_subset.csv', index=False)
