from langchain.vectorstores import Chroma
from src.helper import load_embedding
from dotenv import load_dotenv
import os
from src.helper import repo_injestion
from flask import Flask, render_template,jsonify, request
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain


app = Flask(__name__)

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings = load_embedding()
persist_directory = "db"

#loading persisted database from disk and use it
vectordb = Chroma(persist_directory = persist_directory,
embedding_fucntion = embeddings)

llm = ChatOpenAI()
memory = ConversationSummaryMemory(llm = llm, memory_key = "chat_history", return_messages=True)
qa = ConversationalRetrievalChain.from_llm(llm, retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k":8}), memory=memory)

@app.route('/', methods = ["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=["GET", "POST"])
def gitRepo():
    if(request.method == 'POST'):
        user_input = request.form['question']
        repo_injestion(user_input)
        os.system("python store_index.py")
    return jsonify({"response": str(user_inpt)})