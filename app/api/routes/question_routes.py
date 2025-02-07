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

@question_bp.route('/training-data')
def get_training_data():
    try:
        data = vanna_service.get_training_data()
        return jsonify(success_response(json.loads(data.head(10).to_json(orient="records"))))
    except Exception as e:
        return jsonify(error_response(str(e))), 500


@question_bp.route('/remove-all-training-data', methods=['DELETE'])
def remove_all_training_data():
    try:
        data = vanna_service.get_training_data()
        for index, row in data.iterrows():
            vanna_service.remove_training_data(id=row['id'])
        return jsonify(success_response("Training data removed"))
    except Exception as e:
        return jsonify(error_response(str(e))), 500

@question_bp.route('/add-training-data', methods=['POST'])
def add_training_data():
    try:
        data = request.get_json()
        vanna_service.add_training_data(question=data['question'], sql=data['sql'], ddl=data['ddl'])
        return jsonify(success_response("Training data added"))
    except Exception as e:
        return jsonify(error_response(str(e))), 500

@question_bp.route('/ingest-training-data-from-file', methods=['POST'])
def ingest_training_data_from_file():
    try:
        with open('app/training_data/question-sql-pairs.json', 'r') as file:
            training_data = json.load(file)
            
        success_count = 0
        error_count = 0
        errors = []
        
        for item in training_data:
            try:
                # Get values with None as default if missing
                question = item.get('question')
                sql = item.get('sql')
                ddl = item.get('ddl')
                
                # Add training data if at least one field is present
                if any([question, sql, ddl]):
                    vanna_service.train(
                        question=question,
                        sql=sql,
                        ddl=ddl
                    )
                    success_count += 1
                else:
                    error_count += 1
                    errors.append("Item has no valid fields (question, sql, or ddl)")
            except Exception as e:
                error_count += 1
                errors.append(str(e))
                
        result = {
            "success_count": success_count,
            "error_count": error_count,
            "errors": errors[:10] if errors else []  # Return first 10 errors if any
        }
        
        return jsonify(success_response(result))
    except Exception as e:
        return jsonify(error_response(str(e))), 500
