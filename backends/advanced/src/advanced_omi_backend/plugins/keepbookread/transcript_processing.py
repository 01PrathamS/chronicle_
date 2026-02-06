import os 
import json
from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def keepbookread_ai(transcript_chunk: str):
    """
    Takes a chunk of transcript from live group reading
    and returns extracted knowledge if needed.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are KeepBookRead, an intelligent reading companion plugin for group reading sessions.\n\n"
                    "You receive live or chunked transcriptions of spoken book reading and discussion.\n\n"
                    "Your job is to:\n"
                    "- Identify intent from the transcript\n"
                    "- ONLY respond when something useful needs to be noted\n"
                    "- Ignore normal reading, filler speech, or casual conversation\n\n"
                    "If necessary, extract and return:\n"
                    "1. Meaning of a word or phrase\n"
                    "2. Simple explanation of a complex sentence\n"
                    "3. Any mentioned reference (book, blog, website, author, paper)\n\n"
                    "If nothing important needs to be noted, return an empty JSON object.\n\n"
                    "Rules:\n"
                    "- Do NOT invent information\n"
                    "- Be concise\n"
                    "- Return output strictly in JSON"
                )
            },
            {
                "role": "user",
                "content": transcript_chunk
            }
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {}
