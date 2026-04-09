import pandas as pd
import numpy as np

# Load the cleaned CSV from Task 2
df = pd.read_csv("data/trends_clean.csv")

# Print the number of rows and columns
print(f"Loaded data: {df.shape}")

# Print the first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Calculate average score and average number of comments
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print(f"\nAverage score: {average_score:.2f}")
print(f"Average comments: {average_comments:.2f}")

# Convert score column into a NumPy array
scores = df["score"].to_numpy()

# Use NumPy to calculate statistics
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")

# Find the category with the largest number of stories
category_counts = df["category"].value_counts()
most_common_category = category_counts.idxmax()
most_common_count = category_counts.max()

print(
    f"\nMost stories in: {most_common_category} ({most_common_count} stories)"
)

# Find the row with the highest number of comments
most_commented_story = df.loc[df["num_comments"].idxmax()]

print(
    f"\nMost commented story: \"{most_commented_story['title']}\" "
    f"- {most_commented_story['num_comments']} comments"
)

# Engagement = comments per upvote
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# A story is popular if its score is greater than the average score
df["is_popular"] = df["score"] > average_score

# Save the updated DataFrame for Task 4
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")