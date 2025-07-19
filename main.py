import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Crear carpeta de salida si no existe
os.makedirs("output", exist_ok=True)

# URL del listado principal
url = "https://www.remax-costa-rica.com/Properties-Propiedades/"

# Encabezado para evitar bloqueos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Hacer la solicitud HTTP
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Buscar propiedades
properties = soup.find_all("div", class_="property_listing_blog")

# Lista de resultados
data = []

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

        data.append({
            "Title": title,
            "URL": link,
            "Image": image,
            "Date": date,
            "Description": description
        })
    except Exception as e:
        print("Error processing a property:", e)

# Convertir a DataFrame
df = pd.DataFrame(data)

# Guardar en Excel
output_path = os.path.join("output", "remax_properties_page1.xlsx")
df.to_excel(output_path, index=False)
print(f"Scraping complete. Data saved to {output_path}")
