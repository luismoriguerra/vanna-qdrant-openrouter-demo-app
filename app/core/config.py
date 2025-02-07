import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Qdrant Configuration
    QDRANT_URL = os.getenv("QDRANT_URL") or exit("QDRANT_API_URL environment variable not set")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or exit("QDRANT_KEY environment variable not set")
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or exit("OPENAI_API_KEY environment variable not set")
    OPENAI_MODEL = 'gpt-4o-mini'
    
    # Snowflake Configuration
    SNOWFLAKE_CONFIG = {
        'warehouse': os.getenv("SNOWFLAKE_WAREHOUSE") or exit("SNOWFLAKE_WAREHOUSE environment variable not set"),
        'account': os.getenv("SNOWFLAKE_ACCOUNT") or exit("SNOWFLAKE_ACCOUNT environment variable not set"),
        'username': os.getenv("SNOWFLAKE_USER") or exit("SNOWFLAKE_USER environment variable not set"),
        'password': os.getenv("SNOWFLAKE_PASSWORD") or exit("SNOWFLAKE_PASSWORD environment variable not set"),
        'database': "ANALYTICS",
        'role': os.getenv("SNOWFLAKE_ROLE") or exit("SNOWFLAKE_ROLE environment variable not set"),
    }

config = Config() 