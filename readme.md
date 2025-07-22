# Real Estate Web Scraper – REMAX Costa Rica

This project is a **Python-based web scraper** built to automatically extract property listings from the official [REMAX Costa Rica](https://www.remax-costa-rica.com/) website. The goal is to create a structured database of real estate listings that can be used for analysis, visualizations, or as the backend of a larger real estate product.

> **Note:** This is a **work in progress** and is being built as part of a professional portfolio to showcase skills in scraping, automation, and data structuring—especially in the real estate domain.

---

## What it does so far

1. Scrapes property listings from REMAX Costa Rica’s public listings.
2. Extracts key data such as:
   - Title
   - Image
   - URL
   - Date
   - Price
   - Property type
   - Location
   - Bedrooms, bathrooms, construction size, lot size
3. Saves the results in:
   - `.xlsx` (Excel) format
   - `SQLite` database for further querying
4. Allows exporting from the database into a fresh Excel file at any time.

---

## Technologies Used

- `Python 3.11+`
- `requests`
- `BeautifulSoup`
- `pandas`
- `openpyxl`
- `sqlite3`
- `virtualenv`
- `Git + GitHub`
- Coming soon: `FastAPI` to expose data through a RESTful API

---

## Steps Completed

1. Created a virtual environment with `virtualenv`
2. Initialized Git repository and connected to GitHub
3. Functional script that loops through all property listing pages
4. Extracts both summary and detailed data from listing pages
5. Saves results into Excel spreadsheet
6. Inserts data into a `SQLite` database

---

## Next Steps

- [ ] **Normalize prices and convert them to numeric format** to allow range filtering
- [ ] **Enable filtering by price, location, bedrooms, etc.** from the terminal (CLI)
- [ ] **Add support for other real estate platforms**, such as [Pura Vida Paradise](https://www.puravidaparadise.com/)
- [ ] **Develop a RESTful API using FastAPI** to expose the listings
- [ ] Add basic testing (unit + scraping)
- [ ] Write technical documentation for database structure and codebase
