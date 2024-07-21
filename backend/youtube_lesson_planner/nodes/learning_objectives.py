from textwrap import dedent

from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
from youtube_lesson_planner.schemas import LearningObjectives, LearningObjectivesList

examples = [
    {
        "input": "I want to learn how to manage my time better.",
        "output": [
            LearningObjectives(
                index=1,
                objective="Identify and prioritize daily tasks using time management techniques.",
            ),
            LearningObjectives(
                index=2,
                objective="Implement strategies to minimize distractions and increase productivity.",
            ),
            LearningObjectives(
                index=3,
                objective="Create and maintain a personal schedule that balances work, study, and leisure.",
            ),
        ],
    },
    {
        "input": "I'm interested in understanding the basics of digital marketing.",
        "output": [
            LearningObjectives(
                index=1,
                objective="Define key concepts and terms in digital marketing.",
            ),
            LearningObjectives(
                index=2,
                objective="Identify different digital marketing channels and their uses.",
            ),
            LearningObjectives(
                index=3,
                objective="Develop a basic digital marketing strategy for a hypothetical business.",
            ),
        ],
    },
    {
        "input": "How can I improve my public speaking skills?",
        "output": [
            LearningObjectives(
                index=1,
                objective="Identify the key components of effective public speaking.",
            ),
            LearningObjectives(
                index=2,
                objective="Practice and apply techniques to reduce public speaking anxiety.",
            ),
            LearningObjectives(
                index=3,
                objective="Prepare and deliver a structured speech with confidence.",
            ),
        ],
    },
    {
        "input": "I want to learn the fundamentals of personal finance management.",
        "output": [
            LearningObjectives(
                index=1,
                objective="Create a personal budget and track expenses.",
            ),
            LearningObjectives(
                index=2,
                objective="Identify different types of savings and investment options.",
            ),
            LearningObjectives(
                index=3,
                objective="Develop a plan to reduce debt and build financial security.",
            ),
        ],
    },
    {
        "input": "I'm curious about the basics of coding in Python.",
        "output": [
            LearningObjectives(
                index=1,
                objective="Write basic Python scripts using variables, loops, and functions.",
            ),
            LearningObjectives(
                index=2,
                objective="Understand and apply basic data structures in Python, such as lists and dictionaries.",
            ),
            LearningObjectives(
                index=3,
                objective="Debug simple Python programs and handle errors.",
            ),
        ],
    },
]

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            dedent(
                """
                You are an agent that specializes in building learning curriculums based on user queries by searching YouTube. 
                
                Your task is to create comprehensive and engaging learning curriculums using relevant YouTube videos that match the user's query.
                
                Given the user's response to "What would you like to learn about today?", assess whether the question is simple enough to generate a quick response or if it's complex enough where a brief video-based curriculum would be more helpful. 
                - If it's simple, reply to the user's response.
                - If it's complex, generate a short list of up to 5 learning objectives suitable for an all-digital asynchronous learning platform. 
                
                Each objective should be:
                    - Clearly defined and outcome-focused on what the learner should achieve.
                    - Specific and measurable, utilizing Bloom's Taxonomy for actions like understanding, applying, and analyzing.
                    - Relevant and practical for adult learners, addressing real-world problems and applications.
                    - Structured to include engaging content, practice opportunities, and assessments, using a small set of curated YouTube videos that best align with the learning objectives.
                    - Aligned with principles of learning to enhance motivation, incorporating elements like self-direction, prior experience, and immediate applicability."""
            ),
        ),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)


def generate_learning_objectives(query: str) -> LearningObjectivesList:
    llm = ChatOpenAI(model="gpt-4o", temperature=0.5, streaming=False)

    chain = prompt | llm.with_structured_output(LearningObjectivesList)

    result = chain.invoke({"input": query})

    return result
