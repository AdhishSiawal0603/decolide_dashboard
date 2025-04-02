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
    response.raise_for_status()
    data = response.json()

    if isinstance(data, list) and len(data) > 0:
        df = pd.DataFrame(data)
        df.rename(columns={
            "Order date": "Order Date",
            "Order ID": "Order ID",
            "Customer name": "Customer Name",
            "Customer phone": "Customer Phone",
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
            "PAN": "PAN Card",
            "Status": "Status"
        }, inplace=True)
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
                st.markdown(f"**📞 Customer phone:** {row.get('Customer Phone', 'N/A')}")
                st.markdown(f"**📦 Product:** [{row.get('Product Type', 'N/A')}]({row.get('Product Link', '#')})")
                st.markdown(f"**🪚 Customization:** {row.get('Customization', 'N/A')}")

            with col2:
                st.markdown(f"**💰 Final price:** ₹{row.get('Final Price', 'N/A')}")
                st.markdown(f"**💵 Initial paid:** ₹{row.get('Initial Paid', 'N/A')}")
                st.markdown(f"**📍 Delivery location:** {row.get('Delivery Address', 'N/A')}")
            
            # Order Status Dropdown
            status_options = ["Confirmed", "Manufacturing Stage 1", "Manufacturing Stage 2", "Dispatched"]
            current_status = row.get("Status", "Confirmed")  # Default to 'Confirmed' if not set
            status_index = status_options.index(current_status) if current_status in status_options else 0
            
            selected_status = st.selectbox("🔄 Update Order Status", status_options, index=status_index, key=f"status_{i}")

            # Upload PAN Card
            pan_key = f"pan_{i}"
            pan_file = st.file_uploader(f"📎 Upload PAN Card for {row.get('Customer Name', 'N/A')}", type=["png", "jpg", "pdf"], key=pan_key)

            # Upload Tracking Document
            tracking_key = f"tracking_{i}"
            tracking_file = st.file_uploader(f"📄 Upload Tracking Document for {row.get('Customer Name', 'N/A')}", type=["png", "jpg", "pdf"], key=tracking_key)

            # Save uploaded files and status update
            save_button = st.button(f"💾 Save Changes for Order {row.get('Order ID', 'N/A')}", key=f"save_{i}")
            
            if save_button:
                pan_base64 = base64.b64encode(pan_file.read()).decode() if pan_file else ""
                tracking_base64 = base64.b64encode(tracking_file.read()).decode() if tracking_file else ""

                data_to_send = {
                    "order_id": row.get("Order ID", "N/A"),
                    "pan_card_link": pan_base64,
                    "tracking_doc_link": tracking_base64,
                    "status": selected_status
                }
                
                try:
                    response = requests.post(API_URL, json=data_to_send)
                    response.raise_for_status()
                    result = response.json()

                    if result.get("status") == "success":
                        st.success(f"✅ Changes saved successfully for Order {row.get('Order ID', 'N/A')}!")
                    else:
                        st.error(f"❌ Failed to save changes: {result.get('message')}")
                except Exception as e:
                    st.error(f"❌ Error updating order: {e}")
