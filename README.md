# NBFC Customer Success Manager (MVP)

deployment link - https://ms8sokp3o4wvrqqzekaglm.streamlit.app/

A Customer Success Management platform built for a software company providing core banking products to NBFC (Non-Banking Financial Company) clients.

## Problem Statement
Account managers handling multiple NBFC clients need a centralized platform to track meetings, complaints, feature requests, and customer health. Existing CRMs are often too generic. This MVP provides a tailored solution with AI-powered task generation from meeting notes and emails.

## Features
- **Dashboard**: KPI metrics and visual charts for a high-level overview.
- **Client Management**: Add and view NBFC clients, their revenue, and health status.
- **Client Detail View**: Consolidated timeline of meetings, emails, and linked tasks per client.
- **Meeting Notes & Email Simulation**: Log communications directly to the client profile.
- **AI Task Generator**: Extracts actionable tasks, priorities, and categories from text using the Gemini API (with a rule-based fallback).
- **Task Tracker**: Manage task statuses (Open, In Progress, Completed).
- **Manager Review Dashboard**: A bird's eye view for team leads to spot at-risk accounts quickly.

## Tech Stack
- **Frontend/Backend**: Streamlit (Python)
- **Database**: SQLite (built-in)
- **Data Visualization**: Plotly, Pandas
- **AI Integration**: Google Generative AI (Gemini 1.5 Flash)

## Setup Instructions

1. **Clone the repository** (or navigate to the folder).
2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```
3. **(Optional) Configure Gemini API**:
   Create a `.streamlit/secrets.toml` file in the root directory and add your key:
   ```toml
   GOOGLE_API_KEY = "your_api_key_here"
   ```
   *Note: If no API key is provided, the app will elegantly fall back to a rule-based NLP system for task extraction.*
4. **Run the App**:
   ```bash
   streamlit run app.py
   ```
   The database will automatically initialize with realistic seed data on the first run.

## Future Scope
- **Real Email Integration**: Connect to Microsoft Graph API or Gmail API.
- **Authentication & RBAC**: Implement login and role-based access control (Manager vs. Admin).
- **Notifications**: Automated alerts for overdue tasks or poor client health.
- **Advanced Analytics**: Deeper usage and adoption metrics.
