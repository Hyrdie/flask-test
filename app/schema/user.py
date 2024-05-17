from pydantic_settings import BaseSettings

class User(BaseSettings):
    email: str
    first_name: str
    last_name: str
    avatar: str

class UserResponse(BaseSettings):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str