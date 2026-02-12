import adsk.fusion, adsk.core
from abc import abstractmethod

class CustomComputeError(Exception):
    """Base class for exceptions in custom features."""

    def update_status(self, status: adsk.core.Status):
        messages = status.statusMessages
        messages.addError(self.error_id)
        pass

    @property
    @abstractmethod
    def error_id(self) -> str:
        pass

class ReferenceLostError(CustomComputeError):
    """Raised when a reference used by a custom feature is lost."""
    @property
    def error_id(self) -> str:
        return "FEATURE_REFERENCE_LOST"
    
class InvalidInputError(Exception):
    message: str
    def __init__(self, message: str):
        self.message = message
