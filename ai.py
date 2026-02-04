from openai import OpenAI
from prompts import SYSTEM_PROMPT

client = OpenAI()

def ai_process(session_id, message, history, metadata):
    user_prompt = f"""
Session ID: {session_id}

Conversation History:
{history}

Incoming Message:
{message}

Metadata:
{metadata}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content.strip()
