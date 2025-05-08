import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import dotenv
import requests
from serpapi import GoogleSearch
from rapidfuzz import fuzz
import Levenshtein

dotenv.load_dotenv()

def scrape_ipho(year: int, allowed_countries: list[str] = None) -> pd.DataFrame:
    file_name = f"data/ipho_{year}.csv"
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    url = f"https://ipho-unofficial.org/timeline/{year}/individual"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {year}: Status code {response.status_code}")
        return pd.DataFrame()
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    data = []
    rows = table.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 7:
            name = cols[0].text.strip()
            country = cols[1].text.strip()
            if allowed_countries and country not in allowed_countries:
                continue
            data.append({
                'Name': name,
                'Country': country,
                'Source': 'IPhO',
                'Year': year
            })
    df = pd.DataFrame(data)
    if not df.empty and not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
    if not df.empty:
        df.to_csv(file_name, index=False)
    return df

def scrape_icho(year: int, allowed_countries: list[str] = None) -> pd.DataFrame:
    file_name = f"data/icho_{year}.csv"
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    id_param = 54 - (2022 - year)
    url = f"http://www.icho-official.org/results/results.php?id={id_param}&year={year}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {year}: Status code {response.status_code}")
        return pd.DataFrame()
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    data = []
    rows = table.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) < 4:
            continue
        name = cols[0].text.strip()
        country = cols[2].text.strip()
        if allowed_countries and country not in allowed_countries:
            continue
        data.append({
            'Name': name,
            'Country': country,
            'Source': 'IChO',
            'Year': year
        })
    df = pd.DataFrame(data)
    if not df.empty and not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
    if not df.empty:
        df.to_csv(file_name, index=False)
    return df

def scrape_imo(year: int, allowed_countries: list[str] = None) -> pd.DataFrame:
    file_name = f"data/imo_{year}.csv"
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    url = f"https://www.imo-official.org/year_individual_r.aspx?year={year}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {year}: Status code {response.status_code}")
        return pd.DataFrame()
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    data = []
    rows = table.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 3:
            name = cols[0].text.strip()
            country = cols[1].text.strip()
            if allowed_countries and country not in allowed_countries:
                continue
            data.append({
                'Name': name,
                'Country': country,
                'Source': 'IMO',
                'Year': year
            })
    df = pd.DataFrame(data)
    if not df.empty and not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
    if not df.empty:
        df.to_csv(file_name, index=False)
    return df

def merge_data(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    required_columns = ["Name", "Country", "Source", "Year"]
    dfs = [df for df in dfs if not df.empty]
    if not dfs:
        return pd.DataFrame(columns=required_columns)
    for df in dfs:
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"DataFrame must contain exactly these columns: {required_columns}")
        if len(df.columns) != len(required_columns):
            raise ValueError(f"DataFrame must contain exactly {len(required_columns)} columns")
    return pd.concat(dfs)

def linkedin_search(name: str, country: str="", source: str="", info: str="", year: int=None) -> str:
    query_info = [name, country, source, info]
    query_info = [info for info in query_info if info]
    query = " ".join(query_info)
    query = f"{query} site:linkedin.com"
    print(query, year)
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
        if "organic_results" in results:    
            result_links = {results["organic_results"][i]["link"]: results["organic_results"][i]["title"] for i in range(len(results["organic_results"]))}
            for link, title in result_links.items():
                if "linkedin.com/in/" in link:
                    linkedin_name = title.split("-")[0].split("–")[0].strip()
                    fuzz_score = fuzz.ratio(linkedin_name.lower(), name.lower())
                    print(linkedin_name, name, fuzz_score)
                    if fuzz_score > 50:
                        print(f"Found {name} on LinkedIn: {link} with linkedin name {linkedin_name}")
                        lev_score = Levenshtein.distance(linkedin_name.lower(), name.lower())
                        return link.split("?")[0], linkedin_name, lev_score
        else:
            return None, None, None
    except Exception as e:
        print(e)
        return None, None, None

    return None, None, None

def linkedin_scrape(df: pd.DataFrame) -> pd.DataFrame:
    if "LinkedIn" not in df.columns:
        df["LinkedIn"] = None
    if "LinkedInName" not in df.columns:
        df["LinkedInName"] = None
    if "LevScore" not in df.columns:
        df["LevScore"] = None
    for index, row in df.iterrows():
        if index % 5 == 0:
            df.to_csv(f"data/linkedin_scrape.csv", index=False)
        if pd.notna(row["LinkedIn"]):
            continue
        linkedin_url = None
        search_attempts = [
            {"name": row["Name"], "source": row["Source"], "year": row["Year"]},
            {"name": row["Name"], "year": row["Year"]}
        ]
        for params in search_attempts:
            linkedin_url, linkedin_name, lev_score = linkedin_search(**params)
            if linkedin_url:
                df.loc[index, "LinkedIn"] = linkedin_url
                df.loc[index, "LinkedInName"] = linkedin_name
                df.loc[index, "LevScore"] = lev_score + 4 * search_attempts.index(params)
                break
    df.to_csv(f"data/linkedin_scrape.csv", index=False)
    return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset=["Name", "Country"])
    return df

def main():
    ipho_dfs = [scrape_ipho(year) for year in range(2015, 2025)]
    icho_dfs = [scrape_icho(year) for year in range(2015, 2025)]

    merged_df = merge_data(ipho_dfs + icho_dfs)
    merged_df = remove_duplicates(merged_df)
    if not os.path.exists("data/linkedin_scrape.csv"):
        linkedin_scrape(merged_df)
    else:
        merged_df = pd.read_csv("data/linkedin_scrape.csv")
        linkedin_scrape(merged_df)

if __name__ == "__main__":
    main()