from operator import itemgetter
from textwrap import dedent

from langchain.prompts import ChatPromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
from langchain_qdrant import Qdrant
from youtube_lesson_planner.schemas import (
    LearningObjectivesList,
    LessonPlan,
)
from youtube_lesson_planner.utils import (
    format_learning_objectives,
    format_video_context,
)


def generate_plan(
    query: str,
    learning_objectives: LearningObjectivesList,
    vectorstore: Qdrant,
    chunk_time_limit: int,
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

                Using the learning objectives, create a short, effective curriculum for each topic by selecting and integrating the most relevant YouTube videos. 
                The videos should have appropriate start and end timestamps to cover the key points related to the learning objectives. The transcripts are chunked into {chunk_time_limit} seconds for each video. 
                
                The curriculum should be designed for adult learners and hosted on an all-digital asynchronous learning platform. Do not generate any curriculum that is offensive, hateful, derogatory, sexually explicit, harmful, or otherwise inappropriate. Consider that some topics may not have perfectly aligned YouTube videos and that topics like AI and digital marketing may evolve quickly over time. Ensure that each curriculum is structured to include engaging content, practice opportunities, and self-assessment methods. 
                Analyze the topics in the curriculum and determine the best order for them to occur so they are logical and build on each other. Provide a brief description of the overall curriculum and each segment. 
                For each segment, create an activity that is self-contained and directly related to the learning objectives. 
                       
                The activity should involve practical application of the content covered in the video. The self-assessment should enable learners to review their own performance in the activity to determine how well they have mastered the learning objective. Incorporate a variety of self-assessment options based on best practices in adult learning, such as quizzes, reflective journals, practical assignments, self-reviews, presentations, case studies, simulations, and portfolio development. Ensure the self-assessment is clear and provides criteria for learners to evaluate their work. Do not assume the availability of other supporting materials, such as quizzes.
                """
                ),
            ),
        ]
    )

    retriever_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.6, streaming=False)

    retriever = MultiQueryRetriever.from_llm(
        retriever=vectorstore.as_retriever(search_kwargs={"k": 15}), llm=retriever_llm
    )

    llm = ChatOpenAI(model="gpt-4o", temperature=0.5, streaming=False)

    chain = (
        {
            "context": itemgetter("query") | retriever | format_video_context,
            "query": itemgetter("query"),
            "learning_objectives": itemgetter("learning_objectives"),
            "chunk_time_limit": itemgetter("chunk_time_limit"),
        }
        | prompt
        | llm.with_structured_output(LessonPlan)
    )

    result = chain.invoke(
        {
            "query": query,
            "learning_objectives": format_learning_objectives(learning_objectives),
            "chunk_time_limit": chunk_time_limit,
        }
    )

    return result
