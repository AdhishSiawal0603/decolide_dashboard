import streamlit as st
import requests
import pandas as pd
import base64

# Streamlit Page Config
st.set_page_config(page_title="Decolide Vendor Dashboard", layout="wide")

# API URL from Google Apps Script
API_URL = "https://script.google.com/macros/s/AKfycbx37U8_-DBdjIYflNhFwmmUin4o2ZnbPpeEAcx--LF-NqosXdqss_j8PFTg83A0ncHw/exec"

# Fetch Data from Google Sheets API
try:
    response = requests.get(API_URL)
    response.raise_for_status()  # Ensure no HTTP errors
    data = response.json()

    if isinstance(data, list) and len(data) > 0:
        df = pd.DataFrame(data)

        # Ensure column names are correctly mapped
        df.rename(columns={
            "Order date": "Order Date",
            "Order ID": "Order ID",
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
            "Delivery address": "Delivery Address",
            "Expected dispatch date": "Dispatch Date",
            "Tracking document": "Tracking Document",
            "PAN": "PAN Card"
        }, inplace=True)

        # Ensure Order ID is not empty
        df = df.dropna(subset=["Order ID"])

    else:
        st.warning("⚠️ No valid data found. Check API response.")
        df = pd.DataFrame()

except Exception as e:
    st.error(f"❌ Error fetching data: {e}")
    df = pd.DataFrame()

# Dashboard Title
st.title("📊 Decolide Order Processing")

if df.empty:
    st.warning("No data available.")
else:
    for i, row in df.iterrows():
        with st.expander(f"🎯 Order {row.get('Order ID', 'N/A')} - {row.get('Customer Name', 'N/A')}"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**📅 Order date:** {row.get('Order Date', 'N/A')}")
                st.markdown(f"**📅 Required delivery:** {row.get('Expected Delivery', 'N/A')}")
                st.markdown(f"**📦 Product:** [{row.get('Product Type', 'N/A')}]({row.get('Product Link', '#')})")
                st.markdown(f"**🪚 Customization:** {row.get('Customization', 'N/A')}")

            with col2:
                st.markdown(f"**💰 Final price:** ₹{row.get('Final Price', 'N/A')}")
                st.markdown(f"**💵 Initial paid:** ₹{row.get('Initial Paid', 'N/A')}")
                st.markdown(f"**📍 Delivery location:** {row.get('Delivery Location', 'N/A')}")
                st.markdown(f"**🏠 Delivery address:** {row.get('Delivery Address', 'N/A')}")

            st.markdown(f"**🚛 Expected Dispatch Date:** {row.get('Dispatch Date', 'N/A')}")

            # Upload PAN Card
            pan_key = f"pan_{i}"
            pan_file = st.file_uploader(f"📎 Upload PAN Card for {row.get('Customer Name', 'N/A')}", type=["png", "jpg", "pdf"], key=pan_key)

            # Upload Tracking Document
            tracking_key = f"tracking_{i}"
            tracking_file = st.file_uploader(f"📄 Upload Tracking Document for {row.get('Customer Name', 'N/A')}", type=["png", "jpg", "pdf"], key=tracking_key)

            # Save uploaded files
            if pan_file or tracking_file:
                save_button = st.button(f"💾 Save Documents for Order {row.get('Order ID', 'N/A')}", key=f"save_{i}")

                if save_button:
                    # Convert files to base64
                    pan_base64 = base64.b64encode(pan_file.read()).decode() if pan_file else ""
                    tracking_base64 = base64.b64encode(tracking_file.read()).decode() if tracking_file else ""

                    # Send Data to API
                    data_to_send = {
                        "order_id": row.get("Order ID", "N/A"),
                        "pan_card_link": pan_base64,
                        "tracking_doc_link": tracking_base64
                    }

                    try:
                        response = requests.post(API_URL, json=data_to_send)
                        response.raise_for_status()
                        result = response.json()

                        if result.get("status") == "success":
                            st.success(f"✅ Documents saved successfully for Order {row.get('Order ID', 'N/A')}!")
                        else:
                            st.error(f"❌ Failed to save documents: {result.get('message')}")

                    except Exception as e:
                        st.error(f"❌ Error uploading documents: {e}")
