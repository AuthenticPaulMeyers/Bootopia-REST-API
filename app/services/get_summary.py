from openai import OpenAI
from dotenv import load_dotenv
import os
from ..utils.get_text_from_pdf import extract_text_content

load_dotenv()

client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("GITHUB_TOKEN"),
)

MODEL="gpt-4.1"

def summarize_section(content):
    prompt = f"Summarize the following content clearly and concisely. Focus on separating topics or ideas where possible: {content}"
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes documents topic-by-topic with relevant content."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=1024
    )
    return response.choices[0].message.content.strip()