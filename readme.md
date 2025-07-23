# Real Estate Web Scraper & Dashboard – REMAX Costa Rica

This project is a **Python-based web scraper and data visualization dashboard** built to extract and explore property listings from the official [REMAX Costa Rica](https://www.remax-costa-rica.com/) website.  

The scraper gathers detailed real estate data, stores it in a local database, and exposes a user-friendly dashboard for interactive filtering and exporting. Built as part of a **professional portfolio** to showcase skills in scraping, automation, backend data structuring, and dashboard creation — especially in the real estate domain.

---

## Features

### Scraping
- Loops through all public property listing pages.
- Extracts:
  - Title
  - Image
  - Listing URL
  - Date
  - Price
  - Property type
  - Location
  - Bedrooms, Bathrooms
  - Construction size, Lot size

### Storage
- Saves data to:
  - `SQLite` database for querying and filtering
  - `.xlsx` file for offline access or reporting

### Dashboard with Streamlit
- Filters by:
  - Location
  - Property Type
  - Bedrooms
  - **Price Range**
- Displays listings as visual cards (images, details, links)
- Allows exporting filtered results to Excel with one click

---

## Tech Stack

- `Python 3.11+`
- `requests`, `BeautifulSoup4`, `pandas`
- `sqlite3`, `xlsxwriter`
- `Streamlit` (for interactive dashboard)
- `Git + GitHub`
- Virtual environment with `venv`