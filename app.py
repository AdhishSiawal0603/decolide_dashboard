import streamlit as st
import requests
import pandas as pd

# Streamlit Page Config
st.set_page_config(page_title="Decolide Orders Dashboard", layout="wide")

# Fetch Data from Google Sheets API
API_URL = "https://script.google.com/macros/s/AKfycbyTo4AAC5W7AB6GeQ49WDwv2e7FkxAzAUt9ilFmDGMvav0fELa334qkb3jW67IOsjE3/exec"

try:
    response = requests.get(API_URL)
    data = response.json()
    df = pd.DataFrame(data)

    # Rename columns (update these if actual names are different)
    df.rename(columns={
        "Order date": "Order Date",
        "Customer name": "Customer Name",
        "Expected delivery date": "Expected Delivery",
        "Product type": "Product Type",
        "Product link": "Product Link",
        "Customization requirement": "Customization",
        "Final price": "Final Price",
        "Initial paid": "Initial Paid",
        "Manufacturing cost": "Manufacturing Cost",
        "Shipping cost": "Shipping Cost",
        "Delivery location": "Delivery Location",
        "Processing status": "Status",
        "Expected dispatch date": "Dispatch Date",
        "Tracking link": "Tracking Link"
    }, inplace=True)

except Exception as e:
    st.error(f"Error fetching data: {e}")
    df = pd.DataFrame()  # Empty dataframe to prevent crashes

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["📋 Order Summary", "🏭 Manufacturing", "🚚 Dispatch"])

# Order Summary Page
if page == "📋 Order Summary":
    st.header("📋 Order Summary")
    if df.empty:
        st.warning("No data available.")
    else:
        for _, row in df.iterrows():
            with st.expander(f"🛍 Order {row.get('Order Date', 'N/A')} - {row.get('Customer Name', 'N/A')}"):
                st.markdown(f"**Status:** {row.get('Status', 'N/A')}")
                st.progress(0.5 if row.get('Status') == "In Progress" else 1.0)

# Manufacturing Page
elif page == "🏭 Manufacturing":
    st.header("🏭 Manufacturing Details")
    if df.empty:
        st.warning("No data available.")
    else:
        for _, row in df.iterrows():
            with st.expander(f"🛠 {row.get('Order Date', 'N/A')} - {row.get('Customer Name', 'N/A')}"):
                st.markdown(f"**Product:** [{row.get('Product Type', 'N/A')}]({row.get('Product Link', '#' )})")
                st.markdown(f"**Customization:** {row.get('Customization', 'N/A')}")

# Dispatch Page
elif page == "🚚 Dispatch":
    st.header("🚚 Dispatch Details")
    if df.empty:
        st.warning("No data available.")
    else:
        for i, row in df.iterrows():
            with st.expander(f"📦 {row.get('Order Date', 'N/A')} - {row.get('Customer Name', 'N/A')}"):
                st.markdown(f"**Final Price:** ₹{row.get('Final Price', 'N/A')}")
                st.markdown(f"**Initial Paid:** ₹{row.get('Initial Paid', 'N/A')}")
                st.markdown(f"**Shipping Cost:** ₹{row.get('Shipping Cost', 'N/A')}")
                st.markdown(f"**Delivery Location:** {row.get('Delivery Location', 'N/A')}")
                
                # Unique key to prevent Streamlit error
                pan_key = f"pan_{i}"
                st.file_uploader(f"Upload PAN Card for {row.get('Customer Name', 'N/A')}", type=["png", "jpg", "pdf"], key=pan_key)

