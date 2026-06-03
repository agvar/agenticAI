from openai import OpenAI
from pydantic import BaseModel
from typing import Literal,List
import os

api_key = os.environ.get('OpenAIKey')

class PipelineIncident(BaseModel):
    pipeline_name: str
    severity : Literal['critical','medium','low']
    error_type: str
    affected_tables : List[str]
    needs_immediate_attention : bool

def analyze_log_entry(log_text:str) ->PipelineIncident:
    client = OpenAI(api_key=api_key)
    messages =[]
    model= 'gpt-4o-mini'
    system_prompt = {"role":"system", "content":"You are a data engineering expert.Analyse the log text "}
    log_prompt = {"role":"user", "content":log_text}
    messages.append(system_prompt)
    messages.append(log_prompt)
    response = client.chat.completions.parse(
        model=model,
        messages = messages,
        response_format=PipelineIncident
    )
    report = response.choices[0].message.parsed
    print(report.pipeline_name)
    print(report.severity)
    print(report.error_type)
    print(report.affected_tables)
    print(report.needs_immediate_attention)
    print("model_dump",report.model_dump)

if __name__=="__main__":
    analyze_log_entry("the pipeline completed loading the Datastore tables")
    analyze_log_entry("the pipeline ignored 2 records")
    analyze_log_entry("the pipeline failed because the primary key is NULL")