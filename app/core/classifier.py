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

        # Normalize commands with missing spaces (e.g., /listapp -> /list app)
        if text_lower.startswith("/"):
            for cmd in ["/list", "/read", "/create", "/edit", "/help"]:
                if text_lower.startswith(cmd) and len(text_lower) > len(cmd) and text_lower[len(cmd)] != ' ':
                    text_lower = cmd + " " + text_lower[len(cmd):]
                    text = text[:len(cmd)] + " " + text[len(cmd):]
                    break

        for pattern, intent in self.rules:
            if re.search(pattern, text_lower):
                params = self._extract_params(intent, text)
                params["text"] = text # Keep the full text
                return intent, params

        # If no specific rule matches, we consider it a CHAT intent
        # but only if it's not empty.
        if text.strip():
            return Intent.CHAT, {"text": text}

        return Intent.UNKNOWN, {}

    def _extract_params(self, intent: Intent, text: str) -> Dict[str, Any]:
        """Simple parameter extractor based on command structure."""
        # Convert to list of words and ignore trigger words like "archivos", "archivo", "los", "el"
        # only if they appear where the parameter is expected.
        parts = text.split()
        params = {}

        if intent == Intent.LIST_FILES:
            # If "listar archivos", parts[1] is "archivos". Ignore it.
            if len(parts) > 1:
                # If first word after command is "archivos", check if there's a 3rd word
                if parts[1].lower() in ["archivos", "los"]:
                    params["path"] = parts[2] if len(parts) > 2 else "."
                else:
                    params["path"] = parts[1]
            else:
                params["path"] = "."
                
        elif intent == Intent.READ_FILE:
            if len(parts) > 1:
                if parts[1].lower() in ["archivo", "el"]:
                    params["filename"] = parts[2] if len(parts) > 2 else None
                else:
                    params["filename"] = parts[1]
            else:
                params["filename"] = None
                
        elif intent == Intent.CREATE_FILE:
            # Similar logic for create
            if len(parts) > 1:
                idx = 1
                if parts[idx].lower() in ["archivo", "el"]:
                    idx += 1
                
                if len(parts) > idx:
                    params["filename"] = parts[idx]
                    params["content"] = " ".join(parts[idx+1:])
                else:
                    params["filename"] = None
                    params["content"] = ""
            else:
                params["filename"] = None
                params["content"] = ""
                
        elif intent == Intent.EDIT_FILE:
            # Expected: /edit filename target replacement
            # Skip "archivo" or "el" if present
            if len(parts) > 1:
                idx = 1
                if parts[idx].lower() in ["archivo", "el"]:
                    idx += 1
                
                if len(parts) >= idx + 3:
                     params["filename"] = parts[idx]
                     params["target"] = parts[idx+1]
                     params["replacement"] = " ".join(parts[idx+2:])
        
        return params
