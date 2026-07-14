from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#create FastAPI app (backend server)
app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tickets = [] #temp for now

#keeps track of ticket IDs so each ticket gets a number
ticket_id_counter = 1

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
    ai_summary: Optional[str] = None

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
@app.post("/tickets", response_model = TicketResponse)
def create_ticket(ticket: TicketCreate): #what the user sends
    global ticket_id_counter #can modify counter

    new_ticket = Ticket(
        id = ticket_id_counter,
        title = ticket.title,
        details = ticket.details,
        severity = ticket.severity,
        status = "Open",
        created_at = datetime.now().isoformat()
    )

    ticket_id_counter += 1 #modify counter
    tickets.append(new_ticket.model_dump()) #convers object into dictionary and stoes in the database

    return {
        "message": "Ticket stored successfully",
        "ticket": new_ticket
    }
#get all tickets
#returns everything stored currently in memory
@app.get("/tickets", response_model = list[Ticket])
def get_tickets():
    return tickets

@app.delete("/tickets/{ticket_id}") #expects url with ticket id
def delete_tickets(ticket_id: int):
    for ticket in tickets: #loops through stored tickets
        if ticket["id"] == ticket_id: #checks if this is the ticket that needs to be deleted
            tickets.remove(ticket) #deletes it

            return{
                "message": "Ticket deleted successfully"
            }
    return {
        "message": "Ticket not found"
    }

@app.put("/tickets/{ticket_id}/status")
def update_ticket_status(ticket_id: int, status_update: StatusUpdate):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["status"] = status_update.status

            return {
                "message": "Status updated successfully",
                "ticket": ticket
            }
    return {
        "message": "Ticket not found"
    }

@app.put("/tickets/{ticket_id}/assign")
def assign_to (ticket_id: int, assignment: AssignedTo):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["assigned_to"] = assignment.assigned

            return {
                "message": "Ticket assigned successfully",
                "ticket": ticket
            }
    return {
        "message": "Ticket not found"
    }
    