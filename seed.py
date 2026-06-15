#Importing packages and set up faker
from faker import Faker
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Patient, Appointment

import random
import uuid
import numpy as np
from datetime import date, timedelta

fake = Faker()

"""
this prepares the file to create data for the database. Faker for realistic text, 
SessionLocal to open database sessions, and Patient to insert data into a table
"""

TIME_SLOTS = [
    "9:00AM",
    "10:00AM",
    "11:00AM",
    "1:00PM",
    "2:00PM",
    "3:00PM",
    "4:00PM"
]

APPOINTMENT_TYPES = {
    "Checkup" : {"base_duration": 20, "variability": 10},
    "Follow-up": {"base_duration": 15, "variability": 5},
    "Procedure": {"base_duration": 45, "variability": 25},
    "Consultation": {"base_duration": 30, "variability": 15}
}

BASE_NO_SHOW_RATE = 0.15

#determine appointment types with properties that store base duration and variability
"""
Checkup: base duration = 20, variability = 10
Follow-up: base duration = 15, variability = 5
Procedure: base duration = 45, variability = 25
Consultation: base duration = 30, variability = 15
"""

##using Faker will add data to patient and to appointments
#generate 300 patient profiles with their id, age, no_show_status, patient primary issue, and no show probability
def seed_patients(session: Session): 
    #patients set as lists generates 300 make sure its random between 18 to 80
    patients = [] 

    for _ in range(300): #for the 300 patients
        #set age using random.randint
        age = random.randint(18,80)
        #now the case study says
        no_show_rate = BASE_NO_SHOW_RATE
        #now check if paitent age is above 60, older patients are more reliable so would drop from .15 to .10
        if age > 60:
            no_show_rate *= .7
        
        #determining the gender of patient using np random
        '''
        random generates a number greater than 0.5, multiply
        the no-show by 120%
        '''
        #random.random generates a random floating-point number
        determine_gender = np.random.random() #flip a coin depending on greater or less than 0.5 and then decides to inc by 20%
        if determine_gender > 0.5:
            no_show_rate *= 1.2

        #Applying the no show probability for generating patient data
        """
        The no show probability should be formatted using Numpy's
        uniform method with a low of 0.8 and a high of 1.2 and a size of 0.3
        """
        no_show_probability = float(np.random.uniform(low=0.8, high=1.2)) * no_show_rate * .3 #0.3 is the size or scale factor
        primary_issue = random.choice(["Checkup", "Follow-up", "Procedure", "Consultation"])

        #now including all of patient data which should be 
        """
        patient ID, patient name, age, primary issue, and no show probability
        """

        patient = Patient(
            id=str(uuid.uuid4()),
            name=fake.name(),
            age=age,
            primary_issue=primary_issue,
            no_show_probability=no_show_probability
        )
        session.add(patient)
        patients.append(patient)  
    return patients


def seed_appointments(session: Session, patients):
    appointments = [] #appointments as list

    #storing 60 days worth of appointments
    start_date = date.today() #start date
    #time_delta represents duration of difference between two points in time

    #determine the new date (time period forward)
    #a way to store 60 days' worth of appointments
    for new_day in range(60):
        current_date = start_date + timedelta(days=new_day)
        #accessing the name name of weekday using strftime("%A")
        weekday = current_date.strftime("%A")
        '''
        if the current day is a weekend day, there should be fewer appointments
        in in python checks exist inside a collection
        '''
        is_weekend = weekday in ["Saturday", "Sunday"]

        #set the time slots
        """
        What the case study says:
        Per each time slot:
        Generate a random number of appointments set that day
        Choose a patient at random from our patient array
        Set the patient's appointment type
        Set the scheduled duration based on the appointment type
        Set the actual duration by using Python's max method, with the initial value as 10 and the second value with the appointment type's variability in mind (i.e, duration_info['base_duration'] + random.randint(-duration_info['variability'], duration_info['variability'])
        Determine if the patient showed up based on their no show probability and a random multiplier
        Increase the no show probability if the appointment occurs in a time slot at '3:00PM' or '4:00pm' ONLY if random.random is greater than their no show probability * 1.3
        """
        for time_slot in TIME_SLOTS:
            if is_weekend:
                appointments_today = random.randint(1, 5)
            else:
                appointments_today = random.randint(3, 8)
            #inside the loop still for time_slots
            for _ in range(appointments_today):
                #random patient
                patient = random.choice(patients)
                appointment_type = patient.primary_issue
                #duration info from base duration based on the appointment type
                duration_information = APPOINTMENT_TYPES[appointment_type]
                scheduled_duration = duration_information["base_duration"]
                actual_duration = max(
                    10,
                    #from negative up to positive at random
                    scheduled_duration + random.randint(
                        -duration_information["variability"],
                        duration_information["variability"]
                    )
                )
                no_show_probability = patient.no_show_probability
                '''
                Determine if the patient showed up based on their no show probability and a
                random multiplier, Increase the no show probability if the appointment 
                occurs in a time slot at '3:00PM' or '4:00pm' ONLY if random.random is greater 
                than their no show probability * 1.3
                '''                
                #final determmination of showed
                if time_slot in ["3:00PM", "4:00PM"]:
                    if random.random() > no_show_probability * 1.3:
                        no_show_probability = min(no_show_probability * 1.3, 1.0)
                        
                #probability simulation. False or True depending on random float between 0 and 1 and whatever the no show probability is
                showed_up = random.random() > no_show_probability
                appointment = Appointment(
                    id=str(uuid.uuid4()), 
                    date=current_date,
                    week_day=weekday,
                    time_slot=time_slot,
                    patient_id=patient.id, #.id to access correctly
                    patient=patient,
                    patient_age= patient.age,
                    appointment_type= appointment_type,
                    scheduled_duration=scheduled_duration,
                    actual_duration= actual_duration, ###calculated this
                    show_up_status= showed_up,
                    duration_difference=(actual_duration - scheduled_duration)
                )
                session.add(appointment)
                appointments.append(appointment)
    return appointments #returns appointments

def main() -> None:
    session: Session = SessionLocal()
    try:
        patients = seed_patients(session)
        seed_appointments(session, patients)
        session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    main()
