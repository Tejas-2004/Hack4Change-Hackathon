import os
from groq import Groq
# import datetime

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content



def codeHelp(language,input_code):
    
    
    context_template = read_file('CodeAssistant/contextTemplate.md')
    # input_file=read_file('code_input.txt')
    
    context = context_template.replace('{{language}}', language).replace('{{prompt}}', input_code)

    
    
    
    
    client = Groq(api_key=os.getenv('groq_api'))
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
             {
            "role": "system",
            "content": "You are a coding assistant designed to help users with their coding tasks. Your main tasks include analyzing code for errors, suggesting improvements, providing debugging assistance, and offering coding advice. You can assist with multiple programming languages and ensure that the user's code is efficient, clean, and follows best practices."

             },
            {
                "role": "user",
                "content": context
            }
        ],
        temperature=0,
        max_tokens=2500,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    
    
    response_content = ""
    for chunk in completion:
        response_content += chunk.choices[0].delta.content or ""

    return response_content


    # timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    # output_file_name=f"codeHelp_response {timestamp}.md"
    # with open(output_file_name,'w') as output_file:
    #     for chunk in completion:
    #         output_file.write(chunk.choices[0].delta.content or "")
