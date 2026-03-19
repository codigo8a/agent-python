class Responder:
    """Class to handle business logic for generating responses."""
    
    @staticmethod
    async def get_response() -> str:
        """Always returns the requested string.
        
        Returns:
            str: "que pasa?"
        """
        return "que pasa?"
