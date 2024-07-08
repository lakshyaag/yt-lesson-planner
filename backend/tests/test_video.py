import pytest
from youtube_lesson_planner.video import YouTubeVideo


@pytest.fixture
def youtube_video():
    return YouTubeVideo(
        video_id="RIX4ufelA58",
        title="Do You Know How Mobile Apps Are Released?",
        description="Get a Free System Design PDF with 158 pages by subscribing to our weekly newsletter: https://bytebytego.ck.page/subscribe ...",
        published_at="2024-05-23T15:30:05Z",
        channel_title="ByteByteGo",
        chunk_time_limit=120,
    )


def test_youtube_video_init(youtube_video):
    assert youtube_video.video_id == "RIX4ufelA58"
    assert youtube_video.title == "Do You Know How Mobile Apps Are Released?"
    assert (
        youtube_video.description
        == "Get a Free System Design PDF with 158 pages by subscribing to our weekly newsletter: https://bytebytego.ck.page/subscribe ..."
    )
    assert youtube_video.published_at == "2024-05-23T15:30:05Z"
    assert youtube_video.channel_title == "ByteByteGo"
    assert youtube_video.chunk_time_limit == 120


def test_youtube_video_repr(youtube_video):
    assert (
        repr(youtube_video)
        == "Do You Know How Mobile Apps Are Released? by ByteByteGo - RIX4ufelA58"
    )


def test_youtube_get_transcript(youtube_video):
    transcript = youtube_video._get_transcript()
    assert transcript is not None
    assert len(transcript) > 0


def test_youtube_get_transcript_chunks(youtube_video):
    transcript = youtube_video._get_transcript()
    transcript_pieces = list(youtube_video._get_transcript_chunks(transcript))

    assert len(transcript_pieces) > 0
