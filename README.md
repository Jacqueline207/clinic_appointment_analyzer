# Health Track Clinic - Analyzing Appointment Efficiency

A data simulation dashboard project that models no-show behavior at a clinic. Build with Python, SQLAlchemy, and Streamlit.

---

### What it Does

This project simulates 60 days of clinic appointments accross 300 patients. It was built to explore how factors like patient age, gender, the type of appointment, and time of day influence no-show rates - a real problem in the field of healthcare operations.

---

### Features

-Generates 300 realistic patient profiles using the Faker library
-Simulates appoinments across 60 days with randomized but realistic no-show probabilities
-Applies behavioral logic: older patients are more reliable, late day slots see higher no-show rates
-Stores all data in a local SQLite database via SQLAlchemy
-Exports appointment data to a CSV file
-Displays an interactive dashboard with appoinment metrics, patient filtering, and data tables

---

### Tech Stack
-Python as the core language
-SQLAlchmey for ORM and database management
-SQlite for the local database
-Streamlit for the interactive dashboard
-Faker for synthetic patient name generation
-NumPy for probability calculations 
-Pandas for CSV export

---

## Project Structure

```
├── models.py           # SQLAlchemy models for Patient and Appointment tables
├── database.py         # Database connection and session setup
├── seed.py             # Seeds the database with 300 patients and 60 days of appointments
├── app.py              # Streamlit dashboard
├── export.py           # Exports appointment table to CSV
├── requirements.txt    # Project dependencies
```

---

## How to Run

**1. Clone the repo**
**2. Install dependencies**
```bash
python seed.py
```
**3. Seed the database**
```bash
streamlit run app.py
```
**4. Launch the dashboard**
```bash 
streamlit run app.py
```

## Dashboard Overview

- **Overview** - total appointments, how many patients showed up, and total no-shows
- **Patient Profiles** - filterable table by primary issue (Check up, Follow-up, Procedure, Consultation)
- **Appointmments** - full appointment log with date, time slot, durtion, and show-up status

---

## Key Concepts

- Relational database design with foreign keys and ORM relationships
- Probabilistic simulation using Numpy
- Data seeding and session management with SQLAlchemy
- Building interactive data apps with Streamlt
- Exporting database tables to CSV with Pandas