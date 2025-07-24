# RE/MAX Real Estate Dashboard

A complete real estate data project that scrapes property listings from [RE/MAX Costa Rica](https://www.remax-costa-rica.com), stores them in a local **SQLite** database, and displays the results in a responsive **Streamlit dashboard**.

**Live App**: [scraper-rs.streamlit.app](https://scraper-rs.streamlit.app/)

---

## Features

- Automated web scraping using `requests` and `BeautifulSoup`  
- Data storage in a structured SQLite database  
- Interactive dashboard with filters by:
  - Keyword (title or location)
  - Location
  - Property Type
  - Bedrooms
  - Price range

- Property cards showing:
  - Title, location, price
  - Bedrooms, bathrooms, size
  - Image preview + direct listing URL

- Export filtered results to Excel  
- Dynamic price comparison chart (min, max, avg) by zone  
- Extra charts:
  - Properties by bedrooms
  - Properties by type  
- Summary tab with quick KPIs (count, average price)

---

## Tech Stack

- **Python 3.11+**
- **Streamlit**
- **SQLite**
- **BeautifulSoup**
- **Pandas**
- **Plotly**
- **XlsxWriter**