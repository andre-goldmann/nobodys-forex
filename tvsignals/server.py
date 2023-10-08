import uvicorn
from fastapi import FastAPI, Request, status
import sys

from pydantic import BaseModel

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI()

class SignalDto(BaseModel):
    symbol:str
    timestamp:str
    price:float
    sl:float
    tp:float
    indicator: str

@app.get("/")
async def read_root():
    message = f"Hello world! From FastAPI running on Uvicorn with Gunicorn. Using Python {version}"
    return {"message": message}

@app.post("/signal")
async def signals(signal:SignalDto):
    print(signal)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)