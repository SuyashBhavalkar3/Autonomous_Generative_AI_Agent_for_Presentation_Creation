import asyncio
from agents.executor.executor_agent import GraphExecutor
from agents.planner.schemas import GraphSpec, NodeSpec
from agents.registry import AGENT_REGISTRY

# Register all agents
from agents.executor.research_agent import research_agent
from agents.executor.content_agent import content_agent
from agents.executor.image_agent import image_agent
from agents.executor.slide_agent import slide_agent

AGENT_REGISTRY.update({
    "research_agent": research_agent,
    "content_agent": content_agent,
    "image_agent": image_agent,
    "slide_agent": slide_agent
})

async def main():
    # Define your DAG
    nodes = {
        "research_agent": NodeSpec(agent="research_agent", input=None),
        "content_agent": NodeSpec(agent="content_agent", input=None),
        "image_agent": NodeSpec(agent="image_agent", input=None),
        "slide_agent": NodeSpec(agent="slide_agent", input=None)
    }

    # Define dependencies: research -> content -> image -> slide
    edges = [
        ("research_agent", "content_agent"),
        ("content_agent", "image_agent"),
        ("content_agent", "slide_agent"),  # slide_agent needs content
        ("image_agent", "slide_agent")     # slide_agent needs images
    ]
    
    graph = GraphSpec(
    nodes=nodes,
    edges=edges,
    entry_nodes=["research_agent"],
    goal="Introduction to Medical Sciences",
    num_slides=4
    )


    executor = GraphExecutor()
    final_state = await executor.execute(graph)

    slides = final_state.get("slide_agent", {}).get("slides", [])

    for idx, slide in enumerate(slides, 1):
        print(f"Slide {idx}:")
        print(f"Title: {slide['title']}")
        print("Bullets:")
        for bullet in slide["bullets"]:
            print(f" - {bullet}")
        print(f"Image URL: {slide['image_url']}\n")
asyncio.run(main())
