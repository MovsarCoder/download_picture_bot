import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
ADMIN = os.getenv('ADMIN')


PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")
PRICE = [{'label': 'VIP', 'amount': 10000}]



SENDING_RECEIPT = os.getenv("SENDING_RECEIPT")
PAYMENT_DETAILS = os.getenv("PAYMENT_DETAILS")
VIP_SUBSCRIPTION_PRICE = os.getenv("VIP_SUBSCRIPTION_PRICE")

