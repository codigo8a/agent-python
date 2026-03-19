import asyncio
import sys
import logging
from app.main import App
from app.config import Config

# Setup logging levels for external libraries to reduce noise
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.INFO)

# Run entry point
if __name__ == "__main__":
    """Main execution point for the application."""
    
    app = App()
    
    # Loop and start the bot with proper error handling
    try:
        # Start async event loop
        asyncio.run(app.start())
    except KeyboardInterrupt:
        # Exit on manual interruption
        sys.exit(0)
    except Exception as e:
        # Exit on fatal error
        sys.exit(1)
