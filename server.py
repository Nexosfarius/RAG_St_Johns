from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import ConversationalRetrievalChain
import os

app = Flask(__name__)
CORS(app)

openai_api_key = 'your key'  # Replace with your actual OpenAI API key
pinecone_api_key = 'your key'  # same here

index_name = "capstone1"
embeddings = OpenAIEmbeddings(api_key=openai_api_key) 
vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings, pinecone_api_key=pinecone_api_key)

llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model_name='gpt-3.5-turbo',
    temperature=0.4
)

retriever = vectorstore.as_retriever()

chatbot = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    return_source_documents=True  
)

chat_history = []

@app.route('/ask', methods=['POST'])
def ask():
    global chat_history
    data = request.get_json()
    question = data.get('question')
    
    response = chatbot({"question": question, "chat_history": chat_history})
    answer = response['answer']

    chat_history.append((question, answer))  

    return jsonify({'answer': answer, 'chat_history': chat_history})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
