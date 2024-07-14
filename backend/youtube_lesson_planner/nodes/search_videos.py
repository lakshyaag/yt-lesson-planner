import json
import os
from typing import Dict

import googleapiclient.discovery
from dotenv import load_dotenv
from youtube_lesson_planner.video import YouTubeVideo

load_dotenv()

youtube = googleapiclient.discovery.build(
    "youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY")
)


def search_youtube(
    query: str, max_results: int = 10, chunk_time_limit: int = 60
) -> Dict[str, YouTubeVideo]:
    search_result = (
        youtube.search()
        .list(
            part="snippet",
            q=query,
            maxResults=max_results,
            type="video",
            videoCaption="closedCaption",
        )
        .execute()
    )

    items = search_result["items"]

    # Save search result with query name
    # with open(f"../search_data/search_results_{query}.json", "w") as f:
    #     json.dump(search_result, f, indent=4)

    # with open(
    #     "../search_data/search_results_Generative AI basics explained.json", "r"
    # ) as f:
    #     search_result = json.load(f)
    #     items = search_result["items"]

    yt_videos = {
        item["id"]["videoId"]: YouTubeVideo(
            video_id=item["id"]["videoId"],
            title=item["snippet"]["title"],
            description=item["snippet"]["description"],
            published_at=item["snippet"]["publishedAt"],
            channel_title=item["snippet"]["channelTitle"],
            chunk_time_limit=chunk_time_limit,
        )
        for item in items
    }

    return yt_videos
