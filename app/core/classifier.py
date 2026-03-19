import re
from typing import Optional, Dict, Any, Tuple
from app.core.intent import Intent

class IntentClassifier:
    """Class to identify user intent using rule-based matching."""
    
    def __init__(self):
        # Rules defined as (Regex Pattern, Intent)
        self.rules: List[Tuple[str, Intent]] = [
            (r"^/list\b|^(listar|ver|muestrame) archivos", Intent.LIST_FILES),
            (r"^/read\b|^dime que dice|^lee", Intent.READ_FILE),
            (r"^/create\b|^crea el archivo|^nuevo archivo", Intent.CREATE_FILE),
            (r"^/edit\b|^edita|^reemplaza en|^cambia", Intent.EDIT_FILE),
            (r"^/help\b|^ayuda|^que puedes hacer", Intent.HELP),
            (r"^hola|^buenos dias|^hablaló", Intent.GREETING),
        ]

    def classify(self, text: str) -> Tuple[Intent, Dict[str, Any]]:
        """Identify the intent and extract parameters from the text.
        
        Args:
            text (str): Incoming message text.
            
        Returns:
            Tuple[Intent, Dict[str, Any]]: Identified intent and extracted parameters.
        """
        if not text:
            return Intent.UNKNOWN, {}

        text_lower = text.lower().strip()

        for pattern, intent in self.rules:
            if re.search(pattern, text_lower):
                params = self._extract_params(intent, text)
                return intent, params

        return Intent.UNKNOWN, {}

    def _extract_params(self, intent: Intent, text: str) -> Dict[str, Any]:
        """Simple parameter extractor based on command structure."""
        parts = text.split(maxsplit=3)
        params = {}

        if intent == Intent.LIST_FILES:
            params["path"] = parts[1] if len(parts) > 1 else "."
        elif intent == Intent.READ_FILE:
            params["filename"] = parts[1] if len(parts) > 1 else None
        elif intent == Intent.CREATE_FILE:
            params["filename"] = parts[1] if len(parts) > 1 else None
            params["content"] = " ".join(parts[2:]) if len(parts) > 2 else ""
        elif intent == Intent.EDIT_FILE:
            # Expected: /edit filename target replacement
            if len(parts) >= 4:
                params["filename"] = parts[1]
                # Further splitting for target/replacement
                rest = parts[3].split(maxsplit=1)
                if len(rest) >= 2:
                    params["target"] = rest[0]
                    params["replacement"] = rest[1]
        
        return params
