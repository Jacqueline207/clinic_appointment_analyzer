#File handles all the models in our database. Helps establishes schema and internal relationships
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, Date
from sqlalchemy.orm import declarative_base, relationship
import uuid

#create the declarative base
#This line creates a special base class that all my SQL Alchemy models must inherit from so that 
#sql alchemy knows they represent database tables. When assigned to DBModelBase, every model that 
#extends this class gets automatically registered and included when tables are created
DBModelBase = declarative_base()

#instead of a product model, I need patient and appointment models
class Patient(DBModelBase):
    __tablename__ = "patients"
    #this establishes that the class Patient maps to a database table called patients

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4())) # patient ID (UUID)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False) # make random between 18 to 80
    #status for no show
    #no show status is appointmment specific****
    primary_issue = Column(String(25), nullable=False) #checkup, followup, etc
    no_show_probability = Column(Float, nullable=False)

    appointments = relationship("Appointment", back_populates="patient")    
#appointment model
class Appointment(DBModelBase):
    __tablename__ = "appointments"
    #establishes that the class Appointment maps to a database table called appointments
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(Date, nullable=False) #im not sure if i can set nullable to false becuase we are going to use faker
    #which datat types should I be usingg
    week_day = Column(String(10),nullable=False)
    time_slot = Column(String(10), nullable=False)
    ###bring patient id, age, primary issue?
    patient_id = Column(String, ForeignKey("patients.id"))
    patient = relationship("Patient", back_populates="appointments")
    patient_age = Column(Integer, nullable=False)
    appointment_type = Column(String(25), nullable=False)
    scheduled_duration = Column(Integer, nullable=False) #should i make this a string or an integer
    actual_duration = Column(Integer, nullable=False)
    show_up_status = Column(Boolean, nullable=False)
    duration_difference = Column(Integer, nullable=False)

    

