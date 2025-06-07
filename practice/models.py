from pydantic import BaseModel

class TripPlan(BaseModel):
     city:str
     hotel:str
     route:str
    

class FlightCheck(BaseModel):
      isFlight:bool

class TripSuccess(BaseModel):
      message:str
      city:str
      hotel:str
      route:str
      budget:str
