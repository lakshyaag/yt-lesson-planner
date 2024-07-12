from textwrap import dedent
from typing import List

from langchain.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI


class PlanningStep(BaseModel):
    thought: str = Field(..., description="The thought or reasoning behind the step.")
    action: str = Field(..., description="The action to take in the step.")
    tool: str = Field(..., description="The tool to use in the step.")


class PlanningTemplate(BaseModel):
    steps: List[PlanningStep] = Field(..., description="The steps to take in the plan.")


def get_plan(query: str):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "user",
                dedent(
                    """
                You are an agent that specializes in building learning curriculums based on user queries by searching YouTube. 
                Your task is to create comprehensive and engaging learning curriculums using relevant YouTube videos that match the user's query.

                The tools provided to you are:
                - query_rewrite(): To rewrite the user's query to optimize it for YouTube
                - search_videos(): To search for videos based on user queries
                - get_transcripts(): To get the transcripts of the videos
                
                Make a plan to create a learning curriculum based on the user's query, only including steps that require the use of the tools provided.
                """
                ),
            ),
            ("user", "Query: {input}"),
        ]
    )

    llm = ChatOpenAI(model="gpt-4o", temperature=0.5, streaming=False)

    chain = prompt | llm.with_structured_output(PlanningTemplate)

    result = chain.invoke({"input": query})

    return {"plan": result}
