import pandas as pd

# Read the CSV files
imo_df = pd.read_csv('imo_participants_with_linkedin.csv')
ioi_df = pd.read_csv('ioi_participants_with_linkedin.csv')
icpc_df = pd.read_csv('icpc_participants_with_linkedin.csv')

# Function to extract Name and LinkedIn Profile
def extract_name_linkedin(df):
    # Select only Name and LinkedIn_Profile columns
    result = df[['Name', 'LinkedIn_Profile']].copy()
    # Filter out rows where LinkedIn_Profile is None/NaN
    result = result[result['LinkedIn_Profile'].notna()]
    return result

# Extract data from each DataFrame
imo_data = extract_name_linkedin(imo_df)
ioi_data = extract_name_linkedin(ioi_df)
icpc_data = extract_name_linkedin(icpc_df)

# Combine all data into one DataFrame
all_data = pd.concat([imo_data, ioi_data, icpc_data], ignore_index=True)

# Remove duplicates based on LinkedIn Profile
all_data = all_data.drop_duplicates(subset=['LinkedIn_Profile'])

# Save to a new CSV file
all_data.to_csv('all_participants_with_linkedin.csv', index=False)
