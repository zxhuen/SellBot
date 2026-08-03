from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import PersonCreate, PersonResponse
from app.services import add_person_services, list_person_services, edit_person_services, delete_person_services
from app.core.limiter import limiter

router = APIRouter(prefix="/Person", tags=["Person"])

@router.post("/", response_model=PersonResponse)
@limiter.limit("10/minute")
def add_person(request: Request, person: PersonCreate, db: Session = Depends(get_db)):
    return add_person_services(db, person)

@router.get("/", response_model= list[PersonResponse])
@limiter.limit("10/minute")
def get_person(request: Request, db: Session = Depends(get_db)):
    return list_person_services(db)

@router.put("/{person_id}", response_model=PersonResponse)
@limiter.limit("10/minute")
def edit_person(request: Request, person_id: int, person: PersonCreate, db: Session = Depends(get_db)):
    persons = edit_person_services(db, person_id, person)   
    
    return persons

@router.delete("/{person_id}", response_model=PersonResponse)
@limiter.limit("10/minute")
def delete_person(request: Request, person_id: int, db: Session = Depends(get_db)):
    person = delete_person_services(db, person_id)
    
    return person