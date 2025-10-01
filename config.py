from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()


class Settings(BaseModel):
    # Security
    secret_key: str = Field(default=os.getenv("SECRET_KEY", "dev_secret"))

    # Database
    database_url: str = Field(default=os.getenv("DATABASE_URL", "sqlite:///./expense.db"))

    # Email / SMTP
    smtp_host: str = Field(default=os.getenv("SMTP_HOST", ""))
    smtp_port: int = Field(default=int(os.getenv("SMTP_PORT", 587)))
    smtp_user: str = Field(default=os.getenv("SMTP_USER", ""))
    smtp_pass: str = Field(default=os.getenv("SMTP_PASS", ""))


    # Currency
    currency_base: str = Field(default=os.getenv("CURRENCY_BASE", "USD"))

    # Helper method to get the active AI API key

settings = Settings()
