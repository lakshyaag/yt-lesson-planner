from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import Qdrant
from langgraph.graph import END, StateGraph
from qdrant_client import QdrantClient

from youtube_lesson_planner.nodes.generate_plan import generate_plan
from youtube_lesson_planner.nodes.get_transcripts import get_transcripts
from youtube_lesson_planner.nodes.learning_objectives import (
    generate_learning_objectives,
)
from youtube_lesson_planner.nodes.query_rewriter import rewrite
from youtube_lesson_planner.nodes.search_videos import search_youtube
from youtube_lesson_planner.schemas import AgentState


# Define nodes
def create_vectorstore(state: AgentState) -> AgentState:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=512)
    qdrant_client = QdrantClient(
        location=":memory:",
    )
    qdrant_client.create_collection(
        "youtube_transcripts", {"size": 512, "distance": "Cosine"}
    )

    vectorstore = Qdrant(
        client=qdrant_client,
        collection_name="youtube_transcripts",
        embeddings=embeddings,
    )

    return {
        "vectorstore": vectorstore,
    }


def learning_objectives(state: AgentState) -> AgentState:
    query = state["original_query"]

    objectives = generate_learning_objectives(query)

    return {
        "learning_objectives": objectives,
    }


def rewrite_query(state: AgentState) -> AgentState:
    query = state["original_query"]
    objectives = state["learning_objectives"]

    rewritten_query = rewrite(query, objectives)

    return {
        "rewritten_query": rewritten_query.optimized_query,
    }


def search(state: AgentState) -> AgentState:
    optimized_query = state["rewritten_query"]
    videos = search_youtube(optimized_query, max_results=10)

    return {
        "videos": videos,
    }


def transcripts(state: AgentState) -> AgentState:
    videos = state["videos"]
    vectorstore = state["vectorstore"]

    _ = get_transcripts(list(videos.values()), vectorstore)

    return {"transcripts_status": True}


def generate(state: AgentState) -> AgentState:
    query = state["original_query"]
    objectives = state["learning_objectives"]
    vectorstore = state["vectorstore"]

    lesson_plan = generate_plan(query, objectives, vectorstore)

    return {
        "lesson_plan": lesson_plan,
    }


def create_graph():
    # Define workflow
    workflow = StateGraph(AgentState)
    workflow.add_node("make_vectorstore", create_vectorstore)
    workflow.add_node("objectives", learning_objectives)
    workflow.add_node("rewrite_query", rewrite_query)
    workflow.add_node("search", search)
    workflow.add_node("transcripts", transcripts)
    workflow.add_node("generate", generate)

    workflow.set_entry_point("make_vectorstore")

    # Define edges
    workflow.add_edge("make_vectorstore", "objectives")
    workflow.add_edge("objectives", "rewrite_query")
    workflow.add_edge("rewrite_query", "search")
    workflow.add_edge("search", "transcripts")
    workflow.add_edge("transcripts", "generate")
    workflow.add_edge("generate", END)

    graph = workflow.compile(debug=True)

    return graph
