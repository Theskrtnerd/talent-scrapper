import pandas as pd

# Read the CSV files
hs_debate_df = pd.read_csv('final_hs_debate.csv')
usudc_df = pd.read_csv('usudc_results.csv')

# Select and standardize columns
hs_debate_df = hs_debate_df[['Name', 'Year', 'LinkedIn_Profile', 'Country', 'University', 'Source']]
usudc_df = usudc_df[['Name', 'Year', 'LinkedIn_Profile', 'Country', 'University', 'Source']]

# Merge the dataframes
merged_df = pd.concat([hs_debate_df, usudc_df], ignore_index=True)

# Sort by name
merged_df = merged_df.sort_values('Name')

# Save the merged dataframe
merged_df.to_csv('final_debate.csv', index=False)
