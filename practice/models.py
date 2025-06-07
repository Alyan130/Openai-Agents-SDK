from pydantic import BaseModel

class TripPlan(BaseModel):
     city:str
     hotel:str
     route:str
    

class CheckDetails(BaseModel):
      isCity:bool
      isHotel:bool
      isRoute:bool

class TripSuccess(BaseModel):
      message:str
      city:str
      hotel:str
      route:str
      budget:str
