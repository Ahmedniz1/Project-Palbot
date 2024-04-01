import os

from openai import OpenAI

from flask import Flask, jsonify, request
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

from utils import save_embeddings,create_collection,response_query,create_data_file

app = Flask(__name__)

load_dotenv()
collection = create_collection()
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
client = OpenAI()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')
@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify if the application is running.
    Returns a JSON response with status 'ok'.
    """
    response_data = {"status": "ok"}
    return jsonify(response_data),200
@app.route('/scrape_data', methods = ['GET'])
def scrape_data():
    create_data_file()
    response_data = {"status": "Data Successfully scraped"}
    return jsonify(response_data),200

@app.route('/create_embeddings', methods=['POST'])
def create_embeddings():
    global collection, model
    data = request.json
    save_embeddings(data['path'],collection,model)
    response_data = {'message': 'Embeddings saved successfully'}
    return jsonify(response_data), 200

@app.route('/query',methods = ['POST'])
def query():
    global collection, model
    data = request.json
#    print(model)
    response = response_query(data['query'],collection,model,client)
    response_data = {'response': response}
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(debug=True)