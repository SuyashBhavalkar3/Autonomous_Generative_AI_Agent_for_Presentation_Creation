# research_agent.py
import asyncio
import openai
import os
import dotenv

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def research_agent(input_data):
    """
    input_data is expected to be a dict:
    {
        "goal": str,
        "previous_output": str or None,
        "action": str
    }
    """
    topic = input_data.get("goal") or "General topic"
    prompt = f"""
    You are a research assistant. Summarize key points about the following topic:
    Topic: {topic}
    Provide concise points suitable for slide content.
    """
    try:
        response = await asyncio.to_thread(
            lambda: openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.5,
            )
        )
        # Always return string
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"