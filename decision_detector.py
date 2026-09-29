import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def detect_decisions(transcript):
    prompt = f"""
You are a Meeting Intelligence Agent.

Analyze this meeting transcript and identify ONLY decisions that were
actually agreed upon by the team.

Do NOT include:
- suggestions
- opinions
- questions
- possibilities
- topics that were only discussed

For each confirmed decision, provide:
- Decision
- Context
- Who agreed, if mentioned

If there are no confirmed decisions, say:
"No confirmed decisions found."

Meeting transcript:
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