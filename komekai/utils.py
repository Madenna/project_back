from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def analyze_prompt(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant giving medical suggestions."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content