from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Employee(Base):
    __tablename__ = "employee_attrition_dataset"
    
    Employee_ID = Column(Integer, primary_key=True, autoincrement=True)
    Age = Column(Integer)
    Gender = Column(String)
    Marital_Status = Column(String)
    Department = Column(String)
    Job_Role = Column(String)
    Job_Level = Column(Integer)
    Monthly_Income = Column(Integer)
    Hourly_Rate = Column(Integer)
    Years_at_Company = Column(Integer)
    Years_in_Current_Role = Column(Integer)
    Years_Since_Last_Promotion = Column(Integer)
    Work_Life_Balance = Column(Integer)
    Job_Satisfaction = Column(Integer)
    Performance_Rating = Column(Integer)
    Training_Hours_Last_Year = Column(Integer)
    Overtime = Column(String)
    Project_Count = Column(Integer)
    Average_Hours_Worked_Per_Week = Column(Integer)
    Absenteeism = Column(Integer)
    Work_Environment_Satisfaction = Column(Integer)
    Relationship_with_Manager = Column(Integer)
    Job_Involvement = Column(Integer)
    Distance_From_Home = Column(Integer)
    Number_of_Companies_Worked = Column(Integer)
    Attrition = Column(String)


