import asyncio
from agents.executor.slide_agent import slide_agent

async def main():
    # Mock DAG state
    state = {
        "content_agent": """1. Introduction to AI
2. History of AI
3. AI Applications
4. Future of AI""",
        "image_agent": {
            "slide_1": "https://example.com/image1.jpg",
            "slide_2": "https://example.com/image2.jpg",
            "slide_3": "https://example.com/image3.jpg",
            "slide_4": "https://example.com/image4.jpg"
        }
    }

    input_data = {
        "goal": "AI Presentation",
        "state": state
    }

    slides = await slide_agent(input_data)

    # Print the final slides
    for idx, slide in enumerate(slides["slides"], 1):
        print(f"Slide {idx}:")
        print(f"Content: {slide['content']}")
        print(f"Image URL: {slide['image_url']}\n")

asyncio.run(main())