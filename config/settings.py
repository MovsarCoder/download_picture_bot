import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
ADMIN = os.getenv('ADMIN')


PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")
PRICE = [{'label': 'VIP', 'amount': 10000}]