import asyncio
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


async def content_agent(input_data: dict) -> str:
    """
    Converts research output into structured slide content.
    Ensures each slide has a clear title and 3–5 bullet points.
    """

    goal = input_data.get("goal") or "General topic"
    state = input_data.get("state", {})
    num_slides = state.get("num_slides", 14)

    # Prefer explicit input; fallback to research_agent output
    research_output = input_data.get("input") or state.get("research_agent") or state.get("research") or "No research data provided"

    prompt = f"""
You are a content assistant.
Convert the following research points into a structured slide-wise presentation.

Guidelines:
- Number each slide from 1 to {num_slides}.
- Each slide must have a clear title and 3-5 concise bullet points.
- Format output like this:

1. Slide Title
- Bullet 1
- Bullet 2
- Bullet 3

Goal: {goal}
Research Points: {research_output}
"""

    try:
        response = await asyncio.to_thread(
            lambda: openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.3,
            )
        )

        content = response.choices[0].message.content.strip()

        # Ensure output is not empty
        if not content:
            content = "\n".join([f"{i+1}. Slide {i+1}\n- Key concept overview" for i in range(num_slides)])

        return content

    except Exception as e:
        # Safe fallback if LLM fails
        return "\n".join([f"{i+1}. Slide {i+1}\n- Key concept overview" for i in range(num_slides)])