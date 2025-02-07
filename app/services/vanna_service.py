from vanna.openai import OpenAI_Chat
from vanna.qdrant import Qdrant_VectorStore
from app.core.config import config
from app.core.database import qdrant_client
import pandas as pd
from app.services.openai_service import openai_client, openai_config

class VannaService(Qdrant_VectorStore, OpenAI_Chat):
    def __init__(self):
        Qdrant_VectorStore.__init__(self, config={'client': qdrant_client})
        OpenAI_Chat.__init__(self, client=openai_client, config=openai_config)
        self._connect_to_snowflake()

    def _connect_to_snowflake(self):
        self.connect_to_snowflake(**config.SNOWFLAKE_CONFIG)

    def get_questions(self) -> list:
        return self.generate_questions()

    def ask_question(self, question: str) -> str:
        return self.ask(question=question)

    def generate_sql_query(self, question: str) -> str:
        return self.generate_sql(question=question)

    def execute_sql(self, sql: str) -> pd.DataFrame:
        return self.run_sql(sql=sql)

    def get_training_data(self) -> pd.DataFrame:
        return super().get_training_data()

    def remove_training_data(self, id: str):
        return super().remove_training_data(id=id)

    def train(self, question: str, sql: str, ddl: str):
        return super().train(question=question, sql=sql, ddl=ddl)


vanna_service = VannaService()
