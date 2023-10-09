import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
# Bellow the import create a job that will be executed on background
from fastapi.responses import JSONResponse
import sys

from pydantic import BaseModel

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

class SignalDto(BaseModel):
    symbol:str
    timestamp:str
    type:str
    entry:float
    sl:float
    tp:float
    strategy: str

@app.get("/")
async def read_root():
    message = f"Hello world! From FastAPI running on Uvicorn with Gunicorn. Using Python {version}"
    return {"message": message}

@app.post("/signal")
async def signals(signal:SignalDto):
    print(signal)
    #storeTrade(Trade(
    #    symbol=signal.symbol,
    #    type=signal.type,
    #    entry=signal.entry,
    #    sl=signal.sl,
    #    tp=signal.tp,
    #    lots=0.5,
    #    strategy=signal.strategy
    #))

#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=80)