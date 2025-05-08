import pandas as pd

icpc_df = pd.read_csv('icpc_participants_2015_2024.csv')
imo_df = pd.read_csv('imo_participants_2015_2024.csv')
ioi_df = pd.read_csv('ioi_participants_2015_2024.csv')

def standardize_df(df, source):
    if 'University' not in df.columns:
        df['University'] = None
    # Standardize country names
    df.loc[df['Country'] == 'United States of America', 'Country'] = 'United States'

    df['Source'] = source
    return df[['Name', 'Year', 'Country', 'University', 'Source']]

# Standardize each dataframe
icpc_df = standardize_df(icpc_df, 'ICPC')
imo_df = standardize_df(imo_df, 'IMO')
ioi_df = standardize_df(ioi_df, 'IOI')

# Merge the dataframes
merged_df = pd.concat([icpc_df, imo_df, ioi_df], ignore_index=True)

merged_df = merged_df.sort_values('Name')

merged_df = merged_df.groupby(['Name', 'Country']).agg({
    'University': lambda x: next((u for u in x if pd.notna(u)), None),
    'Year': lambda x: sorted(set(x))[0],
    'Source': lambda x: sorted(set(x))[0]
}).reset_index()

# Save the merged dataframe
merged_df.to_csv('merged_df.csv', index=False)

