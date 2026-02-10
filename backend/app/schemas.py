from sqlmodel import SQLModel
from datetime import date, time, datetime

class RequestIn(SQLModel):
    # Optional contact info (user may provide now or later)
    name: str | None = None
    email: str | None = None

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

class SaveResult(SQLModel):
    user_id: int
    experience_id: int
    newsletter_opt_in: bool
