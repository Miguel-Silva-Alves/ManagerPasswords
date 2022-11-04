import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
BASE_KEY = os.getenv('BASE_KEY')