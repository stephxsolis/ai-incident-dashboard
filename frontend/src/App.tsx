
//import './App.css'
//import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

function App() {

  const [ticketTitle, setTicketTitle] = useState ("") //ticketTitle is current value & setTicketTitle value updates
  const [ticketDetails, setTicketDetails] = useState ("")
 
  const handleSubmit = () => {
    console.log("Title:", ticketTitle)
    console.log("Details:", ticketDetails)
  }




  
 
  return (
    <div>
      <h1>
        AI Incident Dashboard
      </h1> 

      <label> Ticket Title </label>
      <input id ="ticketTitle"
              type = "text"
              value = {ticketTitle}
              placeholder='Ticket Title'
              onChange = {(e) => setTicketTitle(e.target.value)} /* onChange means */
              />

      <label> Ticket Details </label>
      <textarea id = "ticketDetails"
                value = {ticketDetails}
                placeholder = 'Describe the issue'
                onChange = {(e) => setTicketDetails(e.target.value)}
      ></textarea>
      
      <button id = "submitButton"
              onClick={handleSubmit}> 
              Submit 
      </button>



    

    </div>


  )

}


//have a imput text field
//have a submit INC ticket
//after ticket is submitted AI reads it and gives it a 

//user POV 
//user can see all past tickets
//submit another ticket 

export default App
