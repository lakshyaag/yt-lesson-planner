from typing import Dict, List, Optional

from pydantic import BaseModel as PydanticBaseModel
from langchain.pydantic_v1 import BaseModel, Field
from langchain_qdrant import Qdrant
from typing_extensions import TypedDict

from youtube_lesson_planner.video import YouTubeVideo


class Video(BaseModel):
    """
    Represents a YouTube video with start and end timestamps that fulfill a topic.
    """
    id: str = Field(..., description="The YouTube video ID")
    start_timestamp: float = Field(
        ..., description="The start timestamp of the video to watch (in seconds)"
    )
    end_timestamp: float = Field(
        ..., description="The end timestamp of the video to watch (in seconds)"
    )


class Topic(BaseModel):
    objective: str = Field(..., description="The learning objective for the topic")
    videos: List[Video] = Field(
        ..., description="The YouTube videos to watch for the topic"
    )
    description: str = Field(..., description="The description of the topic")
    steps: List[str] = Field(
        ...,
        description="The steps to follow to achieve the learning objective for the topic",
    )

    suggested_activities: List[str] = Field(
        ..., description="Suggested activities for the topic to reinforce learning"
    )


class LessonPlan(BaseModel):
    title: str = Field(..., description="The title of the lesson plan")
    topics: List[Topic] = Field(
        ..., description="The topics covered in the lesson plan"
    )
    comments: Optional[str] = Field(None, description="Additional comments or notes")


class LearningObjectives(BaseModel):
    index: int = Field(..., description="The index of the learning objective.")
    objective: str = Field(..., description="The learning objective.")


class LearningObjectivesList(BaseModel):
    objectives: List[LearningObjectives] = Field(
        ..., description="The list of learning objectives."
    )


class QueryRewriteTemplate(BaseModel):
    original_query: str = Field(
        ..., description="The original query provided by the user."
    )
    optimized_query: str = Field(..., description="The optimized query for YouTube.")


class AgentState(TypedDict):
    original_query: str
    rewritten_query: str
    learning_objectives: LearningObjectivesList
    lesson_plan: LessonPlan
    videos: Dict[str, YouTubeVideo]
    vectorstore: Qdrant
    transcripts_status: bool


class RequestModel(PydanticBaseModel):
    user_input: str
