class User :

    @staticmethod
    def bulk_from_dict(data: dict) -> list['User']:
        return [User(**item) for item in data]

    def __init__(self, name: str,lastname: str,email: str,cellphone: int,password: str,role: str,_id: int = None,_isActive: bool = True) -> None:  
        self.name = name
        self.lastname = lastname
        self.email = email
        self.cellphone = cellphone
        self.password = password
        self.role = role
        self._id = _id
        self.isActive = _isActive

    def to_dict(self) -> dict:
        return {
        'name': self.name,
        'lastname': self.lastname,
        'email': self.email,
        'cellphone': self.cellphone,
        'password': self.password,
        'role': self.role,
        '_isActive': self.isActive
        } 
    
