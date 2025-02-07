from openai import OpenAI
from app.core.config import config



class OpenRouterService:
    def __init__(self):
        self.model = "nousresearch/hermes-2-pro-llama-3-8b"
        # self.model = "openai/gpt-4o-mini"
        self.client = self._create_client()
        self.config = self._create_config()
        
    def _get_cloudflare_ai_gateway_url(self) -> str:
        return f'https://gateway.ai.cloudflare.com/v1/{config.CLOUDFLARE_ACCOUNT_ID}/{config.CLOUDFLARE_API_GATEWAY_NAME}/openrouter'
    
    def _create_client(self) -> OpenAI:
        OpenAI.default_headers = {
            'cf-aig-authorization': f'Bearer {config.CLOUDFLARE_API_GATEWAY_TOKEN}',
            'Authorization': f'Bearer {config.OPENROUTER_API_KEY}'
        }
        
        return OpenAI(
            base_url=self._get_cloudflare_ai_gateway_url()
        )
    
    def _create_config(self) -> dict:
        return {
            'model': self.model,   
            'temperature': 0.7
        }
    
    def get_client(self) -> OpenAI:
        return self.client
    
    def get_config(self) -> dict:
        return self.config


# Create a singleton instance
openrouter_service = OpenRouterService()
openrouter_client = openrouter_service.get_client()
openrouter_config = openrouter_service.get_config() 