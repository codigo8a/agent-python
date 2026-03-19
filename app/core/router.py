from app.services.responder import Responder

class Router:
    """Class to route incoming messages to the proper responder."""
    
    def __init__(self):
        self._responder = Responder()

    async def route(self) -> str:
        """Route the message to the responder.
        
        Returns:
            str: Response string.
        """
        return await self._responder.get_response()
