from textwrap import dedent
from typing import List
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough

from langchain.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel
from langchain_openai import ChatOpenAI
from youtube_lesson_planner.supabase_client import vectorstore


class Video(BaseModel):
    title: str
    url: str
    transcript: str


class LessonPlan(BaseModel):
    title: str
    description: str
    videos: List[Video]
    steps: List[str]


def generate_plan(query: str):
    generator_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "user",
                dedent(
                    """
                You are an agent that specializes in building learning curriculums based on user queries by searching YouTube. 
                Your task is to create comprehensive and engaging learning curriculums using relevant YouTube videos that match the user's query.

                You are provided with:
                - The user's query
                - The relevant chunks of videos through cosine similarity

                Generate an effective learning curriculum based on the videos and the plan.

                User query: {query}

                Context from transcripts: {context}
                """
                ),
            ),
        ]
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

    generator_llm = ChatOpenAI(model="gpt-4o", temperature=0.5, streaming=False)

    generator_chain = (
        {
            "context": itemgetter("query") | retriever,
            "query": itemgetter("query"),
        }
        | RunnablePassthrough.assign(context=itemgetter("context"))
        | generator_prompt
        | generator_llm.with_structured_output(LessonPlan)
    )

    result = generator_chain.invoke({"query": query})

    return {"lesson_plan": result}
