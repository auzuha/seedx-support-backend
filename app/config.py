###
###
### Loading environment variables from the .env file and setting them.
###
###
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv('DATABASE_URL')

SECRET_KEY=os.getenv('SECRET_KEY')
JWT_EXPIRATION_TIME=int(os.getenv('JWT_EXPIRATION_TIME'))
GROQ_API_KEY=os.getenv('GROQ_API_KEY')