import streamlit as st
from datetime import datetime
from database import get_all_clients, add_meeting

st.set_page_config(page_title="Meeting Notes", page_icon="📝", layout="wide")

st.title("📝 Meeting Notes")

clients_df = get_all_clients()
if clients_df.empty:
    st.warning("No clients available.")
    st.stop()

# Form to add meeting note
with st.form("meeting_notes_form"):
    client_dict = dict(zip(clients_df['name'], clients_df['id']))
    selected_client_name = st.selectbox("Select Client", list(client_dict.keys()))
    client_id = client_dict[selected_client_name]
    
    meeting_date = st.date_input("Meeting Date", datetime.now())
    notes = st.text_area("Meeting Notes / Discussion Summary", height=200, 
                         help="Include feature requests, bugs, complaints, support concerns, etc.")
    
    submitted = st.form_submit_button("Save Notes")
    
    if submitted:
        if notes.strip():
            add_meeting(client_id, meeting_date.strftime("%Y-%m-%d"), notes)
            st.success("Meeting notes saved successfully!")
            st.session_state['last_meeting_notes'] = notes
            st.session_state['last_client_id'] = client_id
            st.info("You can now go to the AI Task Generator to extract tasks from these notes.")
        else:
            st.error("Notes cannot be empty.")
