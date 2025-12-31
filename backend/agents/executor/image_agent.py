import os
import asyncio
import httpx
import openai
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")


# ---------------------------
# LLM helper
# ---------------------------
async def generate_image_queries(slide_text: str, goal: str) -> list[str]:
    prompt = f"""
You are an expert at selecting Unsplash image search keywords.

Slide content:
{slide_text}

Overall topic:
{goal}

Generate 3–5 short Unsplash search queries (2–4 words).
Return ONE query per line.
No numbering, no explanation.
"""

    try:
        response = await asyncio.to_thread(
            lambda: openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=80,
                temperature=0.3,
            )
        )

        return [
            q.strip()
            for q in response.choices[0].message.content.split("\n")
            if q.strip()
        ]

    except Exception:
        return [goal]


# ---------------------------
# Unsplash helper
# ---------------------------
async def fetch_image_url(query: str) -> str:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.unsplash.com/photos/random",
                params={
                    "query": query,
                    "client_id": UNSPLASH_ACCESS_KEY,
                    "orientation": "landscape",
                    "count": 1,
                },
                timeout=10,
            )

            data = response.json()

            if isinstance(data, list) and data and "urls" in data[0]:
                return data[0]["urls"]["regular"]

            return None

        except Exception:
            return None


# ---------------------------
# MAIN IMAGE AGENT
# ---------------------------
async def image_agent(input_data: dict) -> dict:
    """
    LangGraph-style image agent.
    Pulls slide content from shared state.
    """

    state = input_data.get("state", {})
    goal = input_data.get("goal", "")

    # ✅ IMPORTANT FIX
    slide_content = state.get("content_agent", "")

    num_slides = state.get("num_slides", 14)

    slides = [
        line.strip()
        for line in slide_content.split("\n")
        if line.strip()
    ][:num_slides]

    results = {}

    for idx, slide_text in enumerate(slides, 1):
        queries = await generate_image_queries(slide_text, goal)

        image_url = None
        for query in queries:
            image_url = await fetch_image_url(query)
            if image_url:
                break

        # store None when no valid image found
        results[f"slide_{idx}"] = image_url

    return results