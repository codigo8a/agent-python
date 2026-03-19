from enum import Enum, auto

class Intent(Enum):
    """Enumeration of possible user intents."""
    LIST_FILES = auto()
    READ_FILE = auto()
    CREATE_FILE = auto()
    EDIT_FILE = auto()
    HELP = auto()
    GREETING = auto()
    UNKNOWN = auto()
