from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()



url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)
