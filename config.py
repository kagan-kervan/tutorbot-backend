import os

# You can use an environment variable or a hardcoded fallback
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/tutorbot"
)

api_key="API_KEY"