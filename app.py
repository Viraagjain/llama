import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from flask import Flask, request, render_template


load_dotenv()


os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

app = Flask(__name__)


def initialize():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Provide response to the user queries"),
            ("user", "Question: {question}")
        ]
    )
    

    llm = Ollama(model="llama3")
    output_parser = StrOutputParser()
    

    chain = prompt | llm | output_parser
    return chain


chain = initialize()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        input_text = request.form['input_text']
        if input_text:
            output = chain.invoke({'question': input_text})
            return render_template('index.html', input_text=input_text, output=output)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
