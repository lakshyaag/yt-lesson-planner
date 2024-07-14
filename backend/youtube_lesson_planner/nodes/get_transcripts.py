from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_openai import OpenAIEmbeddings

from langchain_qdrant import Qdrant
from youtube_lesson_planner.video import YouTubeVideo


def load_and_add_transcript(video: YouTubeVideo) -> None:
    try:
        transcript = video.load()
        return transcript
    except Exception as e:
        print(f"Error loading transcript for video {video.video_id}: {e}")


def get_transcripts(videos: List[YouTubeVideo]) -> None:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1536)
    transcripts = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(load_and_add_transcript, v) for v in videos]
        for future in as_completed(futures):
            transcript = future.result()
            if transcript:
                transcripts.append(transcript)

    vectorstore = Qdrant.from_documents(
        documents=transcripts[0],
        collection_name="youtube_transcripts",
        location=":memory:",
        embedding=embeddings,
    )

    for transcript in transcripts[1:]:
        vectorstore.add_documents(transcript)

    return vectorstore
