import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_real_email(to_email, subject, body, sender_email, app_password):
    """Sends an email using Gmail's SMTP server."""
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login
        server.login(sender_email, app_password)
        
        # Send
        server.send_message(msg)
        server.quit()
        return True, "Email sent successfully!"
    except Exception as e:
        return False, str(e)
