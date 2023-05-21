from flask import Flask, request, jsonify
from flask_cors import CORS

import openai
import os

import logging


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()

app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.INFO)


@app.route("/members")
def members():
    app.logger.info("SEFSDFDF")
    return {"members": ["Member 1", "Member 2"]}


@app.route("/completions", methods=['POST'])
def completion():
    data = request.get_json()
    text_input = data.get('text', None)
    # response = openai.Completion.create(
    #     engine="text-davinci-002",
    #     prompt=text_input,
    #     temperature=0.5,
    #     max_tokens=256,
    #     top_p=1.0,
    #     frequency_penalty=0.0,
    #     presence_penalty=0.0
    #     )
    
    # app.logger.info("Call to OpenAI Made")
    # app.logger.info(response['choices'][0]['text'])
    # return response['choices'][0]['text']
    return jsonify({'text': text_input}), 200  # OK

# curl -X POST -H "Content-Type: application/json" -d '{"text":"Hello, Flask!"}' http://127.0.0.1:5000/completion

if __name__ == "__main__":
    app.run(debug=True)