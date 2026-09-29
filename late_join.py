import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_late_join_catchup(transcript):
    prompt = f"""
You are a Meeting Intelligence Agent helping someone who joined a meeting late.

Analyze the part of the meeting that happened before they joined.

Give the late participant a quick catch-up with exactly these sections:

1. What You Missed
- Briefly explain the important discussion.

2. Decisions Already Made
- List decisions that were actually agreed upon.
- Do not treat suggestions or opinions as decisions.

3. Important Points
- List information the participant should know.

4. What You Need to Know Now
- Give the most important context they need to follow the rest of the meeting.

Keep it concise and easy to understand.

Meeting transcript before the participant joined:
{transcript}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content