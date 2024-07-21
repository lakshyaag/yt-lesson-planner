from operator import itemgetter
from textwrap import dedent

from langchain.prompts import ChatPromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
from langchain_qdrant import Qdrant
from youtube_lesson_planner.schemas import LearningObjectivesList, LessonPlan
from youtube_lesson_planner.utils import (
    format_learning_objectives,
    format_video_context,
)


def generate_plan(
    query: str, learning_objectives: LearningObjectivesList, vectorstore: Qdrant
) -> LessonPlan:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "user",
                dedent(
                    """
                You are an agent that specializes in building learning curriculums based on user queries by searching YouTube. 
                Your task is to create comprehensive and engaging learning curriculums using relevant YouTube videos that match the user's query.

                The learning objectives for the user's query identified by you earlier are:
                {learning_objectives}

                User query: {query}

                Relevant video context: {context}

                Using the learning objectives, create a short, effective curriculum for each topic by selecting and integrating the most relevant YouTube videos. The curriculum should be designed for adult learners and hosted on an all-digital asynchronous learning platform. Do not generate any curriculum that is offensive, hateful, derogatory, sexually explicit, harmful, or otherwise inappropriate. Consider that some topics may not have perfectly aligned YouTube videos and that topics like AI and digital marketing may evolve quickly over time. Ensure that each curriculum is structured to include engaging content, practice opportunities, and self-assessment methods. 
                Analyze the topics in the curriculum and determine the best order for them to occur so they are logical and build on each other. Provide a brief description of the overall curriculum and each segment. 
                For each segment, create an activity that is self-contained and directly related to the learning objectives. 
                       
                The activity should involve practical application of the content covered in the video. The self-assessment should enable learners to review their own performance in the activity to determine how well they have mastered the learning objective.
                """
                ),
            ),
        ]
    )

    retriever_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.6, streaming=False)

    retriever = MultiQueryRetriever.from_llm(
        retriever=vectorstore.as_retriever(search_kwargs={"k": 10}), llm=retriever_llm
    )

    llm = ChatOpenAI(model="gpt-4o", temperature=0.5, streaming=False)

    chain = (
        {
            "context": itemgetter("query") | retriever | format_video_context,
            "query": itemgetter("query"),
            "learning_objectives": itemgetter("learning_objectives"),
        }
        | prompt
        | llm.with_structured_output(LessonPlan)
    )

    result = chain.invoke(
        {
            "query": query,
            "learning_objectives": format_learning_objectives(learning_objectives),
        }
    )

    return result
