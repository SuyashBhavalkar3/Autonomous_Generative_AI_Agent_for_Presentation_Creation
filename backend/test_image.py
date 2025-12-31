import asyncio
from agents.executor.image_agent import image_agent



async def main():
    # Fake state simulating what content_agent returns
    input_data = {
        "goal": "Photosynthesis",
        "state": {
            "num_slides": 3,
            "content_agent": """1. Overview of Photosynthesis
- Converts sunlight into chemical energy
- Occurs in chloroplasts
2. Light-Dependent Reactions
- Produces ATP and NADPH
- Oxygen is released
3. Calvin Cycle
- Uses ATP and NADPH
- Converts CO2 into glucose"""
        }
    }

    results = await image_agent(input_data)
    for slide, url in results.items():
        print(slide, url)

asyncio.run(main())
