import streamlit as st
import pandas as pd
import sqlite3
from io import BytesIO

st.set_page_config(page_title="RE/MAX Property Dashboard", layout="wide")
st.title("RE/MAX Properties in Costa Rica")

@st.cache_data
def load_data():
    conn = sqlite3.connect("output/remax_properties.db")
    df = pd.read_sql_query("SELECT * FROM properties", conn)
    conn.close()
    return df

df = load_data()

def parse_price(p):
    try:
        return int(p.replace("$", "").replace(",", "").strip())
    except:
        return None

df["price_num"] = df["price"].apply(parse_price)

st.sidebar.header("🔍 Filter Listings")

locations = sorted(df["location"].dropna().unique())
selected_locations = st.sidebar.multiselect("Location", locations, default=locations)

types = sorted(df["property_type"].dropna().unique())
selected_types = st.sidebar.multiselect("Property Type", types, default=types)

bedroom_options = sorted(df["bedrooms"].dropna().unique())
selected_bedrooms = st.sidebar.multiselect("Bedrooms", bedroom_options, default=bedroom_options)

st.sidebar.markdown("---")
st.sidebar.subheader("Price Range")

min_price = int(df["price_num"].min()) if df["price_num"].notnull().any() else 0
max_price = int(df["price_num"].max()) if df["price_num"].notnull().any() else 1000000

selected_price = st.sidebar.slider("Select price range", min_price, max_price, (min_price, max_price))

filtered_df = df[
    (df["location"].isin(selected_locations)) &
    (df["property_type"].isin(selected_types)) &
    (df["bedrooms"].isin(selected_bedrooms)) &
    (df["price_num"] >= selected_price[0]) &
    (df["price_num"] <= selected_price[1])
]

st.markdown(f"### 🔎 Showing {len(filtered_df)} Properties")

for i in range(0, len(filtered_df), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(filtered_df):
            prop = filtered_df.iloc[i + j]
            with cols[j]:
                st.image(prop["image"], use_container_width=True)
                st.markdown(f"**{prop['title']}**")
                st.markdown(f"📍 {prop['location']}")
                st.markdown(f"💰 {prop['price']}")
                st.markdown(f"🛏️ {prop['bedrooms']}   |   🛁 {prop['bathrooms']}   |   📐 {prop['area']}")
                st.markdown(f"[🔗 View Property]({prop['url']})", unsafe_allow_html=True)

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='FilteredProperties')
    return output.getvalue()

st.sidebar.markdown("---")
st.sidebar.subheader("Export Results")

if not filtered_df.empty:
    excel_data = convert_df_to_excel(filtered_df)
    st.sidebar.download_button(
        label="Download Excel",
        data=excel_data,
        file_name="filtered_properties.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.sidebar.write("No properties to export.")
