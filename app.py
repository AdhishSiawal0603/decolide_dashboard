import streamlit as st

# Dashboard Title
st.title("Decolide Orders Processing Dashboard")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["📋 Order Summary", "🏭 Manufacturing", "🚚 Dispatch"])

# Sample Order Data (Replace with real data later)
orders = [
    {"Order ID": 101, "Customer": "Rohan", "Status": "Manufacturing", "Address": "Mumbai"},
    {"Order ID": 102, "Customer": "Priya", "Status": "Dispatched", "Address": "Delhi"},
    {"Order ID": 103, "Customer": "Amit", "Status": "Manufacturing", "Address": "Bangalore"},
]

# Display Order Summary
if page == "📋 Order Summary":
    st.header("All Orders")
    for order in orders:
        with st.expander(f"Order {order['Order ID']} - {order['Customer']}"):
            st.write(f"**Status:** {order['Status']}")
            st.write(f"**Address:** {order['Address']}")
            if st.button(f"View Details {order['Order ID']}"):
                st.write("🔍 Order details coming soon!")

# Manufacturing Section
elif page == "🏭 Manufacturing":
    st.header("Manufacturing Details")
    order_id = st.selectbox("Select Order ID", [order["Order ID"] for order in orders if order["Status"] == "Manufacturing"])
    st.write(f"🔧 Customization details for **Order {order_id}** will be displayed here.")

# Dispatch Section
elif page == "🚚 Dispatch":
    st.header("Dispatch Details")
    order_id = st.selectbox("Select Order ID", [order["Order ID"] for order in orders if order["Status"] == "Dispatched"])
    st.write(f"📦 Delivery details for **Order {order_id}** will be displayed here.")
    
    # File Upload for PAN Card
    st.subheader("Upload PAN Card")
    uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg", "pdf"])
    if uploaded_file is not None:
        st.success("✅ File uploaded successfully!")
