class ExpiredTokenException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class TokenNotInSessionException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class ProductNotFoundException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
class ProviderNotFoundException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class UserNotFoundException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)