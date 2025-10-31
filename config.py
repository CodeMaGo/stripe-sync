from dotenv import load_dotenv
import os
import stripe

# Load .env variables
load_dotenv()

# Read values
STRIPE_LIVE_KEY = os.getenv("STRIPE_LIVE_KEY")
STRIPE_TEST_KEY = os.getenv("STRIPE_TEST_KEY")
STRIPE_MODE = os.getenv("STRIPE_MODE", "test")
EXPORT_FOLDER = os.getenv("EXPORT_FILE", "./exports/")
EXPORT_PRODUCTS_FILE = os.getenv("EXPORT_PRODUCT_FILE", "products_export")
EXPORT_PRICES_FILE = os.getenv("EXPORT_FILE", "prices_export")


# Select correct key
stripe.api_key = STRIPE_LIVE_KEY if STRIPE_MODE == "live" else STRIPE_TEST_KEY

def get_stripe_client():
    return stripe
