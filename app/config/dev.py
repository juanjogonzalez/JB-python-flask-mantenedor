import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env.dev"
load_dotenv(ENV_FILE_PATH)

# Flask
SECRET_KEY          = os.environ.get("SECRET_KEY", "YOUR-FALLBACK-SECRET-KEY")

#Database
DATABASE_URI        = os.environ.get('SQLALCHEMY_DATABASE_URI')

class DevConfig:
     # Flask
    TESTING = True
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    STATIC_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False
    SECRET_KEY = SECRET_KEY
    
    # Database
    SQLALCHEMY_DATABASE_URI = DATABASE_URI