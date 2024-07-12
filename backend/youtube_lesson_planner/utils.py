from youtube_lesson_planner.schemas import LearningObjectivesList
from langchain.schema import Document
from textwrap import dedent


def format_learning_objectives(plan: LearningObjectivesList) -> str:
    steps = []
    for objective in plan.objectives:
        steps.append(f"{objective.index}. {objective.objective}")

    return "\n".join(steps)


def format_video_context(chunks: list[Document]) -> str:
    context = []
    for chunk in chunks:
        context.append(
            dedent(
                f"""{chunk.metadata["title"]} ({chunk.metadata["video_id"]}) at {chunk.metadata["start_seconds"]}s:
                
                {chunk.page_content}"""
            )
        )

    return "\n\n".join(context)
