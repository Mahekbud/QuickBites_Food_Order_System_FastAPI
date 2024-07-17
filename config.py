from dotenv import load_dotenv

import os
load_dotenv()
db_url = os.environ.get("DB_url") 

SECRET_KEY = str(os.environ.get("SECRET_KEY"))
ALGORITHM = str(os.environ.get("ALGORITHM"))