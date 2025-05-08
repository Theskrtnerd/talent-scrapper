import pandas as pd

# Read the CSV file
df = pd.read_csv('final_debate.csv')

# Sort by Name and Year in descending order
df = df.sort_values(['Name', 'Year'], ascending=[True, False])

# Keep only the first occurrence of each Name (which will be the latest year due to sorting)
df = df.drop_duplicates(subset=['Name'], keep='first')

# Save the filtered DataFrame back to CSV
df.to_csv('final_debate_filtered.csv', index=False)
