from app.services.file_manager import FileManager

class Responder:
    """Class to handle business logic for generating responses."""
    
    def __init__(self):
        self.file_manager = FileManager()

    async def get_response(self, text: str) -> str:
        """Parses the message and returns a response.
        
        Supported commands:
        /list [path]
        /read [file]
        /create [file] [content]
        /edit [file] [target] [replacement]
        """
        if not text:
            return "Please send a command."

        parts = text.split(maxsplit=3)
        command = parts[0].lower()

        if command == "/list":
            path = parts[1] if len(parts) > 1 else "."
            return await self.file_manager.list_files(path)
        
        elif command == "/read":
            if len(parts) < 2:
                return "Usage: /read [filename]"
            return await self.file_manager.read_file(parts[1])
            
        elif command == "/create":
            if len(parts) < 3:
                return "Usage: /create [filename] [content]"
            # rejoin the rest if there's text after the first word of content
            content = " ".join(parts[2:])
            return await self.file_manager.create_file(parts[1], content)
            
        elif command == "/edit":
            # For edit, we need exactly 3 arguments after the command
            edit_parts = text.split(maxsplit=3)
            if len(edit_parts) < 4:
                return "Usage: /edit [filename] [target_text] [replacement_text]"
            # Note: this simple split might be tricky with spaces. 
            # In a real app we'd use quotes, but for now we follow the simple split.
            filename = edit_parts[1]
            # Use split again for target and replacement if they don't have spaces
            # Or just assume the first space after filename is the separator
            rest = edit_parts[3].split(maxsplit=1)
            if len(rest) < 2:
                 return "Usage: /edit [filename] [target_text] [replacement_text]"
            return await self.file_manager.edit_file(filename, rest[0], rest[1])

        return "Comando desconocido. Usa /list, /read, /create o /edit."
