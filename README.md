# Voice-Based Assistant for Monitoring Public Welfare Scheme Usage

This project demonstrates how to integrate **Azure SQL Database, Azure OpenAI, Azure Speech-to-Text, and FastAPI/Streamlit** into a complete application. The assistant enables non-technical government officers to query structured welfare scheme data (e.g., MGNREGA, PMAY, Ujjwala) using **natural language (text/voice)**.

---

## Features

- **Natural Language Querying**: Users can ask questions in plain English.  
- **Voice Input**: Queries can be submitted by speech via Azure Speech-to-Text.  
- **NL→SQL Conversion**: Azure OpenAI translates natural language into SQL SELECT queries.  
- **Database Backend**: Normalized schema hosted on **Azure SQL Database**.  
- **Summarized Results**: Outputs are returned as natural language + tables.  
- **Charts & Visuals**: Numeric/comparison queries are displayed with Plotly charts in Streamlit.  
- **Database Explorer**: Users can view tables, schema metadata, and run SELECT queries directly.  
- **Security**:  
  - Regular login → only NL/voice queries  
  - DB creds login → SQL explorer access (read-only)  
  - SQL injection protection (SELECT-only guard)  
- **Cloud Integration**:  
  - App Service hosts backend  
  - Azure SQL with VNet/NSG for private access  
  - Geo-redundant backup enabled  
  - App Insights + Monitoring

---

## Architecture

```
User (Streamlit) --> FastAPI Backend --> Azure OpenAI
                                  \-> Azure Speech-to-Text
                                  \-> Azure SQL Database
```

- **Frontend**: Streamlit (Query Page + Explorer Page)  
- **Backend**: FastAPI (Dockerized, deployed via Azure App Service)  
- **Database**: Azure SQL
- **AI Services**: Azure OpenAI (NL→SQL, Summarization), Azure Speech (Voice Input)  

---

## API Endpoints

- `GET /health` → Service check  
- `POST /nl_query` → Natural language query → SQL → results  
- `POST /voice_query` → Voice file → text → SQL → results  
- `POST /direct_sql` → Run SELECT query directly (read-only)  
- `GET /metadata` → Schema & tables metadata  

---

## Database Schema

Main tables:
- **citizens**(citizen_id, name, age, gender, district, …)  
- **schemes**(scheme_id, name, sector, …)  
- **enrollments**(enrollment_id, citizen_id, scheme_id, date_enrolled, …)  
- **disbursements**(disbursement_id, citizen_id, scheme_id, amount, date, …)  
- **officers**(officer_id, name, role, …)  

---

## Security Notes

- Only `SELECT` queries allowed in `/direct_sql` (guarded).  
- Database explorer requires DB login (read-only).  
- VNet + NSG restrict Azure SQL access to App Service only.  
- Geo-redundant backups enabled for DB reliability.  

---

## Future Improvements

- Multilingual support (translate queries + responses)  
- Automated PDF/Excel report exports  
- Offline mode with cached queries  
- Notification system (alerts if disbursement below target)  
- Advanced monitoring (latency, GPT usage, SQL performance) 
