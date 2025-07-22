import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="RE/MAX Property Dashboard", layout="wide")
st.title("RE/MAX Properties in Costa Rica")

@st.cache_data
def load_data():
    conn = sqlite3.connect("output/remax_properties.db")
    df = pd.read_sql_query("SELECT * FROM properties", conn)
    conn.close()
    return df

df = load_data()

st.sidebar.header("Filter Listings")

locations = sorted(df["location"].dropna().unique())
selected_locations = st.sidebar.multiselect("Location", locations, default=locations)

types = sorted(df["property_type"].dropna().unique())
selected_types = st.sidebar.multiselect("Property Type", types, default=types)

bedroom_options = sorted(df["bedrooms"].dropna().unique())
selected_bedrooms = st.sidebar.multiselect("Bedrooms", bedroom_options, default=bedroom_options)

filtered_df = df[
    (df["location"].isin(selected_locations)) &
    (df["property_type"].isin(selected_types)) &
    (df["bedrooms"].isin(selected_bedrooms))
]

st.markdown(f"### 🔎 Showing {len(filtered_df)} Properties")

# Visualización tarjetas
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
