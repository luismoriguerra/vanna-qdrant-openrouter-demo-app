import json
import pandas as pd
from typing import Dict, List, Any
from app.services.vanna_service import vanna_service

class TrainingService:
    @staticmethod
    def get_training_data() -> pd.DataFrame:
        return vanna_service.get_training_data()

    @staticmethod
    def remove_all_training_data() -> None:
        data = vanna_service.get_training_data()
        for index, row in data.iterrows():
            vanna_service.remove_training_data(id=row['id'])

    @staticmethod
    def add_training_data(question: str, sql: str, ddl: str) -> None:
        vanna_service.add_training_data(question=question, sql=sql, ddl=ddl)

    @staticmethod
    def ingest_training_data_from_file(file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r') as file:
            training_data = json.load(file)
            
        success_count = 0
        error_count = 0
        errors: List[str] = []
        
        for item in training_data:
            try:
                question = item.get('question')
                sql = item.get('sql')
                ddl = item.get('ddl')
                
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
                
        return {
            "success_count": success_count,
            "error_count": error_count,
            "errors": errors[:10] if errors else []
        } 