# RE/MAX Costa Rica Property Scraper & Dashboard

This is an end-to-end real estate data project built with **Python**, focused on **web scraping, data analysis**, and **interactive dashboards**.

It scrapes property listings from [remax-costa-rica.com](https://www.remax-costa-rica.com/), stores the data in a **SQLite database**, and visualizes it using **Streamlit**.

---

## Features

### Web Scraping
- Scrapes all pages of property listings (with pagination)
- Extracts detailed info:
  - Title, image, description
  - Price, type, location
  - Bedrooms, bathrooms, area, lot size
- Handles missing data gracefully
- Saves data to SQLite and Excel

### Data Dashboard
Built with **Streamlit**:
- Filter by location, property type, bedrooms, and price
- Search by keyword in title or location
- Download filtered results as Excel
- Visualize:
  - Price comparison by zone (min, max, average)
  - Number of properties by zone
  - Average price by property type
- Summary indicators: total listings, zones, price ranges


---

## Technologies Used

- `Python 3.11`
- `BeautifulSoup` for scraping
- `requests` for HTTP
- `pandas` for data manipulation
- `SQLite3` for local database
- `Streamlit` for dashboard
- `Plotly` for data visualization
- `xlsxwriter` for Excel export