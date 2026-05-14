import sqlite3
import os
import pandas as pd
from datetime import datetime, timedelta

DB_NAME = "nbfc_csm.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            account_manager TEXT,
            contact_person TEXT,
            email TEXT,
            revenue REAL,
            billing_status TEXT,
            health_status TEXT,
            last_meeting_date DATE
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            date DATE,
            notes TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            date DATE,
            subject TEXT,
            body TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            title TEXT,
            category TEXT,
            priority TEXT,
            due_date DATE,
            status TEXT,
            source TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')
    
    # Check if we need to seed
    c.execute("SELECT COUNT(*) FROM clients")
    if c.fetchone()[0] == 0:
        seed_data(conn)
        
    conn.commit()
    conn.close()

def seed_data(conn):
    c = conn.cursor()
    
    clients_data = [
        ("ABC Finance", "Alice Smith", "John Doe", "john@abcfinance.com", 150000.0, "Paid", "Good", (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")),
        ("Sunrise Capital", "Alice Smith", "Sarah Lee", "sarah@sunrisecap.com", 85000.0, "Pending", "At Risk", (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d")),
        ("Bharat Lending", "Bob Jones", "Raj Patel", "raj@bharatlending.in", 220000.0, "Paid", "Excellent", (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")),
        ("QuickLoan NBFC", "Bob Jones", "Emily Chen", "emily@quickloan.com", 45000.0, "Overdue", "Poor", (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")),
        ("FinTrust Microfinance", "Charlie Davis", "Vikram Singh", "vikram@fintrust.org", 110000.0, "Paid", "Good", (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d")),
        ("Urban Credit Services", "Charlie Davis", "Maria Garcia", "maria@urbancredit.com", 95000.0, "Paid", "Good", (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")),
    ]
    
    c.executemany('''
        INSERT INTO clients (name, account_manager, contact_person, email, revenue, billing_status, health_status, last_meeting_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', clients_data)
    
    # Tasks
    tasks_data = [
        (1, "Fix report generation delay", "Bug", "High", (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"), "Open", "Meeting"),
        (2, "Discuss new loan module", "Proposal", "Medium", (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"), "In Progress", "Email"),
        (3, "Follow up on invoice", "Support", "High", (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"), "Open", "System"),
        (4, "System integration training", "Training", "Low", (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"), "Open", "Meeting"),
    ]
    c.executemany('''
        INSERT INTO tasks (client_id, title, category, priority, due_date, status, source)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', tasks_data)
    
    # Meetings
    meetings_data = [
        (1, (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"), "Discussed Q3 roadmap. Client happy but wants faster reports."),
        (2, (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d"), "Client expressed concerns about API downtime. Needs urgent follow up."),
    ]
    c.executemany('''
        INSERT INTO meetings (client_id, date, notes)
        VALUES (?, ?, ?)
    ''', meetings_data)

# Helper functions for UI
def get_all_clients():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM clients", conn)
    conn.close()
    return df

def get_client_by_id(client_id):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM clients WHERE id = {client_id}", conn)
    conn.close()
    return df.iloc[0] if not df.empty else None

def get_tasks_for_client(client_id):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM tasks WHERE client_id = {client_id}", conn)
    conn.close()
    return df

def get_all_tasks():
    conn = get_connection()
    df = pd.read_sql_query("SELECT t.*, c.name as client_name FROM tasks t JOIN clients c ON t.client_id = c.id", conn)
    conn.close()
    return df

def add_meeting(client_id, date, notes):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO meetings (client_id, date, notes) VALUES (?, ?, ?)", (client_id, date, notes))
    c.execute("UPDATE clients SET last_meeting_date = ? WHERE id = ?", (date, client_id))
    conn.commit()
    conn.close()

def add_task(client_id, title, category, priority, due_date, status, source):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO tasks (client_id, title, category, priority, due_date, status, source)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (client_id, title, category, priority, due_date, status, source))
    conn.commit()
    conn.close()

def update_task_status(task_id, status):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()

def get_meetings_for_client(client_id):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM meetings WHERE client_id = {client_id} ORDER BY date DESC", conn)
    conn.close()
    return df

def add_email(client_id, date, subject, body):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO emails (client_id, date, subject, body) VALUES (?, ?, ?, ?)", (client_id, date, subject, body))
    conn.commit()
    conn.close()
    
def get_emails_for_client(client_id):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM emails WHERE client_id = {client_id} ORDER BY date DESC", conn)
    conn.close()
    return df
