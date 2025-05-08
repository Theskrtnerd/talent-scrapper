import pandas as pd
from serpapi import GoogleSearch
import os
import dotenv

dotenv.load_dotenv()

def get_linkedin_profile(name, university="", country="", source=""):
    university = "" if pd.isna(university) else university
    query = f"{name} {university} {country} {source} site:linkedin.com"
    print(query)

    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": os.getenv("SERPAPI_KEY")
    }

    search = GoogleSearch(params)
    try:        
        results = search.get_dict()
        if "organic_results" in results and "linkedin.com/in/" in results["organic_results"][0]["link"]:
            return results["organic_results"][0]["link"]
        else:
            return None
    except Exception as e:
        print(e)
        return None
    
print("Starting scrape...")

file_name = "final_hs_debate.csv"

df = pd.read_csv(file_name)

for index, row in df.iterrows():
    df.at[index, 'Source'] = "HS_Debate"
    df.at[index, 'University'] = None
    linkedin_url = get_linkedin_profile(name=row["Name"], source="Debate")
    df.at[index, 'LinkedIn_Profile'] = linkedin_url
    print(f"Processed {index + 1}/{len(df)}: {row['Name']} {row['Country']} - {linkedin_url}")

    if index % 10 == 0:
        df.to_csv(file_name, index=False)

df.to_csv(file_name, index=False)