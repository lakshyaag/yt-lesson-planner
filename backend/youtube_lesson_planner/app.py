import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from youtube_lesson_planner.graph import create_graph
from youtube_lesson_planner.schemas import RequestModel

app = FastAPI(
    title="YouTube Lesson Planner API",
    description="A tool to generate lesson plans from YouTube videos.",
    version="0.0.2",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

graph = create_graph()


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the YouTube Lesson Planner API. Please visit /docs for more information."
    }


@app.post("/learn/")
def build_plan(user_input: RequestModel):
    response = graph.invoke({"original_query": user_input})

    output = {
        "original_query": response["original_query"],
        "learning_objectives": response["learning_objectives"],
        "videos": response["videos"],
        "lesson_plan": response["lesson_plan"],
    }

    return output


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)
