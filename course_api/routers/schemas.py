from pydantic import BaseModel, field_validator, Field


class CreateUser(BaseModel):
    firstname: str = Field(default=None, max_length=50, min_length=3)
    lastname: str = Field(default=None, max_length=50, min_length=3)

    @field_validator('firstname')
    @classmethod
    def firstname_cant_contain_space(cls, firstname: str) -> str:
        if ' ' in firstname:
            raise ValueError("can't contain space")
        return firstname.title()
