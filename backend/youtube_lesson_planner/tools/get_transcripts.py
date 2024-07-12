from typing import List

from youtube_lesson_planner.video import YouTubeVideo
from youtube_lesson_planner.supabase_client import vectorstore


def get_transcripts(videos: List[YouTubeVideo]) -> None:
    for v in videos:
        try:
            transcript = v.load()
            vectorstore.add_documents(transcript)
        except Exception as e:
            print(f"Error loading transcript for video {v.video_id}: {e}")
            continue

    return
