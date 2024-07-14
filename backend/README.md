# YouTube Lesson Planner

## Overview

The YouTube Lesson Planner is an application designed to generate comprehensive lesson plans from YouTube videos based on user queries. It leverages the YouTube API to search for videos, extract transcripts, and compile them into structured learning curriculums using Large Language Models (LLMs).

## Project Structure

- backend/youtube_lesson_planner/
  - nodes/: Contains various nodes for the lesson plan generation workflow.
    - `generate_plan.py`: Main node for generating lesson
    - `get_transcript.py`: Node for extracting video transcripts
    - `search_videos.py`: Node for searching YouTube videos
    - `learning_objectives.py`: Node for building learning objectives from user's query
    - `query_rewriter.py`: Node for rewriting user's query to improve search results
  - `app.py`: Main FastAPI application.
  - `video.py`: Functions for interacting with YouTube API and processing videos.
  - `schemas.py`: Data models and schemas.
  - `utils.py`: Utility functions.
- `pyproject.toml`: Project dependencies and configuration.

## Installation & Usage

1. Clone the repository:

```bash
   git clone <https://github.com/lakshyaag/yt-lesson-planner.git>
   cd youtube-lesson-planner
```

2. Install dependencies:

```bash
    pip install poetry
    poetry install
```

3. Set up environment variables based on `.env.example`.

4. Run the FastAPI application:

```bash
    poetry run start
```

This will start the server at `http://localhost:8000`.

## API Endpoints

- `/learn/`: Generate a lesson plan based on a user query.
