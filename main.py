import os
from flask import Flask, jsonify

from vanna.openai import OpenAI_Chat
from vanna.qdrant import Qdrant_VectorStore
from qdrant_client import QdrantClient, models
import json
import os
from dotenv import load_dotenv

load_dotenv()

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL") or exit("QDRANT_API_URL environment variable not set"),
    api_key=os.getenv("QDRANT_API_KEY") or exit("QDRANT_KEY environment variable not set"),
)

app = Flask(__name__)


@app.route('/')
def hello():
    return jsonify({
        "message": "Hello world, welcome to Railway!",
        "status": "success"
    })

@app.route('/collections')
def get_collections():
    try:
        collections = qdrant_client.get_collections()
        return jsonify({
            "status": "success",
            "collections": collections.dict()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500