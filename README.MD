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