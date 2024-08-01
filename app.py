from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

app = Flask(__name__)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a chatbot"),
        ("human", "Question:{question}")
    ]
)

output_parser = StrOutputParser()
chain = prompt | llm | output_parser

def query_llm(topic, difficulty, questions):
    query = (
        f"Generate educational content for the programming language topic {topic} with difficulty '{difficulty}'. "
        f"The content should include:\n"
        f"- Intro to the difficulty of the topic, concepts which will be covered, syntaxes and important points.\n"
        f"- {questions} coding questions that cover different concepts related to the topic.\n"
        f"- Each question should have the following fields: question, question_id, concept_introduction and syntax, and expected_output.\n"
        f"DO NOT SKIP ANY QUESTION! EVERY QUESTION TO BE IN THE STRUCTURE PROVIDED BELOW\n\n"
        f"The response should be structured as follows:\n"
        f"{{\n"
        f"  'topic': '{topic}',\n"
        f"  'introduction': '...',\n"
        f"  'data': [\n"
        f"    {{\n"
        f"      'question': '...',\n"
        f"      'concept_introduction': '...',\n"
        f"      'solution': '...',\n"
        f"      'expected_output': '...'\n"
        f"    }},\n"
        f"    ...\n"
        f"  ]\n"
        f"}}"
    )
    response = chain.invoke({'question': query})
    return response

def query_llm2(codes):
    query = (
        f"Analyze the following list of code snippets:\n{codes}\n\n"
        f"Identify the programming language or framework used and the topics covered. The response should be structured as follows:\n"
        
        f"  'Title': '...',\n"
        f"  'Topics': [...]"
       
    )
    response = chain.invoke({'question': query})
    return response

@app.route('/generate-skill', methods=['POST'])
def generate_skill():
    data = request.json
    topic = data.get('topic')
    difficulty = data.get('difficulty')
    questions = data.get('questions')
    
    if not topic or not difficulty or not questions:
        return jsonify({'error': 'Topic, difficulty, and questions are required fields.'}), 400

    result = query_llm(topic, difficulty, questions)
    return jsonify(result)

@app.route('/generate-badge', methods=['POST'])
def badge_gen():
    data = request.json
    codes = data.get('codes')
    
    if not codes or not isinstance(codes, list):
        return jsonify({'error': 'Codes must be provided as a list of strings.'}), 400

    result = query_llm2(codes)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
