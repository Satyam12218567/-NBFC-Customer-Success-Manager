import streamlit as st
from datetime import datetime
from database import get_all_clients, add_email
from email_utils import send_real_email

st.set_page_config(page_title="Email Hub", page_icon="📧", layout="wide")

st.title("📧 Email Hub")
st.markdown("*Log inbound communications or send real outbound emails to clients.*")

clients_df = get_all_clients()
if clients_df.empty:
    st.warning("No clients available.")
    st.stop()

with st.form("email_logger_form", clear_on_submit=False):
    client_dict = dict(zip(clients_df['name'], clients_df['id']))
    selected_client_name = st.selectbox("Select Client", list(client_dict.keys()))
    client_id = client_dict[selected_client_name]
    
    # Get client email
    client_data = clients_df[clients_df['id'] == client_id].iloc[0]
    client_email = client_data['email']
    
    st.markdown(f"**Client Email:** `{client_email}`")
    
    email_date = st.date_input("Date", datetime.now())
    subject = st.text_input("Email Subject")
    body = st.text_area("Email Body", height=200)
    
    st.markdown("---")
    st.subheader("Outbound Email Settings")
    send_real = st.checkbox("Actually send this email to the client via Gmail")
    
    sender_email = ""
    app_password = ""
    if send_real:
        st.warning("You must provide your Gmail address and a 16-letter Google App Password. Do NOT use your normal password.")
        col_a, col_b = st.columns(2)
        with col_a:
            sender_email = st.text_input("Your Gmail Address")
        with col_b:
            app_password = st.text_input("Google App Password", type="password")
            
    submitted = st.form_submit_button("Submit Email")
    
    if submitted:
        if subject.strip() and body.strip():
            # If sending real email
            if send_real:
                if sender_email and app_password:
                    with st.spinner("Sending email via Gmail..."):
                        success, msg = send_real_email(client_email, subject, body, sender_email, app_password)
                        if success:
                            st.success(f"📨 {msg}")
                        else:
                            st.error(f"Failed to send email: {msg}")
                            st.stop() # Stop if email fails, don't log it
                else:
                    st.error("Please provide your Gmail and App Password to send real emails.")
                    st.stop()
                    
            # 1. Log the email in database
            add_email(client_id, email_date.strftime("%Y-%m-%d"), subject, body)
            st.success("Email logged to client timeline successfully!")
            
            # 2. Automatically generate and save tasks in the background
            with st.spinner("Auto-extracting tasks from email..."):
                from llm_utils import generate_tasks_from_text
                from database import add_task
                
                email_text = f"Subject: {subject}\n\n{body}"
                tasks = generate_tasks_from_text(email_text)
                
                if tasks:
                    for t in tasks:
                        add_task(client_id, t.get('title', 'Untitled'), t.get('category', 'Support'), 
                                 t.get('priority', 'Medium'), t.get('due_date', email_date.strftime("%Y-%m-%d")), 
                                 "Open", "Email")
                    st.success(f"Magic! ✨ {len(tasks)} tasks were automatically extracted and added to your Task Tracker.")
                else:
                    st.info("No actionable tasks were found in this email.")
        else:
            st.error("Subject and Body are required.")
