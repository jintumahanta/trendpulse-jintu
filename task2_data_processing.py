import pandas as pd
import os

# Find the newest JSON file inside the data folder
json_files = [file for file in os.listdir("data") if file.endswith(".json")]
json_files.sort()

latest_file = os.path.join("data", json_files[-1])

# Load the JSON file into a pandas DataFrame
df = pd.read_json(latest_file)

# Print how many rows were loaded
print(f"Loaded {len(df)} stories from {latest_file}")

# Remove duplicate rows that have the same post_id
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# Remove rows where important fields are missing
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Convert score and num_comments columns to integers
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Keep only stories with score 5 or more
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Remove extra spaces from the beginning and end of titles
df["title"] = df["title"].str.strip()

# Save the cleaned data as a CSV file
output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

# Print how many stories belong to each category
print("\nStories per category:")
print(df["category"].value_counts())