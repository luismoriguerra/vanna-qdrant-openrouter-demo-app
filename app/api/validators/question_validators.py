from flask import Request
from typing import Dict, Any, Optional

class QuestionValidator:
    @staticmethod
    def validate_question_request(data: Dict[str, Any]) -> Optional[str]:
        if not data or 'question' not in data:
            return "Question is required in request body"
        return None

    @staticmethod
    def validate_sql_request(data: Dict[str, Any]) -> Optional[str]:
        if not data or 'sql' not in data:
            return "SQL query is required in request body"
        return None

    @staticmethod
    def validate_training_data_request(data: Dict[str, Any]) -> Optional[str]:
        if not data or not all(key in data for key in ['question', 'sql', 'ddl']):
            return "Question, SQL, and DDL are required in request body"
        return None 