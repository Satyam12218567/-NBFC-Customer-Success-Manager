import streamlit as st
import pandas as pd
import plotly.express as px
from database import init_db, get_all_clients, get_all_tasks

st.set_page_config(
    page_title="NBFC Customer Success Manager",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

st.title("🏢 NBFC Customer Success Manager")
st.markdown("Welcome to the MVP Dashboard for NBFC client management.")

# Fetch data
clients_df = get_all_clients()
tasks_df = get_all_tasks()

if not clients_df.empty:
    # KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Clients", len(clients_df))
    with col2:
        open_tasks = len(tasks_df[tasks_df['status'] == 'Open']) if not tasks_df.empty else 0
        st.metric("Open Tasks", open_tasks)
    with col3:
        complaints = len(tasks_df[tasks_df['category'] == 'Complaint']) if not tasks_df.empty else 0
        st.metric("Pending Complaints", complaints)
    with col4:
        st.metric("Monthly Revenue", f"${clients_df['revenue'].sum():,.2f}")
    with col5:
        overdue = len(clients_df[clients_df['billing_status'] == 'Overdue'])
        st.metric("Overdue Accounts", overdue)
        
    st.markdown("---")
    
    # Charts Row
    st.subheader("Analytics")
    chart_col1, chart_col2, chart_col3 = st.columns(3)
    
    with chart_col1:
        if not tasks_df.empty:
            fig1 = px.pie(tasks_df, names='status', title='Tasks by Status', hole=0.4)
            st.plotly_chart(fig1, use_container_width=True)
            
    with chart_col2:
        fig2 = px.pie(clients_df, names='health_status', title='Client Health Distribution', 
                      color='health_status', color_discrete_map={'Excellent':'green', 'Good':'lightgreen', 'At Risk':'orange', 'Poor':'red'})
        st.plotly_chart(fig2, use_container_width=True)
        
    with chart_col3:
        fig3 = px.bar(clients_df, x='name', y='revenue', title='Revenue by Client')
        st.plotly_chart(fig3, use_container_width=True)
        
    st.markdown("---")
    
    # Client Summary Table
    st.subheader("Client Overview")
    display_df = clients_df[['name', 'account_manager', 'health_status', 'last_meeting_date', 'revenue', 'billing_status']]
    # Add open tasks count
    if not tasks_df.empty:
        task_counts = tasks_df[tasks_df['status'] == 'Open'].groupby('client_id').size().reset_index(name='open_tasks')
        clients_with_tasks = pd.merge(clients_df, task_counts, left_on='id', right_on='client_id', how='left')
        clients_with_tasks['open_tasks'] = clients_with_tasks['open_tasks'].fillna(0).astype(int)
        display_df = clients_with_tasks[['name', 'account_manager', 'health_status', 'last_meeting_date', 'open_tasks', 'revenue', 'billing_status']]
        
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.info("No clients found. Please add clients or wait for seed data initialization.")
