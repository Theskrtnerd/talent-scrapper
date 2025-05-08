import pandas as pd
import requests
import json
import os
import time
from pathlib import Path
import dotenv
import numpy as np

dotenv.load_dotenv()
file_name = "final_debate.csv"


# Read the CSV file
df = pd.read_csv(file_name)

# Apollo API configuration
APOLLO_API_KEY = os.getenv('APOLLO_API_KEY')  # Replace with your actual API key
APOLLO_BASE_URL = 'https://api.apollo.io/v1/people/match'

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
    
for index, row in df.iterrows():
    linkedin_url = row['LinkedIn_Profile']
    print(f"Processing {index + 1}/{len(df)}: {linkedin_url}")
    if linkedin_url is None or pd.isna(linkedin_url):
        continue

    response = search_apollo(linkedin_url)
    if response and 'person' in response:
        person = response['person']
        if df.at[index, 'Source'] == "HS_Debate":
            df.at[index, 'University'] = None
            emp_history = person.get('employment_history')
            for exp in emp_history:
                org_name = str(exp.get('organization_name'))
                if 'University' in org_name or 'College' in org_name:
                    df.at[index, 'University'] = org_name
                    print(f"Found university: {org_name}")
                    break
    
    if index % 5 == 0:
        print(f"Saving at {index + 1}/{len(df)}")
        df.to_csv(file_name, index=False)

    time.sleep(0.5)

# Save updated DataFrame
df.to_csv(file_name, index=False)
