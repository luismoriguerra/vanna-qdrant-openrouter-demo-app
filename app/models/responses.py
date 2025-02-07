from typing import Any, Optional, List, Dict
from dataclasses import dataclass

@dataclass
class APIResponse:
    status: str
    data: Optional[Any] = None
    message: Optional[str] = None

    def to_dict(self) -> Dict:
        response = {"status": self.status}
        if self.data is not None:
            response["data"] = self.data
        if self.message is not None:
            response["message"] = self.message
        return response

def success_response(data: Any = None) -> Dict:
    return APIResponse(status="success", data=data).to_dict()

def error_response(message: str) -> Dict:
    return APIResponse(status="error", message=message).to_dict() 