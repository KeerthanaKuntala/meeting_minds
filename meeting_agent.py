import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_summary(transcript):
    prompt = f"""
You are a Meeting Intelligence Agent.

Analyze the following meeting transcript.

Return:
1. A short meeting summary
2. The important points discussed
3. The decisions made

Keep the answer clear and concise.

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