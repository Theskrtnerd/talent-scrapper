import pandas as pd

# Read the CSV file
df = pd.read_csv('all_participants_with_apollo.csv')

# Filter for specific columns
filtered_df = df[['Name', 'LinkedIn_Profile', 'apollo_email', 'apollo_name']]

# Display the filtered dataframe
filtered_df.to_csv('filtered_participants.csv', index=False)