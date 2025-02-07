from typing import Dict, Any, List
import pandas as pd
from app.services.vanna_service import vanna_service

class QuestionService:
    @staticmethod
    def get_collections() -> Dict[str, Any]:
        collections = vanna_service._client.get_collections()
        return collections.dict()

    @staticmethod
    def get_questions() -> List[str]:
        return vanna_service.get_questions()

    @staticmethod
    def ask_question(question: str) -> str:
        return vanna_service.ask_question(question=question)

    @staticmethod
    def generate_sql_query(question: str) -> str:
        return vanna_service.generate_sql_query(question=question)

    @staticmethod
    def execute_sql(sql: str) -> pd.DataFrame:
        return vanna_service.execute_sql(sql=sql) 