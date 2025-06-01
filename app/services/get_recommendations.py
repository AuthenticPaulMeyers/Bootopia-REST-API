from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("GITHUB_TOKEN"),
)

def get_mood_recommendations(mood):
        
        response = client.chat.completions.create(
        model="gpt-4o",
        temperature=1,
        max_tokens=4096,
        top_p=1,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """You are an AI agent called JessAI. You recommend books based on user moods for the day. You do not recommend any information outside of books. The books are legally provided and are free and downloadable from public domains. Use https://www.gutenberg.org/cache/epub/. Use the following JSON format:

                {
                    "reasoning": "reasoning for the books recommended based on the user mood",
                    "books": [
                        {
                            "title": "book title",
                            "author": "author of the book",
                            "description": "description of the book",
                            "file_url": "the book file url",
                            "genre": "the genre of the book",
                            "cover_image_url": "image cover link",
                            "year_pusblished": "year of publication",
                            "isbn": "the ISBN of the book (if any)"
                        }
                    ]
                }"""
            },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Today am feeling {mood}. Give me five books you'd recommend for me to read."
                            }
                        ]
                    },
                ],

            )

        response_message = response.choices[0].message
        content = response_message.content

        return json.loads(content)