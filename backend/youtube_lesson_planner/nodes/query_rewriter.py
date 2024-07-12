from textwrap import dedent

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from youtube_lesson_planner.schemas import LearningObjectivesList, QueryRewriteTemplate
from youtube_lesson_planner.utils import format_learning_objectives


def rewrite(query: str, plan: LearningObjectivesList) -> QueryRewriteTemplate:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "user",
                dedent(
                    """
                You are an agent that specializes in optimizing user queries for YouTube.

                The learning objectives for the user's query are:
                {plan}

                The user has provided the following query: {input}

                Rewrite the user's query to optimize it for YouTube to find relevant videos that match ALL the learning objectives, while keeping the intent of the original query.

                Ensure that the optimized query is clear, CONCISE, and specific to improve the search results on YouTube.
                """
                ),
            ),
        ]
    )

    llm = ChatOpenAI(model="gpt-4o", temperature=0.5, streaming=False)

    chain = prompt | llm.with_structured_output(QueryRewriteTemplate)

    result = chain.invoke({"input": query, "plan": format_learning_objectives(plan)})

    return result
