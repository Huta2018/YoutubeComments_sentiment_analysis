#Download all comments from prakash saputs youtube channel for all videos


from googleapiclient.discovery import build
from tqdm import tqdm
import json

API_KEY = 'enter_api_key_obtained_from_google_for_youtube'
CHANNEL_ID = "UCLjMHtCwaTy4aCs-EVudqYQ"

youtube = build("youtube", "v3", developerKey=API_KEY)

# Step 1: Get all video IDs from the channel
def get_all_video_ids(channel_id):
    video_ids = []
    next_page_token = None

    while True:
        res = youtube.search().list(
            part="id",
            channelId=channel_id,
            maxResults=50,
            order="date",
            pageToken=next_page_token,
            type="video"
        ).execute()

        for item in res["items"]:
            video_ids.append(item["id"]["videoId"])

        next_page_token = res.get("nextPageToken")
        if not next_page_token:
            break

    return video_ids

# Step 2: Get comments for each video
def get_comments(video_id):
    comments = []
    next_page_token = None

    while True:
        try:
            res = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
                textFormat="plainText"
            ).execute()

            for item in res["items"]:
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comment_text = snippet["textDisplay"]
                author = snippet["authorDisplayName"]
                comments.append({
                    "author": author,
                    "comment": comment_text
                })

            next_page_token = res.get("nextPageToken")
            if not next_page_token:
                break
        except Exception as e:
            break  # Skip on error

    return comments


# Step 3: Build dictionary {video_id: [comments]}
def build_comment_dict(video_ids):
    comment_dict = {}
    for vid in tqdm(video_ids, desc="Fetching comments"):
        comments = get_comments(vid)
        if comments:
            comment_dict[vid] = comments
    return comment_dict

# Run all codes and get data
video_ids = get_all_video_ids(CHANNEL_ID)
print(f"Found {len(video_ids)} videos.")

comment_data = build_comment_dict(video_ids)

# Save comments to JSON
with open("prakash_saput_comments.json", "w", encoding="utf-8") as f:
    json.dump(comment_data, f, ensure_ascii=False, indent=2)

print("All comments saved to prakash_saput_comments.json")
