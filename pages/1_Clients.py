import streamlit as st
import sqlite3
from database import get_all_clients, get_connection

st.set_page_config(page_title="Clients", page_icon="👥", layout="wide")

st.title("👥 NBFC Clients")

# Show all clients
clients_df = get_all_clients()
if not clients_df.empty:
    st.dataframe(clients_df[['name', 'account_manager', 'contact_person', 'email', 'revenue', 'billing_status', 'health_status']], use_container_width=True, hide_index=True)
else:
    st.write("No clients available.")
    
st.markdown("---")

# Add a new client
st.subheader("Add New Client")
with st.form("add_client_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Client Name")
        account_manager = st.text_input("Account Manager")
        contact_person = st.text_input("Contact Person")
        email = st.text_input("Email")
    with col2:
        revenue = st.number_input("Revenue", min_value=0.0, step=1000.0)
        billing_status = st.selectbox("Billing Status", ["Paid", "Pending", "Overdue"])
        health_status = st.selectbox("Health Status", ["Excellent", "Good", "At Risk", "Poor"])
        
    submitted = st.form_submit_button("Add Client")
    
    if submitted:
        if name and email:
            conn = get_connection()
            c = conn.cursor()
            c.execute('''
                INSERT INTO clients (name, account_manager, contact_person, email, revenue, billing_status, health_status, last_meeting_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, NULL)
            ''', (name, account_manager, contact_person, email, revenue, billing_status, health_status))
            conn.commit()
            conn.close()
            st.success(f"Client {name} added successfully!")
            st.rerun()
        else:
            st.error("Name and Email are required.")
