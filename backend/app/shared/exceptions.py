"""
Domain exceptions for LPBank AI RM Copilot.
"""

class DomainException(Exception):
    """Base domain exception."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class CustomerNotFoundException(DomainException):
    def __init__(self, customer_id: str):
        super().__init__(f"Customer not found: {customer_id}")
        self.customer_id = customer_id


class TransactionNotFoundException(DomainException):
    def __init__(self, message: str = "No transactions found"):
        super().__init__(message)


class RecommendationEngineException(DomainException):
    def __init__(self, message: str):
        super().__init__(message)


class LLMServiceException(DomainException):
    def __init__(self, message: str):
        super().__init__(message)

