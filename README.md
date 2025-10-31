# stripe-sync

Small utilities to export/import Stripe products & prices and inspect local export files.

## Overview
- Export products & prices from Stripe to JSON/CSV.
- Import products (and prices) into Stripe from exported JSON.
- List products from Stripe.
- Scripts: export_products.py, export_prices.py, import_products.py, list_products.py, main.py

## Repo contents (summary)
- export_products.py — Export Stripe Product objects (and default prices) to JSON.
- export_prices.py — Export Stripe Price objects to JSON and CSV.
- import_products.py — Import products (and create prices) into Stripe from exported JSON.
- list_products.py — CLI helper to list products & prices (see "Notes" below).
- main.py — Simple CLI wrapper for common operations.
- config.py — Loads environment variables and returns a configured Stripe client.
- exports/ — sample export files (JSON/CSV)
- requirements.txt, .env.example (not committed secrets)

## Requirements
- Python 3.8+
- See requirements.txt for dependencies

## Setup

1. Create and activate a virtual environment

Windows (PowerShell / CMD):
```ps
python -m venv venv
.\venv\Scripts\Activate.ps1   # PowerShell
.\venv\Scripts\activate.bat   # CMD
```

macOS / Linux:
```sh
python -m venv venv
source venv/bin/activate
```

2. Install dependencies
```sh
pip install -r requirements.txt
```

3. Configure environment variables
Create a `.env` file (do not commit secrets). Relevant variables used by the code:
- STRIPE_TEST_KEY
- STRIPE_LIVE_KEY
- STRIPE_MODE      # "test" or "live"
- EXPORT_FOLDER    # e.g. ./exports
- EXPORT_PRODUCTS_FILE
- EXPORT_PRICES_FILE

The project uses python-dotenv or similar (see config.py) to load these values.

## Usage

Run the small CLI in main.py:
```sh
python main.py export [products|prices] [csv|json]  # export products/prices from Stripe to files
python main.py import    # import products/prices from exported JSON to Stripe
python main.py list <number_of_products>    # list first page of products from Stripe
```

Or run scripts directly:
```sh
python export_products.py [csv|json]
python export_prices.py
python import_products.py
python list_products.py <number_of_products>
```

Recommended workflow:
1. Set STRIPE_MODE=test and use STRIPE_TEST_KEY.
2. Run export to capture current Stripe state.
3. Inspect exported JSON/CSV files.
4. Run import only after verifying mapping and edge cases (null unit_amount, recurring prices).
5. When ready, switch to live keys.

## Exports & Output
Default output folder is configured with EXPORT_FOLDER. Typical files:
- live_products_export.json / .csv
- sandbox_products_export.json / .csv
- live_prices_export.json / .csv
- live_prices_export.json / .csv
- sandbox_prices_export.json / .csv

Check the CSV/JSON format in the sample export files in the repo.

## Notes & Gotchas
- Importer may skip prices with null unit_amount (custom/donation prices). Review import_products.py before running.
- Recurring and one-time prices are handled differently; verify the mapping logic.
- Use test mode before running against live Stripe keys.
- Do not commit your .env or API keys.
- Export scripts use Stripe pagination (auto_paging_iter() / manual paging), so large exports can take time.
- Importer may skip prices with null unit_amount (custom/donation prices). Inspect import_products.py before running.


## Troubleshooting
- Invalid/insufficient API key errors → verify STRIPE_* keys and STRIPE_MODE.
- Large exports → scripts use Stripe pagination (may take time).

## Contributing
- Add CLI flags (dry-run, limit, output path).
- Add unit tests for import/export mapping and edge cases.
- Improve logging, error handling and retries.

## License
[![CC0](https://i.creativecommons.org/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)

## Stripe API documentation (reference)

Official Stripe documentation — use these links for details on API endpoints, object schemas, authentication, testing, and best practices:

- API Reference: https://stripe.com/docs/api
- Products API: https://stripe.com/docs/api/products
- Prices API: https://stripe.com/docs/api/prices
- Authentication & API keys: https://stripe.com/docs/keys
- Pagination: https://stripe.com/docs/api/pagination
- Webhooks: https://stripe.com/docs/webhooks
- Python SDK / Libraries: https://stripe.com/docs/libraries#python
- Testing guide (test data & tokens): https://stripe.com/docs/testing

Use the official docs when reviewing object fields (e.g. price.unit_amount, price.recurring), request parameters, and rate-limit behavior before running imports/exports against live data.

