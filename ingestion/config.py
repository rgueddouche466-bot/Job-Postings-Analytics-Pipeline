import os
from dotenv import load_dotenv
from pathlib import Path
# Always resolve .env relative to project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# load_dotenv()

class Config:
    ADZUNA_APP_ID = os.environ.get('ADZUNA_APP_ID')
    ADZUNA_API_KEY = os.environ.get('ADZUNA_API_KEY')
    BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search"

    SNOWFLAKE_CONFIG ={
        'user': os.environ.get('SNOWFLAKE_USER'),
        'password': os.environ.get('SNOWFLAKE_PASSWORD'),
        'account': os.environ.get('SNOWFLAKE_ACCOUNT'),
        'database': os.environ.get('SNOWFLAKE_DATABASE'),
        'warehouse': os.environ.get('SNOWFLAKE_WAREHOUSE'),
        'schema': os.environ.get('SNOWFLAKE_SCHEMA'),
    }


# print("APP_ID:", os.getenv("ADZUNA_APP_ID"))
# print("API_KEY:", os.getenv("ADZUNA_API_KEY"))
