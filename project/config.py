import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# اگر در ایران هستید و اتصال مشکل دارد، پراکسی وارد کنید
PROXY_URL = os.getenv("PROXY_URL", None)