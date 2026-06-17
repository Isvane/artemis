import re
from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr, Field

STRONG_PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[ !\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~]).+$"
)


def validate_password_strength(password: str) -> str:
    if not STRONG_PASSWORD_REGEX.match(password):
        raise ValueError(
            "Password must contain at least one uppercase letter, lowercase letter, digit, and special character."
        )
    return password


Username = Annotated[
    str,
    Field(
        min_length=4,
        max_length=40,
        pattern="^[a-zA-Z0-9_.-]+$",
        examples=["Artemis"],
    ),
]

Password = Annotated[
    str,
    Field(min_length=8, max_length=128, examples=["I_Love_You_3000!"]),
    AfterValidator(validate_password_strength),
]


class UserBase(BaseModel):
    username: Username
    email: EmailStr


class UserCreate(UserBase):
    password: Password


class UserUpdate(BaseModel):
    username: Username | None = None
    email: EmailStr | None = None
    password: Password | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
