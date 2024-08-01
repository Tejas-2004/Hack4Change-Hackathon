from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import streamlit as st
template = """Question:{question}
Answer:Lets think step by step."""
prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="llama3.1")
chain = prompt |model
print(chain.invoke({"question":"""
Generate educational content for the programming language topic {topic} with difficulty '{difficulty}'. The content should include:
- Intro to the difficulty of the topic, concepts which will be covered, syntaxes and important points.
- {questions} coding questions that cover different concepts related to the topic.
- Each question should have the following fields: question, question_id, concept_introduction and syntax, and expected_output.
DO NOT SKIP ANY QUESTION! EVERY QUESTION TO BE IN THE STRUCTURE PROVIDED BELOW

The response should be structured as follows:
{
  'topic': '{topic}',
  'introduction': '...',
  'data': [
    {
      'question': '...',
      
      'concept_introduction': '...',
    'solution':'...',
      'expected_output': '...'
    },
    ...
  ]
}


"""}))