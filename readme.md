# RE/MAX Costa Rica Property Scraper

This Python-based scraper extracts real estate listings from [RE/MAX Costa Rica](https://www.remax-costa-rica.com/Properties-Propiedades/) and saves them in a structured Excel file for analysis.

## Features

- Extracts:
  - Title
  - Listing URL
  - Image URL
  - Date of publication
  - Short description
- Saves data in `/output` as `.xlsx`
- Clean and extendable code

## Requirements

- Python 3.8+
- requests
- beautifulsoup4
- pandas
- openpyxl

Install dependencies:

```bash
pip install -r requirements.txt
