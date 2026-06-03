from openai import OpenAI
import os

api_key= os.environ.get('OpenAIKey')

messages = []
client = OpenAI(api_key=api_key)
MODEL = 'gpt-4o-mini'
system_prompt = {"role":"system", "content":"You are a data engineering expert."}
user_prompt1 = {"role":"user", "content":"What is a data pipeline?"}
messages.append(system_prompt)
messages.append(user_prompt1)
print(messages)

response1 = client.chat.completions.create(model = MODEL,messages = messages)
messages.append({"role":"assistant","content":response1.choices[0].message.content})
user_prompt2 = {"role":"user", "content":"What causes it to fail?"}
messages.append(user_prompt2)
print(messages)

response2 = client.chat.completions.create(model = MODEL,messages = messages)
print(response2.choices[0].message.content)