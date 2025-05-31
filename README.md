# tutorbot-backend

#How To Run:
1- Install all the requirements in the requirements.txt file.

2- Install PostGreSQL and create a new database named "tutorbot".

3- Change the database connection url in the config.py as "DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://{username}:{password}@localhost:5432/tutorbot"
)"

4- Run create_tables.py to create new tables to database.

5- Enter your Gemini API key in the config.py section.

6- Run the app using uvicorn main:app command.

7- Optional: You can build_faiss.py to update the faiss_index and documents.

TO-DO:

1-Adding memory to keep track of the user and also making to point in a direction that they need

2-Adding more resources on the documents

3- Making the UI user-based

4- 