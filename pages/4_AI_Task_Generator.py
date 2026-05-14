import streamlit as st
import pandas as pd
from database import get_all_clients, add_task
from llm_utils import generate_tasks_from_text

st.set_page_config(page_title="AI Task Generator", page_icon="🤖", layout="wide")

st.title("🤖 AI Task Generator")
st.markdown("Extract actionable tasks from meeting notes or emails using AI.")

clients_df = get_all_clients()
if clients_df.empty:
    st.warning("No clients available.")
    st.stop()

client_dict = dict(zip(clients_df['name'], clients_df['id']))

# Pre-fill if coming from another page
default_client = list(client_dict.keys())[0]
default_notes = ""

if 'last_client_id' in st.session_state:
    for name, cid in client_dict.items():
        if cid == st.session_state['last_client_id']:
            default_client = name
            break
if 'last_meeting_notes' in st.session_state:
    default_notes = st.session_state['last_meeting_notes']

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input Source Text")
    selected_client_name = st.selectbox("Select Client", list(client_dict.keys()), index=list(client_dict.keys()).index(default_client))
    client_id = client_dict[selected_client_name]
    
    source_type = st.selectbox("Source Type", ["Meeting Note", "Email", "Manual"])
    text_to_analyze = st.text_area("Paste Notes or Email Body", value=default_notes, height=300)
    
    if st.button("Generate Tasks 🚀"):
        if text_to_analyze.strip():
            with st.spinner("Analyzing text and generating tasks..."):
                tasks = generate_tasks_from_text(text_to_analyze)
                st.session_state['generated_tasks'] = tasks
        else:
            st.error("Please provide text to analyze.")

with col2:
    st.subheader("Generated Tasks")
    if 'generated_tasks' in st.session_state and st.session_state['generated_tasks']:
        tasks = st.session_state['generated_tasks']
        
        # Display editable tasks
        edited_tasks = []
        for i, task in enumerate(tasks):
            with st.expander(f"Task {i+1}: {task.get('title', 'Untitled')}", expanded=True):
                title = st.text_input(f"Title {i}", value=task.get('title', ''))
                category = st.selectbox(f"Category {i}", ["Bug", "Feature Request", "Complaint", "Proposal", "Training", "Support"], 
                                        index=["Bug", "Feature Request", "Complaint", "Proposal", "Training", "Support"].index(task.get('category', 'Support')) if task.get('category') in ["Bug", "Feature Request", "Complaint", "Proposal", "Training", "Support"] else 5)
                priority = st.selectbox(f"Priority {i}", ["High", "Medium", "Low"], 
                                        index=["High", "Medium", "Low"].index(task.get('priority', 'Medium')) if task.get('priority') in ["High", "Medium", "Low"] else 1)
                due_date = st.text_input(f"Due Date {i} (YYYY-MM-DD)", value=task.get('due_date', ''))
                
                edited_tasks.append({
                    "title": title,
                    "category": category,
                    "priority": priority,
                    "due_date": due_date,
                    "status": "Open",
                    "source": source_type
                })
                
        if st.button("Save Tasks to Tracker 💾"):
            for t in edited_tasks:
                add_task(client_id, t['title'], t['category'], t['priority'], t['due_date'], t['status'], t['source'])
            st.success("Tasks saved successfully! Check the Task Tracker.")
            # Clear state
            del st.session_state['generated_tasks']
            if 'last_meeting_notes' in st.session_state:
                del st.session_state['last_meeting_notes']
            st.rerun()
    else:
        st.info("Click 'Generate Tasks' to see results here.")
