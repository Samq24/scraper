import sqlite3
import pandas as pd

conn = sqlite3.connect("output/remax_properties.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM properties")
total = cursor.fetchone()[0]

print(f"🔢 Total de propiedades en la base de datos: {total}")


# cursor.execute("SELECT title, url, price, location FROM properties ORDER BY id DESC LIMIT 5")
# for row in cursor.fetchall():
#     print(row)

# search_term = "%Nosara%"  # usa % para buscar con LIKE
# cursor.execute("SELECT title, price, location FROM properties WHERE location LIKE ?", (search_term,))
# for row in cursor.fetchall():
#     print(row)


conn = sqlite3.connect("output/remax_properties.db")
df = pd.read_sql_query("SELECT * FROM properties", conn)
conn.close()

df.to_excel("output/remax_export.xlsx", index=False)
print("📤 Exportado a Excel: remax_export.xlsx")

conn.close()
