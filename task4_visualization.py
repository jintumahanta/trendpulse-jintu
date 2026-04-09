import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the CSV created in Task 3
df = pd.read_csv("data/trends_analysed.csv")

# Create the outputs folder if it does not already exist
os.makedirs("outputs", exist_ok=True)

# Get the 10 highest-scoring stories
top_stories = df.sort_values("score", ascending=False).head(10)

# Shorten very long titles so the chart stays readable
short_titles = [
    title[:50] + "..." if len(title) > 50 else title
    for title in top_stories["title"]
]

# Create a horizontal bar chart of the top 10 stories
plt.figure(figsize=(10, 6))
plt.barh(short_titles, top_stories["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.show()


# Count how many stories belong to each category
category_counts = df["category"].value_counts()

# Create a bar chart of stories per category
plt.figure(figsize=(8, 5))
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.show()

# Separate popular and non-popular stories
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

# Create a scatter plot of score vs comments
plt.figure(figsize=(8, 6))
plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.show()

# Create a combined dashboard with all charts
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("TrendPulse Dashboard", fontsize=16)

# Top stories chart in dashboard
axes[0, 0].barh(short_titles, top_stories["score"])
axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].set_xlabel("Score")
axes[0, 0].invert_yaxis()

# Category chart in dashboard
axes[0, 1].bar(category_counts.index, category_counts.values)
axes[0, 1].set_title("Stories per Category")
axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Stories")

# Scatter plot in dashboard
axes[1, 0].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[1, 0].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[1, 0].set_title("Score vs Comments")
axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Comments")
axes[1, 0].legend()

# Leave the final subplot empty
axes[1, 1].axis("off")

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.show()

print("Charts saved in outputs/ folder")