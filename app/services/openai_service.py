from openai import OpenAI
from app.core.config import config

def get_openai_client() -> OpenAI:
    OpenAI.default_headers = {
        'cf-aig-authorization': f'Bearer {config.CLOUDFLARE_API_GATEWAY_TOKEN}',
        'Authorization': f'Bearer {config.OPENAI_API_KEY}'
    }
    
    return OpenAI(
        base_url=f'https://gateway.ai.cloudflare.com/v1/{config.CLOUDFLARE_ACCOUNT_ID}/{config.CLOUDFLARE_API_GATEWAY_NAME}/openai'
    )

def get_openai_config() -> dict:
    return {
        'model': config.OPENAI_MODEL,
        'temperature': 0.7
    }

openai_client = get_openai_client()
openai_config = get_openai_config() 