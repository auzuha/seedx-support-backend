# Support Backend

This is a simple backend application for a Customer Support Assistant. It allows users to create support tickets, track ticket statuses, and interact with an AI for real-time responses. The app uses FastAPI for the backend, PostgreSQL as the database, and integrates with an AI service (like Groq API) for real-time responses.

# Instructions
- Add a valid GROQ API KEY in the .env file.
- run ```docker-compose up --build```
- Access the swagger ui on localhost:8000

# Design Decision
## Service Oriented Architecture
- I focused on a service oriented architecture, each module/service handles a specific responsibility, making the application easier to manage.
- Authentication Service: Handles user signup, login, JWT Token generation.
- Ticket Service: Manages the creation, retrieval and adding messages to the tickets.
- AI Service: Interfaces with Groq to provide real-time responses.

# API Documentation:
## POST ```/auth/signup```
- Creates a new user.
- Request body: 
```
{
  "email": "user@example.com",
  "password": "yourpassword",
  "role": "user"
}
```
- Response:
```
{
  "id": "uuid",
  "email": "example",
  "role": "user"
}
```

## POST ```/auth/login```
- Returns a token for existing user.
- Example Request Body:
```
{
  "email": "example",
  "password": "example"
}
```
- Example Response:
```
{
    "access_token": "token",
    "token_type": "bearer"
}
```

## POST ```/tickets```
- Create a ticket.
- Request Body:
```
{
  "title": "Example Title",
  "description": "Example description"
}
```
- Response:
```
{
  "title": "Example Title",
  "description": "Example description",
  "created_at": "2025-04-20T20:20:39.431487",
  "id": "uuid",
  "status": "open",
  "user_id": "user_id"
}
```

## GET ```/tickets```
- Get all tickets by the current user.
- Response Body:
```
[
  {
    "title": "Example Title",
    "description": "Example description",
    "created_at": "2025-04-20T20:20:39.431487",
    "id": "uuid",
    "status": "open",
    "user_id": "user_id"
  }
]
```


## GET ```/tickets/{ticket_id}```
- Get a ticket by its id
- Response body:
```
{
  "title": "Example Title",
  "description": "Example description",
  "created_at": "2025-04-20T20:20:39.431487",
  "id": "uuid",
  "status": "open",
  "user_id": "user_id"
}
```

## POST ```/tickets/{ticket_id}/messages```
- Add a message to an existing ticket by its ticket id
- Request Body:
```
{
  "content": "message here"
}
```
- Response Body:
```
{
  "content": "message here",
  "is_ai": false,
  "ticket_id": "55928a6b-a189-4723-afc8-806ef248c559",
  "id": "32718703-050b-4c42-b985-350660c27da3",
  "created_at": "2025-04-20T20:26:32.873132"
}
```

## GET ```/tickets/{ticket_id}/ai-response```
- Get AI response for a conversation for a given ticket.
- It is a streaming response.