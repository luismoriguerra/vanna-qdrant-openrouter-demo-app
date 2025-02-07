import os
from flask import Flask, jsonify, request

from vanna.openai import OpenAI_Chat
from vanna.qdrant import Qdrant_VectorStore
from qdrant_client import QdrantClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL") or exit("QDRANT_API_URL environment variable not set"),
    api_key=os.getenv("QDRANT_API_KEY") or exit("QDRANT_KEY environment variable not set"),
)

class MyVanna(Qdrant_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        Qdrant_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

vn = MyVanna(config={
    'client': qdrant_client,
    'api_key': os.getenv("OPENAI_API_KEY") or exit("OPENAI_API_KEY environment variable not set"),
    'model': 'gpt-4o-mini',
})


database = "ANALYTICS"
# os.getenv("SNOWFLAKE_DATABASE") or exit("SNOWFLAKE_DATABASE environment variable not set"),
vn.connect_to_snowflake(
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE") or exit("SNOWFLAKE_WAREHOUSE environment variable not set"),
    account=os.getenv("SNOWFLAKE_ACCOUNT") or exit("SNOWFLAKE_ACCOUNT environment variable not set"),
    username=os.getenv("SNOWFLAKE_USER") or exit("SNOWFLAKE_USER environment variable not set"),
    password=os.getenv("SNOWFLAKE_PASSWORD") or exit("SNOWFLAKE_PASSWORD environment variable not set"),
    database=database,
    role=os.getenv("SNOWFLAKE_ROLE") or exit("SNOWFLAKE_ROLE environment variable not set"),
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

@app.route('/questions')
def get_questions():
    try:
        questions = vn.generate_questions()
        return jsonify({
            "status": "success",
            "questions": questions
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        # Get the question from the request body
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                "status": "error",
                "message": "Question is required in request body"
            }), 400

        # Get the answer using vn.ask
        answer = vn.ask(question=data['question'])
        
        return jsonify({
            "status": "success",
            "answer": answer
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/generate-sql', methods=['POST'])
def generate_sql():
    try:
        # Get the question from the request body
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                "status": "error",
                "message": "Question is required in request body"
            }), 400

        # Generate SQL using vn.generate_sql
        sql = vn.generate_sql(question=data['question'])
        
        return jsonify({
            "status": "success",
            "sql": sql
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/run-sql', methods=['POST'])
def run_sql():
    try:
        # Get the SQL query from the request body
        data = request.get_json()
        if not data or 'sql' not in data:
            return jsonify({
                "status": "error",
                "message": "SQL query is required in request body"
            }), 400

        # Run the SQL query using vn.run_sql
        df = vn.run_sql(sql=data['sql'])
        
        return jsonify({
            "status": "success",
            "data": json.loads(df.head(10).to_json(orient="records"))
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500