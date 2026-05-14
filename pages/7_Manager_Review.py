import streamlit as st
import pandas as pd
from database import get_all_clients, get_all_tasks

st.set_page_config(page_title="Manager Review", page_icon="📊", layout="wide")

st.title("📊 Manager Review Dashboard")
st.markdown("High-level overview of all account portfolios.")

clients_df = get_all_clients()
tasks_df = get_all_tasks()

if not clients_df.empty:
    # Prepare consolidated data
    review_data = []
    for _, client in clients_df.iterrows():
        cid = client['id']
        c_tasks = tasks_df[tasks_df['client_id'] == cid] if not tasks_df.empty else pd.DataFrame()
        
        open_count = len(c_tasks[c_tasks['status'] == 'Open']) if not c_tasks.empty else 0
        complaints_count = len(c_tasks[(c_tasks['category'] == 'Complaint') & (c_tasks['status'] != 'Completed')]) if not c_tasks.empty else 0
        
        health_icon = "🟢" if client['health_status'] == "Excellent" else "🟡" if client['health_status'] == "Good" else "🟠" if client['health_status'] == "At Risk" else "🔴"
        
        review_data.append({
            "Client": client['name'],
            "Manager": client['account_manager'],
            "Health": f"{health_icon} {client['health_status']}",
            "Last Meeting": client['last_meeting_date'],
            "Open Tasks": open_count,
            "Active Complaints": complaints_count,
            "Revenue": f"${client['revenue']:,.2f}",
            "Billing": client['billing_status']
        })
        
    review_df = pd.DataFrame(review_data)
    
    # Highlight risky rows
    def highlight_risk(row):
        if "🔴" in row['Health'] or row['Active Complaints'] > 0 or row['Billing'] == 'Overdue':
            return ['background-color: #ffcccc'] * len(row)
        return [''] * len(row)
        
    st.dataframe(review_df.style.apply(highlight_risk, axis=1), use_container_width=True, hide_index=True)
    
else:
    st.info("No data available for review.")
