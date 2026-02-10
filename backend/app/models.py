from sqlmodel import Field, Relationship, SQLModel
from datetime import date, time, datetime, timezone

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = None
    email: str

    dob: date
    birth_time: time
    birth_location: str

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    experiences: list["Experience"] = Relationship(back_populates="user")

    newsletter_subscriber: bool

class Experience(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    #Experience info collected, but saved only if an email is provided
    experience_date: date
    experience_time: time
    experience_location: str
    substance: str | None = None
    intention: str | None = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="experiences")

    #Store exactly what the user saw
    answer_text: str | None = None
