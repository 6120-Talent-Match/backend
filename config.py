# config.py - Configuration settings
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
  DB_NAME: str = "talentmatch"
  DB_USER: str = "postgres"
  DB_PASSWORD: str = "root"
  DB_HOST: str = "localhost"
  DB_PORT: str = "5432"
  OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
  HUGGING_FACE_API_KEY: str = os.getenv("HUGGING_FACE_API_KEY")

  @property
  def db_params(self):
    return {
        "dbname": self.DB_NAME,
        "user": self.DB_USER,
        "password": self.DB_PASSWORD,
        "host": self.DB_HOST,
        "port": self.DB_PORT
    }

  class Config:
    env_file = ".env"


settings = Settings()
