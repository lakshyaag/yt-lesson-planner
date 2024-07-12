from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

from langchain_qdrant import Qdrant
from youtube_lesson_planner.video import YouTubeVideo


def load_and_add_transcript(video: YouTubeVideo, vectorstore: Qdrant) -> None:
    try:
        transcript = video.load()
        vectorstore.add_documents(transcript)
    except Exception as e:
        print(f"Error loading transcript for video {video.video_id}: {e}")


def get_transcripts(videos: List[YouTubeVideo], vectorstore: Qdrant) -> None:
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(load_and_add_transcript, v, vectorstore) for v in videos
        ]
        for future in as_completed(futures):
            future.result()

    return
