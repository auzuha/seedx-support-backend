from groq import Groq
from app.models import Ticket, Message
from app.config import GROQ_API_KEY

def store_ai_message(db, ticket_id, full_content):
    """
    Function to store AI Responses in the database.
    """
    message = Message(content=full_content, is_ai=True, ticket_id=ticket_id)
    db.add(message)
    db.commit()
    db.refresh(message)


async def get_ai_response(ticket: Ticket, messages: list[Message], db):
    """
    Function to get the AI Response for a particular ticket conversation.
    """
    #init the conversation list with system message
    conversation = [
        {"role": "system", "content": f"You are an assistant that will resolve user queries about tickets. The current ticket description is: {ticket.description}"}
    ]

    #add messages in the conversation history
    for msg in messages:
        if msg.is_ai:
            conversation.append({"role": "assistant", "content": msg.content})
        else:
            conversation.append({"role": "user", "content": msg.content})
    
    #init groq client
    client = Groq()

    #stream the response
    stream = client.chat.completions.create(
        messages = conversation,
        model="llama-3.3-70b-versatile",
        stream=True
    )

    #init a variable to store the full ai response, to add to messages database later
    full_content = ""

    #stream the ai response
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            full_content += content
            yield content
        else:
            yield ""
    
    #add complete ai response to the database
    store_ai_message(db, ticket.id, full_content)
    
