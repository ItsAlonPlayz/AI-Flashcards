import os
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("Missing OPENROUTER_API_KEY. Check your .env file!")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY.strip().strip('"').strip("'"),
)


def generate_flashcard_text(raw_note):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": "You are a flashcard generator. Convert user input into a single line formatted strictly as 'Term : Definition'.",
            },
            {"role": "user", "content": raw_note},
        ],
        extra_body={"reasoning": {"effort": "none"}},
        max_tokens=60,
    )

    message = response.choices[0].message
    content = message.content or ""

    # Parse out the 'Term : Definition' pair even if the model surrounds it with extra text
    match = re.search(r"([^:\n]+?\s*:\s*[^:\n]+)", content)
    if match:
        return match.group(1).strip()

    return content.strip()


def parse_notes(notes_list):
    flashcards = []

    for note in notes_list:
        colon_index = note.find(":")
        if colon_index != -1:
            front = note[:colon_index].strip()
            back = note[colon_index + 1 :].strip()
            flashcards.append({"front": front, "back": back})
    return flashcards