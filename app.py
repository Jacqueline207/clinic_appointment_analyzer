import streamlit as st
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Patient, Appointment


#create a database session helper so that application has a consistent and reusable way
#to create database sessions whenever it needs to read from or write to the database. 
#declaring a function only, not calling it

def get_session() -> Session:
    return SessionLocal()

#load_patients, and load_products to be responsibe for querying the database,

#filter patients by no shows, usefull to find the primary issue
def load_patients(profile_filter: str | None = None) ->list[Patient]:
    session = get_session()
    try:
        query = session.query(Patient)
        if profile_filter and  profile_filter != "all":
            query = query.filter(Patient.primary_issue == profile_filter)
        patients = query.order_by(Patient.id).all()
        return patients
    finally:
        session.close()

#appointment can look like;

def load_appointments() -> list[Appointment]:
    session = get_session()
    try:
        appointments = (
            session.query(Appointment)
            .order_by(Appointment.date, Appointment.time_slot)
            .all()
        )
        return appointments
    finally:
        session.close()

#changing the names I GOT THIS

def patients_to_dict(patient: Patient) -> dict:
    return {
        "id": patient.id, 
        "name": patient.name,
        "age": patient.age,
        "primary_issue": patient.primary_issue,
        "no_show_probability": patient.no_show_probability
    
    }

#include more
def appointments_to_dict(appointment: Appointment) -> dict:
    return {
        "id": appointment.id,
        "date": str(appointment.date),
        "week_day": appointment.week_day,
        "time_slot": appointment.time_slot,
        "patient_id" : appointment.patient_id,
        #looking up patient assigned to appointment
        "patient_age" : appointment.patient_age,
        "appointment_type": appointment.appointment_type,
        "scheduled_duration" : appointment.scheduled_duration,
        "actual_duration" : appointment.actual_duration,
        "show_up_status" : appointment.show_up_status,
        "duration_difference": appointment.duration_difference
    }

#starting the main application function
#sets up the streamlit page configuration and introduces the purpose of the dashboard to the user. 

def main() -> None:
    #to determine what data to display from the tables
    st.set_page_config(page_title="Patient Appointment Information", layout="wide")
    st.title("Health Track Clinic - Appointment Efficiency Analyzer")
    st.write(
        "Will be used to analyze no-show patterns, appointment durations, and scheduling"
    )
    
    patients = load_patients()
    appointments = load_appointments()

    #for the clinic
    st.subheader("Overview")
    total = len(appointments)
    showed_up = sum(1 for a in appointments if a.show_up_status)
    no_shows = total - showed_up

    #3 columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Appointments", total)
    col2.metric("Showed Up", showed_up)
    col3.metric("No-Shows", no_shows)

    #patient data

    st.subheader("Patient Profiles")
    issue_filter = st.selectbox(
        "Filter by primary issue", 
        ["all", "Checkup", "Follow-up", "Procedure", "Consultation"]
    )
    #show patient info, where patients = filtered patients
    patients = load_patients(profile_filter=issue_filter)
    st.dataframe([patients_to_dict(p) for p in patients])
    
    #appointments
    st.subheader("Appointments")
    st.dataframe([appointments_to_dict(a) for a in appointments])

if __name__ == "__main__": 
    main()

