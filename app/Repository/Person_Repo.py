from sqlalchemy.orm import Session
from app.models.Person import Person
from app.schemas.Person import PersonCreate, PersonResponse

def create_person_repo(db: Session, Persons: PersonCreate):
    db_person = Person(**Persons.model_dump())
    return db_person

def get_person_repo(db: Session):
    return db.query(Person).all()

def edit_person_repo(db: Session, person_id: int, person: PersonCreate):
    person_from_db = (
        db.query(Person)
        .filter(Person.id == person_id)
        .first()
    )
    return person_from_db


def delete_person_repo(db: Session, person_id: int):
    person = db.query(Person).filter(Person.id == person_id).first()

    return person