from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import pickle
import json


with open('Kisan_model.pickle','rb') as f:
            __model = pickle.load(f)

app  = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["*"],
)

class Kisan(BaseModel):
    Nitrogen:float
    Phosphorus:float
    Potassium:float
    temperature:float
    humidity:float
    ph:float
    rainfal:float


@app.get('/')
async def home():
    return "Welcome"

@app.post('/api/predict')
async def model(data:Kisan):
    
    data = data.dict()
    
    N = data['Nitrogen']
    P = data['Phosphorus']
    K = data['Potassium']
    t = data['temperature']
    h = data['humidity']
    p = data['ph']
    r = data['rainfal']
    
    # return __model.predict([[N,P,K,t,h,p,r]])[0]
    result = __model.predict([[N,P,K,t,h,p,r]])[0]
    data = {"crop":result}
    
    value = json.dumps(data)
    
    new_val = json.loads(value)
    
    return new_val


port = os.environ.get('PORT', 5000)

if '__name__' == '__main__':
    uvicorn.run(app,'127.0.0.1',port)

# Hello this is just for checking