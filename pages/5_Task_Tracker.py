import streamlit as st
import pandas as pd
from database import get_all_tasks, update_task_status, get_all_clients

st.set_page_config(page_title="Task Tracker", page_icon="📋", layout="wide")

st.title("📋 Task Tracker")

tasks_df = get_all_tasks()

if not tasks_df.empty:
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        client_filter = st.selectbox("Filter by Client", ["All"] + list(tasks_df['client_name'].unique()))
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "Open", "In Progress", "Completed"])
    with col3:
        priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    with col4:
        category_filter = st.selectbox("Filter by Category", ["All"] + list(tasks_df['category'].unique()))

    # Apply filters
    filtered_df = tasks_df.copy()
    if client_filter != "All":
        filtered_df = filtered_df[filtered_df['client_name'] == client_filter]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['status'] == status_filter]
    if priority_filter != "All":
        filtered_df = filtered_df[filtered_df['priority'] == priority_filter]
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
        
    st.write(f"Showing {len(filtered_df)} tasks.")
    
    # Display tasks with ability to update status
    for _, row in filtered_df.iterrows():
        with st.container():
            col_a, col_b, col_c, col_d, col_e = st.columns([3, 2, 1, 1, 2])
            with col_a:
                st.markdown(f"**{row['title']}**")
                st.caption(f"Client: {row['client_name']} | Source: {row['source']}")
            with col_b:
                st.write(f"Due: {row['due_date']}")
            with col_c:
                st.write(row['category'])
            with col_d:
                # Color code priority
                color = "red" if row['priority'] == "High" else "orange" if row['priority'] == "Medium" else "green"
                st.markdown(f"<span style='color:{color}; font-weight:bold;'>{row['priority']}</span>", unsafe_allow_html=True)
            with col_e:
                new_status = st.selectbox("Status", ["Open", "In Progress", "Completed"], 
                                          index=["Open", "In Progress", "Completed"].index(row['status']), 
                                          key=f"status_{row['id']}")
                if new_status != row['status']:
                    update_task_status(row['id'], new_status)
                    st.rerun()
            st.markdown("---")
else:
    st.info("No tasks found.")
