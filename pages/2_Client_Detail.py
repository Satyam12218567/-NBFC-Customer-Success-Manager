import streamlit as st
import pandas as pd
from database import get_all_clients, get_client_by_id, get_tasks_for_client, get_meetings_for_client, get_emails_for_client

st.set_page_config(page_title="Client Detail", page_icon="🔍", layout="wide")

st.title("🔍 Client Detail")

clients_df = get_all_clients()
if clients_df.empty:
    st.warning("No clients found in the database.")
    st.stop()

# Select Client
client_dict = dict(zip(clients_df['name'], clients_df['id']))
selected_client_name = st.selectbox("Select Client", list(client_dict.keys()))
client_id = client_dict[selected_client_name]

if client_id:
    client = get_client_by_id(client_id)
    
    # Profile Header
    st.header(client['name'])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Account Manager", client['account_manager'])
    with col2:
        st.metric("Health Status", client['health_status'])
    with col3:
        st.metric("Revenue", f"${client['revenue']:,.2f}")
    with col4:
        st.metric("Billing Status", client['billing_status'])
        
    st.markdown(f"**Contact:** {client['contact_person']} ({client['email']}) | **Last Meeting:** {client['last_meeting_date']}")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Linked Tasks", "Meeting History", "Communication Logs", "Analytics"])
    
    with tab1:
        st.subheader("Open Tasks & Issues")
        tasks_df = get_tasks_for_client(client_id)
        if not tasks_df.empty:
            open_tasks = tasks_df[tasks_df['status'] != 'Completed']
            if not open_tasks.empty:
                st.dataframe(open_tasks[['title', 'category', 'priority', 'status', 'due_date']], use_container_width=True, hide_index=True)
            else:
                st.success("No open tasks for this client.")
        else:
            st.info("No tasks recorded.")
            
    with tab2:
        st.subheader("Meeting History")
        meetings_df = get_meetings_for_client(client_id)
        if not meetings_df.empty:
            for _, row in meetings_df.iterrows():
                with st.expander(f"Meeting on {row['date']}"):
                    st.write(row['notes'])
        else:
            st.info("No meetings recorded.")
            
    with tab3:
        st.subheader("Email/Communication Logs")
        emails_df = get_emails_for_client(client_id)
        if not emails_df.empty:
            for _, row in emails_df.iterrows():
                with st.expander(f"{row['date']} - {row['subject']}"):
                    st.write(row['body'])
        else:
            st.info("No emails logged.")
            
    with tab4:
        st.subheader("Client Specific Analytics")
        st.write("Revenue History & Usage stats would go here (Placeholder for future metrics)")
