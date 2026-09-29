import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

BANK_ID = "meeting-minds"


def get_client():
    return Hindsight(
        base_url="https://api.hindsight.vectorize.io",
        api_key=os.getenv("HINDSIGHT_API_KEY")
    )


def save_meeting_memory(meeting_information):
    client = get_client()

    client.retain(
        bank_id=BANK_ID,
        content=meeting_information
    )

    return "Meeting memory saved successfully!"


def recall_meeting_memory(query):
    client = get_client()

    result = client.recall(
        bank_id=BANK_ID,
        query=query
    )

    return result