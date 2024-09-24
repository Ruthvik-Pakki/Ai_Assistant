import os
import openai
from config import apikey

openai.api_key = apikey

response = openai.Completion.create(
  model="gpt-3.5-turbo-instruct-0914",
  prompt="what is the value of one Bitcoin in USD",
  temperature=1,
  max_tokens=2048,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)


