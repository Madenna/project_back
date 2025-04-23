import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def get_ai_reply(messages):
    system_msg = {
        "role": "system",
        "content": "You're a kind, helpful assistant named KomekAI. You support parents of special needs children on the BalaSteps platform."
    }

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[system_msg] + messages,
    )
    return response.choices[0].message["content"]