import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def detect_changes(previous_meeting, current_meeting):
    prompt = f"""
You are a Meeting Intelligence Agent.

Compare the previous meeting with the current meeting.

Identify important changes in:
- decisions
- deadlines
- dates
- plans
- responsibilities

Do not report something as changed just because the wording is different.

Return exactly these sections:

1. Decisions From Previous Meeting
2. Decisions From Current Meeting
3. What Changed
4. What Stayed the Same

If there are no important changes, say:
"No important changes detected."

PREVIOUS MEETING:
{previous_meeting}

CURRENT MEETING:
{current_meeting}
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