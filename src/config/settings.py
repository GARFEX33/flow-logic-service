import os
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
BROKER_URL = os.getenv("BROKER_URL", "localhost:9092")
ENV = os.getenv("ENV", "development")
SERVICE_NAME = os.getenv("SERVICE_NAME", "flow-logic-service")
AUDIT_DB_URL = os.getenv("AUDIT_DB_URL", "sqlite:///audit.db")