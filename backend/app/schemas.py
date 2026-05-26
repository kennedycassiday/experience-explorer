from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel
from datetime import date, time, datetime

class RequestIn(SQLModel):
    # Optional contact info (user may provide now or later)
    name: str | None = None
    email: EmailStr | None = None

    @field_validator("email", mode="before")
    @classmethod
    def empty_email_to_none(cls, v):
        if v is None or (isinstance(v, str) and not v.strip()):
            return None
        return v

    # Birth information
    dob: date
    birth_time: time
    birth_location: str

    # Experience information
    experience_date: date
    experience_time: time
    experience_location: str
    substance: str | None = None
    intention: str | None = None

class AnswerOut(SQLModel):
    answer_text: str
    draft_token: str | None = None #signed token that contains RequestIn + answer_text

    newsletter_opt_in: bool = False
    saved: bool = False


class EmailOptIn(SQLModel):
    # For users who didn’t provide email initially but want to save later

    draft_token: str
    name: str | None = None
    email: str
    # newsletter_opt_in: bool

class SaveResult(SQLModel):
    user_id: int
    experience_id: int
    newsletter_opt_in: bool
