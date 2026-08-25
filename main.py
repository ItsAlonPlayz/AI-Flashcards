import os
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    try:
        import streamlit as st

        API_KEY = st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        pass

if not API_KEY:
    raise ValueError(
        "Missing OPENROUTER_API_KEY! Set it in your .env file or Streamlit Cloud Secrets."
    )

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
                "content": (
                    "You are a flashcard generator. Convert user input into flashcards.\n"
                    "RULES:\n"
                    "1. Only create flashcards for core, distinct facts. Do NOT split a single concept into micro-facts.\n"
                    "2. Output format must strictly be 'Term : Definition' on each line.\n"
                    "3. Do not include intro text, numbering, or bullet points."
                ),
            },
            {"role": "user", "content": raw_note},
        ],
        extra_body={"reasoning": {"effort": "none"}},
        max_tokens=300,
    )

    message = response.choices[0].message
    return message.content or ""


def parse_notes(raw_output):
    flashcards = []
    lines = raw_output.strip().split("\n")

    for line in lines:
        match = re.search(r"([^:\n]+?\s*:\s*[^:\n]+)", line)
        if match:
            pair = match.group(1)
            colon_index = pair.find(":")
            front = pair[:colon_index].strip()
            back = pair[colon_index + 1 :].strip()
            if front and back:
                flashcards.append({"front": front, "back": back})

    return flashcards