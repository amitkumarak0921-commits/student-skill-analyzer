from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)
    college: str | None = Field(default=None, max_length=150)
    branch: str | None = Field(default=None, max_length=100)
    semester: str | None = Field(default=None, max_length=30)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(max_length=72)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    college: str | None
    branch: str | None
    semester: str | None
    role: str

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
