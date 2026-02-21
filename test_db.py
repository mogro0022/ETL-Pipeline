import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load the environment variables from the .env file
load_dotenv()

# Grab the database URL
db_url = os.getenv("AZURE_PG_URL")

try:
    # Create the SQLAlchemy engine
    engine = create_engine(db_url)

    # Open a connection and run a simple test query
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print("Success! Connected to Azure:")
        print(result.fetchone()[0])

except Exception as e:
    print(f"Connection failed: {e}")
