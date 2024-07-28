from CodeAssistant.codeHelpAI import codeHelp
from JobSearch.query import search_jobs

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Home route'

@app.route('/code-assistant', methods=['POST'])
def codeAssistant():
    data=request.json
    language = data.get('language')
    code = data.get('code')

    if not language or not code:
        return jsonify({'error': 'Invalid input, missing language or code'}), 400

    response=codeHelp(language,code)
    return jsonify({'response': response})

@app.route('/job-search', methods=['POST'])
def llm_response():
    data=request.json
    query = data.get('query')
    
    if not query:
        return jsonify({'error': 'Invalid input, missing query'}), 400


    response=search_jobs(query)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)


