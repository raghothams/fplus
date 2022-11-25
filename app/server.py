from datetime import date, datetime, time, timedelta
from typing import Union, List
from fastapi import FastAPI
from pydantic import BaseModel
from prophet import Prophet
import pandas as pd
import arrow

app = FastAPI()


class RequestModel(BaseModel):
    ds: List[str] 
    y: List[float] 
    periods: int 

class ResponseModel(BaseModel):
    ds: List[date]
    y: List[float]



def fplus_predict(x,y,periods=1):

    x_dt = [arrow.get(dt_val).date() for dt_val in x]
    print(x_dt)
    df = pd.DataFrame(list(zip(x_dt, y)), columns=["ds", "y"])
    print(df)
    
    m = Prophet()
    # m.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    m.fit(df)
    
    future = m.make_future_dataframe(periods=periods)
    forecast = m.predict(future)
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
    
    return forecast


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/forecast", response_model=ResponseModel)
def forecast(data: RequestModel):
    forecast = fplus_predict(data.ds, data.y, data.periods)
    print(forecast.iloc[-data.periods:,]['ds'])
    print(forecast.iloc[-data.periods:,]['yhat'])

    response = ResponseModel(
        ds=forecast.iloc[-data.periods:,]['ds'].tolist(),
        y=forecast.iloc[-data.periods:,]['yhat'].tolist()
    )

    print(response.dict())
    return response






