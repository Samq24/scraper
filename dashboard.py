import streamlit as st
import pandas as pd
import sqlite3
from io import BytesIO
import plotly.express as px

st.set_page_config(page_title="🏘️ RE/MAX Property Dashboard", layout="wide")

tab1, tab2 = st.tabs(["Property Listings", "📊 Price Summary by Zone"])

with tab1:
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

    st.sidebar.subheader("Keyword Search")
    search_term = st.sidebar.text_input("Search by title or location", "")

    locations = sorted(df["location"].dropna().unique())
    selected_locations = st.sidebar.multiselect("Location", locations, default=locations)

    types = sorted(df["property_type"].dropna().unique())
    selected_types = st.sidebar.multiselect("Property Type", types, default=types)

    bedroom_options = sorted(df["bedrooms"].dropna().unique())
    selected_bedrooms = st.sidebar.multiselect("Bedrooms", bedroom_options, default=bedroom_options)

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

    if search_term.strip():
        keyword = search_term.lower()
        filtered_df = filtered_df[
            filtered_df["title"].str.lower().str.contains(keyword, na=False) |
            filtered_df["location"].str.lower().str.contains(keyword, na=False)
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
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_filtered_properties_tab1"
        )
    else:
        st.sidebar.write("No properties to export.")


with tab2:
    st.title("Market Insights")

    if filtered_df.empty:
        st.warning("No properties match the selected filters.")
    else:
        zone_stats = filtered_df.groupby("location")["price_num"].agg(["min", "max", "mean"]).reset_index()
        zone_stats.columns = ["Location", "Min Price", "Max Price", "Average Price"]

        st.dataframe(zone_stats, use_container_width=True)

        st.subheader("Price Comparison by Zone")
        zone_stats = filtered_df.groupby("location")["price_num"].agg(["min", "max", "mean"]).reset_index()
        zone_stats.columns = ["Location", "Min Price", "Max Price", "Average Price"]

        melted = zone_stats.melt(id_vars="Location", var_name="Metric", value_name="Price")
        fig = px.bar(melted, x="Location", y="Price", color="Metric", barmode="group",
                     title="Min / Max / Average Price by Zone")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Price Distribution")
        hist_fig = px.histogram(filtered_df, x="price_num", nbins=30, title="Distribution of Property Prices")
        hist_fig.update_layout(xaxis_title="Price (USD)", yaxis_title="Number of Properties")
        st.plotly_chart(hist_fig, use_container_width=True)

        st.subheader("Properties by Type")
        type_counts = filtered_df["property_type"].value_counts().reset_index()
        type_counts.columns = ["Property Type", "Count"]
        type_fig = px.bar(type_counts, x="Property Type", y="Count", title="Property Counts by Type")
        st.plotly_chart(type_fig, use_container_width=True)
