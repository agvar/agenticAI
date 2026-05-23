from openai import OpenAI
import os

api_key= os.environ.get('OpenAIKey')
print(api_key)
client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model = 'gpt-4o-mini',
    messages =[
        {"role":"system", "content":"You are a data engineering expert."},
        {"role":"user", "content":"What causes a pipeline to fail silently?"}
    ]
)

print(response)