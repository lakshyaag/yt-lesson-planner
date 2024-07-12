import os
from typing import Any, Dict, Generator, List

import googleapiclient.discovery
from dotenv import load_dotenv
from langchain.schema import Document
from rich import print
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

youtube = googleapiclient.discovery.build(
    "youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY")
)


def search_videos(query: str, max_results: int = 10) -> dict:
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        videoCaption="closedCaption",
        maxResults=max_results,
    )

    response = request.execute()
    return response


class YouTubeVideo:
    def __init__(
        self,
        video_id,
        title,
        description,
        published_at,
        channel_title,
        chunk_time_limit=120,
    ):
        self.video_id = video_id
        self.title = title
        self.description = description
        self.published_at = published_at
        self.channel_title = channel_title
        self.chunk_time_limit = chunk_time_limit

    def __repr__(self):
        return f"{self.title} by {self.channel_title} - {self.video_id} | {self.description}"

    def _get_transcript(self):
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(self.video_id)
            for t in transcript_list:
                if t.language_code in ["en", "en-US"]:
                    return t.fetch()
                elif any(
                    lang["language_code"] == "en" for lang in t.translation_languages
                ):
                    return t.translate("en").fetch()
        except Exception as e:
            print(f"Error fetching transcript: {e} for video {self.video_id}")
        return None

    def _make_chunk_document(
        self, chunk_pieces: List[Dict], chunk_start_seconds: int
    ) -> Document:
        """Create Document from chunk of transcript pieces."""
        # TODO: Add overlap for chunking to avoid cutting off sentences.
        m, s = divmod(chunk_start_seconds, 60)
        h, m = divmod(m, 60)
        return Document(
            page_content=" ".join(
                map(lambda chunk_piece: chunk_piece["text"].strip(" "), chunk_pieces)
            ),
            metadata={
                "start_seconds": chunk_start_seconds,
                "start_timestamp": f"{h:02d}:{m:02d}:{s:02d}",
                "source": f"https://www.youtube.com/watch?v={self.video_id}&t={chunk_start_seconds}s",
                "title": self.title,
                "video_id": self.video_id,
            },
        )

    def _get_transcript_chunks(
        self, transcript_pieces: List[Dict]
    ) -> Generator[Document, None, None]:
        chunk_pieces: List[Dict[str, Any]] = []
        chunk_start_seconds = 0
        chunk_time_limit = self.chunk_time_limit
        for transcript_piece in transcript_pieces:
            piece_end = transcript_piece["start"] + transcript_piece["duration"]
            if piece_end > chunk_time_limit:
                if chunk_pieces:
                    yield self._make_chunk_document(chunk_pieces, chunk_start_seconds)
                chunk_pieces = []
                chunk_start_seconds = chunk_time_limit
                chunk_time_limit += self.chunk_time_limit

            chunk_pieces.append(transcript_piece)

        if len(chunk_pieces) > 0:
            yield self._make_chunk_document(chunk_pieces, chunk_start_seconds)

    def load(self):
        try:
            transcripts = self._get_transcript()
            if transcripts:
                return list(self._get_transcript_chunks(transcripts))
        except Exception as e:
            print(f"Error: {e} for video {self.video_id}")

        return []