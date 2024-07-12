from textwrap import dedent

from langchain.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from youtube_lesson_planner.nodes.planner import PlanningTemplate


class QueryRewriteTemplate(BaseModel):
    original_query: str = Field(
        ..., description="The original query provided by the user."
    )
    optimized_query: str = Field(..., description="The optimized query for YouTube.")


def format_plan(plan: PlanningTemplate) -> str:
    return "\n".join(
        [
            f"{i + 1}. {step.action} - {step.tool}"
            if step.tool
            else f"{i + 1}. {step.action}"
            for i, step in enumerate(plan.steps)
        ]
    )


def query_rewrite(query: str, plan: PlanningTemplate) -> QueryRewriteTemplate:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "user",
                dedent(
                    """
                You are an agent that specializes in optimizing user queries for YouTube.

                The plan to follow is:
                {plan}

                The user has provided the following query: {input}

                Rewrite the user's query to optimize it for YouTube.
                """
                ),
            ),
        ]
    )

    llm = ChatOpenAI(model="gpt-4o", temperature=0.5, streaming=False)

    chain = prompt | llm.with_structured_output(QueryRewriteTemplate)

    result = chain.invoke({"input": query, "plan": format_plan(plan)})

    return result
