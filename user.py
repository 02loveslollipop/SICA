class User :
    # bcrypt?

    @staticmethod
    def bulk_from_dict(data: dict) -> list['User']:
        return [User(**item) for item in data]

    def __init__(self, username: str,password: str,role: str,_id: int = None,_isActive: bool = True) -> None:  
        self.username = username
        self.password = password
        self.role = role
        self.id = _id
        self.isActive = _isActive

    def to_dict(self) -> dict:
        return {
        'username': self.username,
        'password': self.password,
        'role': self.role,
        '_isActive': self.isActive
        } 
    
