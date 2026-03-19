from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseHandler(ABC):
    """Abstract base class for all intent handlers."""
    
    @abstractmethod
    async def handle(self, params: Dict[str, Any]) -> str:
        """Handle the identified intent with the given parameters."""
        pass
