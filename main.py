import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
import sqlite3

os.makedirs("output", exist_ok=True)

base_url = "https://www.remax-costa-rica.com/Properties-Propiedades"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

data = []
page = 1
max_pages = 10

while True:
    if page == 1:
        url = base_url + "/"
    else:
        url = f"{base_url}/page/{page}/"

    print(f"Scraping page {page} -> {url}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    properties = soup.find_all("div", class_="property_listing_blog")

    if not properties:
        print("No more properties found. Stopping.")
        break

    for prop in properties:
        try:
            title_tag = prop.find("a", class_="blog_unit_title")
            image_tag = prop.find("img")
            date_tag = prop.find("div", class_="blog_unit_meta")
            description_tag = prop.find("div", class_="listing_details")

            title = title_tag.get_text(strip=True) if title_tag else "N/A"
            link = title_tag["href"] if title_tag and title_tag.has_attr("href") else "N/A"
            image = image_tag["src"] if image_tag and image_tag.has_attr("src") else "N/A"
            date = date_tag.get_text(strip=True) if date_tag else "N/A"
            description = description_tag.get_text(strip=True) if description_tag else "N/A"

            detail_response = requests.get(link, headers=headers)
            detail_soup = BeautifulSoup(detail_response.content, "html.parser")

            price_tag = detail_soup.find("div", class_="price_area")
            price = price_tag.get_text(strip=True) if price_tag else "N/A"

            type_tag = detail_soup.find("div", class_="property_title_label actioncat")
            property_type = type_tag.get_text(strip=True) if type_tag else "N/A"

            location_tag = detail_soup.find("div", class_="property_categs")
            location = location_tag.get_text(separator=" ", strip=True) if location_tag else "N/A"

            overview_wrapper = detail_soup.find("div", class_="property-page-overview-details-wrapper")
            bedrooms = bathrooms = area = lot_size = "N/A"

            if overview_wrapper:
                lists = overview_wrapper.find_all("ul", class_="overview_element")
                for ul in lists:
                    li_items = ul.find_all("li")
                    if len(li_items) >= 2:
                        value_text = li_items[1].get_text(strip=True).lower()

                        if "bedroom" in value_text:
                            bedrooms = value_text.replace("bedrooms", "").replace("bedroom", "").strip()
                        elif "bathroom" in value_text:
                            bathrooms = value_text.replace("bathrooms", "").replace("bathroom", "").strip()
                        elif "m²" in value_text or "m2" in value_text:
                            area = value_text.strip()
                        elif "lot" in value_text or "land" in value_text:
                            lot_size = value_text.strip()

            data.append({
                "Title": title,
                "URL": link,
                "Image": image,
                "Date": date,
                "Short Description": description,
                "Price": price,
                "Property Type": property_type,
                "Location": location,
                "Bedrooms": bedrooms,
                "Bathrooms": bathrooms,
                "Area": area,
                "Lot Size": lot_size
            })

        except Exception as e:
            print("Error processing property:", e)

    page += 1
    if page > max_pages:
        print("Reached max page limit. Consider increasing it.")
        break

df = pd.DataFrame(data)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_path = os.path.join("output", f"remax_properties_{timestamp}.xlsx")
df.to_excel(output_path, index=False)
print(f"Scraping complete. Data saved to {output_path}")


conn = sqlite3.connect("output/remax_properties.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    url TEXT UNIQUE,
    image TEXT,
    date TEXT,
    short_description TEXT,
    price TEXT,
    property_type TEXT,
    location TEXT,
    bedrooms TEXT,
    bathrooms TEXT,
    area TEXT,
    lot_size TEXT
)
""")

inserted = 0
for prop in data:
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO properties (
                title, url, image, date, short_description,
                price, property_type, location, bedrooms,
                bathrooms, area, lot_size
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prop["Title"], prop["URL"], prop["Image"], prop["Date"], prop["Short Description"],
            prop["Price"], prop["Property Type"], prop["Location"], prop["Bedrooms"],
            prop["Bathrooms"], prop["Area"], prop["Lot Size"]
        ))
        if cursor.rowcount > 0:
            inserted += 1
    except Exception as e:
        print(f"Error insertando propiedad {prop['Title']}: {e}")

conn.commit()
conn.close()
print(f"Datos guardados en SQLite: output/remax_properties.db")
print(f"Propiedades insertadas: {inserted}")
