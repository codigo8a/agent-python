from typing import Dict, Any
from app.handlers.base_handler import BaseHandler
from app.services.file_manager import FileManager
from app.core.intent import Intent

class FileHandler(BaseHandler):
    """Handler for file-related intents."""
    
    def __init__(self):
        self._file_manager = FileManager()

    async def handle(self, intent: Intent, params: Dict[str, Any]) -> str:
        """Execute file operations based on intent."""
        if intent == Intent.LIST_FILES:
            return await self._file_manager.list_files(params.get("path", "."))
        elif intent == Intent.READ_FILE:
            return await self._file_manager.read_file(params.get("filename", ""))
        elif intent == Intent.CREATE_FILE:
            return await self._file_manager.create_file(params.get("filename", ""), params.get("content", ""))
        elif intent == Intent.EDIT_FILE:
            return await self._file_manager.edit_file(
                params.get("filename", ""), 
                params.get("target", ""), 
                params.get("replacement", "")
            )
        return "Error: Intent not supported by FileHandler."
