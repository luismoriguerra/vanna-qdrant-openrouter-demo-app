from flask import Blueprint, jsonify, request
from app.services.vanna_service import vanna_service
from app.models.responses import success_response, error_response
import json

question_bp = Blueprint('questions', __name__)

@question_bp.route('/collections')
def get_collections():
    try:
        collections = vanna_service._client.get_collections()
        return jsonify(success_response(collections.dict()))
    except Exception as e:
        return jsonify(error_response(str(e))), 500

@question_bp.route('/questions')
def get_questions():
    try:
        questions = vanna_service.get_questions()
        return jsonify(success_response(questions))
    except Exception as e:
        return jsonify(error_response(str(e))), 500

@question_bp.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify(error_response("Question is required in request body")), 400

        answer = vanna_service.ask_question(question=data['question'])
        return jsonify(success_response(answer))
    except Exception as e:
        return jsonify(error_response(str(e))), 500

@question_bp.route('/generate-sql', methods=['POST'])
def generate_sql():
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify(error_response("Question is required in request body")), 400

        sql = vanna_service.generate_sql_query(question=data['question'])
        return jsonify(success_response(sql))
    except Exception as e:
        return jsonify(error_response(str(e))), 500

@question_bp.route('/run-sql', methods=['POST'])
def run_sql():
    try:
        data = request.get_json()
        if not data or 'sql' not in data:
            return jsonify(error_response("SQL query is required in request body")), 400

        df = vanna_service.execute_sql(sql=data['sql'])
        return jsonify(success_response(json.loads(df.head(10).to_json(orient="records"))))
    except Exception as e:
        return jsonify(error_response(str(e))), 500 