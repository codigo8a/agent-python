import os
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

class FileManager:
    """Service to handle filesystem operations."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = os.path.abspath(base_path)

    async def list_files(self, relative_path: str = ".") -> str:
        """List files in the given directory."""
        try:
            target_path = os.path.abspath(os.path.join(self.base_path, relative_path))
            if not target_path.startswith(self.base_path):
                return "Error: Access denied (path outside project)."
            
            if not os.path.exists(target_path):
                return f"Error: Path '{relative_path}' does not exist."
            
            items = os.listdir(target_path)
            if not items:
                return f"Directory '{relative_path}' is empty."
            
            return "\n".join([f"📁 {item}" if os.path.isdir(os.path.join(target_path, item)) else f"📄 {item}" for item in items])
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return f"Error: {str(e)}"

    async def read_file(self, relative_path: str) -> str:
        """Read content of a file."""
        try:
            target_path = os.path.abspath(os.path.join(self.base_path, relative_path))
            if not target_path.startswith(self.base_path):
                return "Error: Access denied."
            
            if not os.path.isfile(target_path):
                return f"Error: '{relative_path}' is not a file."
            
            with open(target_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"```\n{content}\n```"
        except Exception as e:
            return f"Error: {str(e)}"

    async def create_file(self, relative_path: str, content: str) -> str:
        """Create or overwrite a file."""
        try:
            target_path = os.path.abspath(os.path.join(self.base_path, relative_path))
            if not target_path.startswith(self.base_path):
                return "Error: Access denied."
            
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"File '{relative_path}' created successfully."
        except Exception as e:
            return f"Error: {str(e)}"

    async def edit_file(self, relative_path: str, target: str, replacement: str) -> str:
        """Replace text in a file."""
        try:
            target_path = os.path.abspath(os.path.join(self.base_path, relative_path))
            if not target_path.startswith(self.base_path):
                return "Error: Access denied."
            
            if not os.path.isfile(target_path):
                return f"Error: '{relative_path}' not found."
            
            with open(target_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if target not in content:
                return f"Error: '{target}' not found in file."
            
            new_content = content.replace(target, replacement)
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return f"File '{relative_path}' updated successfully."
        except Exception as e:
            return f"Error: {str(e)}"
