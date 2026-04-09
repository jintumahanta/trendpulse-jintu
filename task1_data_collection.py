# Import required libraries
import requests
import json
import time
import os
from datetime import datetime

# Keywords used to decide the category of each story
CATEGORY_KEYWORDS = {
    "technology": [
        "ai", "software", "tech", "code", "computer", "data",
        "cloud", "api", "gpu", "llm", "startup", "programming",
        "open source", "developer", "python", "app"
    ],

    "worldnews": [
        "war", "iran", "america", "government", "country", "president", "election",
        "climate", "attack", "global", "china", "india", "russia",
        "ukraine", "minister", "military", "security", "court",
        "law", "politics", "state", "economy"
    ],

    "sports": [
        "nfl", "nba", "fifa", "sport", "sports", "game", "team",
        "player", "league", "championship", "football", "cricket",
        "match", "tournament", "olympics", "season", "coach",
        "win", "cup", "club", "soccer", "tennis", "baseball",
        "basketball", "golf", "hockey", "race", "racing"
    ],


    "science": [
        "research", "study", "studies", "scientist", "scientists",
        "science", "space", "physics", "biology", "chemistry",
        "discovery", "discover", "nasa", "genome", "medical",
        "medicine", "health", "disease", "drug", "brain",
        "cell", "energy", "climate", "quantum", "mars",
        "earth", "planet", "universe", "experiment", "lab"
    ],

    "entertainment": [
        "movie", "film", "music", "netflix", "game", "book",
        "show", "award", "streaming", "tv", "series", "youtube",
        "song", "actor", "actress", "video", "media"
    ]
}

# Function to find the category from the story title
def get_category(title):
    title = title.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title:
                return category
            
    return None

# Header required by the API
headers = {"User-Agent": "TrendPulse/1.0"}
url = "https://hacker-news.firebaseio.com/v0/topstories.json"

# Fetch the top story IDs from HackerNews
response = requests.get(url, headers=headers, timeout=10)
story_ids = response.json()[:1000]

# Store stories separately for each category
stories_by_category = {
    "technology": [],
    "worldnews": [],
    "sports": [],
    "science": [],
    "entertainment": []
}

# Go through every story ID and fetch its details
for story_id in story_ids:
    try:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        response = requests.get(story_url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"Failed to fetch story {story_id}")
            continue

        story = response.json()

    except Exception as e:
        print(f"Skipping story {story_id}: {e}")
        continue

    title = story.get("title", "")
    category = get_category(title)

    # Skip if no category matched
    if category is None:
        continue

    # Save only up to 25 stories per category
    if len(stories_by_category[category]) >= 25:
        continue

    # Create a clean dictionary with only required fields
    story_data = {
        "post_id": story.get("id"),
        "title": title,
        "category": category,
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by", "unknown"),
        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    }

    # Add the story to its category list
    stories_by_category[category].append(story_data)
    # If all categories have collected 25 stories, stop the loop
    done = True

    for category_name in stories_by_category:
        if len(stories_by_category[category_name]) < 25:
            done = False
            break
    if done:
        break

    # Pause for 2 seconds after completing one category
    if len(stories_by_category[category]) == 25:
        print(f"Finished category: {category}")
        time.sleep(2)


# Show how many stories were collected in each category
print({cat: len(stories_by_category[cat]) for cat in stories_by_category})

# Combine all category lists into one final list
all_stories = []

for category_list in stories_by_category.values():
    all_stories.extend(category_list)

# Create data folder if it does not exist
os.makedirs("data", exist_ok=True)

date_string = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{date_string}.json"

# Save all stories into a JSON file
with open(filename, "w", encoding="utf-8") as file:
    json.dump(all_stories, file, indent=4)

print(f"collected {len(all_stories)} stories. Saved to {filename}")




