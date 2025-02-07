from flask import Blueprint, jsonify, request
from app.models.responses import success_response, error_response
from app.services.question_service import QuestionService
from app.services.training_service import TrainingService
from app.api.validators.question_validators import QuestionValidator
import json

question_bp = Blueprint('questions', __name__)

@question_bp.route('/collections')
def get_collections():
    try:
        collections = QuestionService.get_collections()
        return jsonify(success_response(collections))
    except Exception as e:
        return jsonify(error_response(str(e))), 500

@question_bp.route('/questions')
def get_questions():
    try:
        questions = QuestionService.get_questions()
        return jsonify(success_response(questions))
    except Exception as e:
        return jsonify(error_response(str(e))), 500

@question_bp.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        error = QuestionValidator.validate_question_request(data)
        if error:
            return jsonify(error_response(error)), 400

        answer = QuestionService.ask_question(question=data['question'])
        return jsonify(success_response(answer))
    except Exception as e:
        return jsonify(error_response(str(e))), 500

@question_bp.route('/generate-sql', methods=['POST'])
def generate_sql():
    try:
        data = request.get_json()
        error = QuestionValidator.validate_question_request(data)
        if error:
            return jsonify(error_response(error)), 400

        sql = QuestionService.generate_sql_query(question=data['question'])
        return jsonify(success_response(sql))
    except Exception as e:
        return jsonify(error_response(str(e))), 500

@question_bp.route('/run-sql', methods=['POST'])
def run_sql():
    try:
        data = request.get_json()
        error = QuestionValidator.validate_sql_request(data)
        if error:
            return jsonify(error_response(error)), 400

        df = QuestionService.execute_sql(sql=data['sql'])
        return jsonify(success_response(json.loads(df.head(10).to_json(orient="records"))))
    except Exception as e:
        return jsonify(error_response(str(e))), 500 

@question_bp.route('/training-data')
def get_training_data():
    try:
        data = TrainingService.get_training_data()
        return jsonify(success_response(json.loads(data.head(10).to_json(orient="records"))))
    except Exception as e:
        return jsonify(error_response(str(e))), 500

@question_bp.route('/remove-all-training-data', methods=['DELETE'])
def remove_all_training_data():
    try:
        TrainingService.remove_all_training_data()
        return jsonify(success_response("Training data removed"))
    except Exception as e:
        return jsonify(error_response(str(e))), 500

@question_bp.route('/add-training-data', methods=['POST'])
def add_training_data():
    try:
        data = request.get_json()
        error = QuestionValidator.validate_training_data_request(data)
        if error:
            return jsonify(error_response(error)), 400

        TrainingService.add_training_data(
            question=data['question'],
            sql=data['sql'],
            ddl=data['ddl']
        )
        return jsonify(success_response("Training data added"))
    except Exception as e:
        return jsonify(error_response(str(e))), 500

@question_bp.route('/ingest-training-data-from-file', methods=['POST'])
def ingest_training_data_from_file():
    try:
        result = TrainingService.ingest_training_data_from_file('app/training_data/question-sql-pairs.json')
        return jsonify(success_response(result))
    except Exception as e:
        return jsonify(error_response(str(e))), 500
