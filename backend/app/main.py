from .schemas import RequestIn, AnswerOut, EmailOptIn, SaveResult
from .db import create_db_and_tables, engine
from .models import User, Experience
from .security.jwe import create_token, decrypt_token
from fastapi import FastAPI, HTTPException
from sqlmodel import Session
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Experience Explorer Backend")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/request")
def generate_experience_answer(request: RequestIn):
     # Accept birth + experience + optional name/email
    # Generate answer
    # Return answer + signed token
    # Save/email ONLY if email is provided

    session = Session(engine)
    # answer_text = generate_answer(request)
    answer_text = "placeholder answer"
    if request.email:
        user = User(
            name=request.name,
            email=request.email,  # Required for User, so we check email exists first
            dob=request.dob,
            birth_time=request.birth_time,
            birth_location=request.birth_location,
            newsletter_subscriber=False  # Will be updated later if they opt in
        )
        session.add(user)
        session.flush()  # Flush to get the user.id without committing yet

        experience = Experience(
                experience_date=request.experience_date,
                experience_time=request.experience_time,
                experience_location=request.experience_location,
                substance=request.substance,
                intention=request.intention,
                answer_text=answer_text,  # Store the generated answer
                user_id=user.id  # Link to the User
        )
        session.add(experience)
        session.commit()
        session.refresh(user)
        session.refresh(experience)
        return AnswerOut(
            answer_text=answer_text,
            saved=True,
            newsletter_opt_in=False,
            draft_token=None
        )
    else:
        # No email = don't save, just return answer
        # create token and return it
        # Convert RequestIn to dict, handling date/time serialization

        request_dict = request.model_dump(mode='json')  # This handles date/time conversion
        draft_token = create_token(request_dict, answer_text)

        return AnswerOut(
            answer_text=answer_text,
            draft_token=draft_token,
            saved=False,
            newsletter_opt_in=False
        )

@app.post("/save")
def save_experience_from_token(opt_in: EmailOptIn):
    session  = Session(engine)
    # 1. Decrypt the draft_token to get original RequestIn + reconstruct
    try:
        decrypted = decrypt_token(opt_in.draft_token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid token: {str(e)}")

    original_request = RequestIn(**decrypted["request"])
    answer_text = decrypted["answer_text"]

    # 2. Create User from EmailOptIn.email + decrypted RequestIn data
    user = User(
        name=opt_in.name,
        email=opt_in.email,
        dob=original_request.dob,
        birth_time=original_request.birth_time,
        birth_location=original_request.birth_location,
        newsletter_subscriber=False
    )
    session.add(user)
    session.flush()  # Flush to get the user.id without committing yet
    # 3. Create Experience from decrypted RequestIn + answer_text
    experience = Experience(
        experience_date=original_request.experience_date,
        experience_time=original_request.experience_time,
        experience_location=original_request.experience_location,
        substance=original_request.substance,
        intention=original_request.intention,
        answer_text=answer_text,  # Store the generated answer
        user_id=user.id  # Link to the User
    )
    # 4. Save to database
    session.add(experience)
    session.commit()
    session.refresh(user)
    session.refresh(experience)

    # 5. Return success message
    return SaveResult(
        user_id=user.id,
        experience_id=experience.id,
        newsletter_opt_in=False # Update if newsletter_opt_in is added to EmailOptIn
    )
