from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from services.ai_service import analyze_ticket
from database import engine, Base, SessionLocal
from models.ticket import TicketDB

#create FastAPI app (backend server)
app = FastAPI()

Base.metadata.create_all(bind=engine)

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#tickets = [] #temp for now

#keeps track of ticket IDs so each ticket gets a number
#ticket_id_counter = 1

#What user sends 
#no "id" since backend generates it
class TicketCreate(BaseModel):
    title: str #required ticket title
    details: str
    severity: Optional[str] = "Low" #optional but defaults to "low"

#backend stores ticket
class Ticket(BaseModel):
    id: int #number backend generates
    title: str
    details: str
    severity: str
    category: str = "Uncategorized"
    status: str = "Open" #defaults to "open"
    created_at: str
    assigned_to: Optional[str] = None
    
    #AI-generated
    ai_summary: Optional[str] = None
    recommended_steps: Optional[list[str]] = None
    ai_confidence: Optional[float] = None

class StatusUpdate(BaseModel):
    status: str

class TicketResponse(BaseModel):
    message: str
    ticket: Ticket

class AssignedTo(BaseModel):
    assigned: str

#confirm the API is running
@app.get("/")
def home():
    return {"message": "Backend is running"}

#creates a new ticket
@app.post("/tickets", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate):

    db = SessionLocal()

    ai_result = analyze_ticket(
        ticket.title,
        ticket.details
    )

    new_ticket = TicketDB(
        title=ticket.title,
        details=ticket.details,
        severity=ticket.severity,
        category=ai_result["category"],
        status="Open",
        created_at=datetime.now().isoformat(),
        assigned_to=None,
        ai_summary=ai_result["ai_summary"],
        recommended_steps=ai_result["recommended_steps"],
        ai_confidence=ai_result["ai_confidence"]
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    db.close()

    return {
        "message": "Ticket stored successfully",
        "ticket": new_ticket
    }
    
#get all tickets
#returns everything stored currently in memory

@app.get("/tickets")
def get_tickets():
    db = SessionLocal()

    tickets = db.query(TicketDB).all()

    db.close()

    return tickets

@app.delete("/tickets/{ticket_id}") #expects url with ticket id
def delete_tickets(ticket_id: int):
    db = SessionLocal()

    ticket = db.query(TicketDB).filter(
        TicketDB.id == ticket_id
    ).first()

    if ticket:
        db.delete(ticket)
        db.commit()
        db.close()

        return {
            "message": "Ticket deleted successfully"
        }
    db.close()

    return {
        "message": "Ticket not found"
    }


@app.put("/tickets/{ticket_id}/status")
def update_ticket_status(ticket_id: int, status_update: StatusUpdate):
    db = SessionLocal()

    ticket = db.query(TicketDB).filter(
        TicketDB.id == ticket_id
    ).first()

    if ticket:
        ticket.status = status_update.status
        db.commit()
        db.refresh(ticket)
        db.close()

        return {
            "message": "Status updated successfully",
            "ticket": ticket
        }
    db.close()

    return {
        "message": "Ticket not found"
    }

@app.put("/tickets/{ticket_id}/assign")
def assign_to (ticket_id: int, assignment: AssignedTo):
    db = SessionLocal()

    ticket = db.query(TicketDB).filter(
        TicketDB.id == ticket_id
    ).first()

    if ticket:
        ticket.assigned_to = assignment.assigned

        db.commit()
        db.refresh(ticket)
        db.close()

        return {
            "message": "Status assigned successfully",
            "ticket": ticket
        }
    db.close()

    return {
        "message": "Ticket not found"
    }
