"""Functions to send prompt and return output from OpenAI API."""

import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
