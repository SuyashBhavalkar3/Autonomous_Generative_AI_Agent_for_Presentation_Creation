import asyncio
import webbrowser
from agents.executor.image_agent import image_agent  # adjust import path if needed

async def test_image_agent():
    input_data = {
        "goal": "Artificial Intelligence in Healthcare",
        "state": {"num_slides": 5},
        "input": """AI in diagnostics
AI in treatment
AI in patient monitoring
AI in drug discovery
AI in hospital management"""
    }

    result = await image_agent(input_data)

    print("\nFetched Images:")
    for slide, url in result.items():
        print(f"{slide}: {url}")
        # Open each image in the default browser
        if not url.startswith("ImageAgentError"):
            webbrowser.open(url)

if __name__ == "__main__":
    asyncio.run(test_image_agent())