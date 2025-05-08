import pandas as pd

# Read the CSV files
icpc_df = pd.read_csv('icpc_participants_with_linkedin.csv')
imo_df = pd.read_csv('imo_participants_with_linkedin.csv')
ioi_df = pd.read_csv('ioi_participants_with_linkedin.csv')

apollo_df = pd.read_csv('all_participants_with_apollo.csv')
email_mapping = dict(zip(apollo_df['LinkedIn_Profile'], apollo_df['apollo_email']))

# Function to standardize columns
def standardize_df(df, source):
    # Ensure required columns exist
    if 'Country' not in df.columns:
        df['Country'] = 'United States of America'
    if 'University' not in df.columns:
        df['University'] = None

    df['Source'] = source
    df['Email'] = df['LinkedIn_Profile'].apply(
        lambda x: email_mapping.get(x) if pd.notna(x) else None
    )
    # Select and rename columns
    return df[['Name', 'Year', 'LinkedIn_Profile', 'Country', 'University', 'Email', 'Source']]

# Standardize each dataframe
icpc_df = standardize_df(icpc_df, 'ICPC')
imo_df = standardize_df(imo_df, 'IMO')
ioi_df = standardize_df(ioi_df, 'IOI')

# Concatenate the dataframes
merged_df = pd.concat([icpc_df, imo_df, ioi_df], ignore_index=True)

# Save the merged dataframe
merged_df.to_csv('final.csv', index=False)
