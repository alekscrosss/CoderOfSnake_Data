Installation Instructions
To install and run the application, follow these steps:


1. Clone the Repository
Clone the repository from GitHub to your workspace:


use command: git clone https://github.com/alekscrosss/CoderOfSnake_Data


2. Create a .env File
In the root of the project, create a .env file to store your environment variables. Insert your specific details as shown below:


APP_ENV=your_app_environment POSTGRES_DB=your_postgres_db POSTGRES_USER=your_postgres_user POSTGRES_PASSWORD=your_postgres_password POSTGRES_PORT=your_postgres_port


SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}


SECRET_KEY=your_secret_key ALGORITHM=HS256


MAIL_USERNAME=your_mail_username MAIL_PASSWORD=your_mail_password MAIL_FROM=your_mail_from MAIL_PORT=your_mail_port MAIL_SERVER=your_mail_server


REDIS_HOST=localhost REDIS_PORT=6379


CLD_NAME=your_cloudinary_name CLD_API_KEY=your_cloudinary_api_key CLD_API_SECRET=your_cloudinary_api_secret


3. Start Docker
Ensure Docker is running on your system. You may need to start Docker from your applications menu or system settings.


4. Run Docker Compose
Build and start the application containers using Docker Compose:


in telminal use command: # docker-compose up
This command will set up all necessary services as defined in your docker-compose.yml.


5. Launch the Application with Uvicorn
In a new terminal session, start the FastAPI application:


use command: uvicorn main:app --reload
The --reload option enables auto-reloading, allowing the server to automatically restart after file changes. This is particularly useful during development.


6. Access the FastAPI Application
After starting the application, you can access the FastAPI UI by navigating to:


http://localhost:8000/docs This URL provides access to the FastAPI Swagger UI, where you can test and interact with the available API endpoints.