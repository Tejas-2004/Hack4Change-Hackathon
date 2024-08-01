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
        f"- Intro to the difficulty of the topic, all the concepts of the language which fall under{difficulty}difficulty, syntaxes and important points.\n"
        f"- {questions} coding questions that cover all the concepts discussed above.\n"
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


@app.route('/generate-badge',methods=['POST'])
def badge_gen():
    data = request.json
    

if __name__ == '__main__':
    app.run(host='localhost', port=5868, debug=True)
