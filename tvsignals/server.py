import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
# Bellow the import create a job that will be executed on background
from fastapi.responses import JSONResponse
import sys

from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker

version = f"{sys.version_info.major}.{sys.version_info.minor}"

engine = create_engine('postgresql://nobodysforex:pwd@db:6432/trading-db')
Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

class Base(DeclarativeBase):
    pass

class Trade(Base):
    __tablename__ = "Trades"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(6))
    type: Mapped[str] = mapped_column(String(6))
    entry: Mapped[float]
    sl: Mapped[float]
    tp: Mapped[float]
    lots: Mapped[float]
    spread: Mapped[float] = mapped_column(nullable=True, default=0.0)
    tradeid: Mapped[int] = mapped_column(nullable=True, default=0)
    stamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    # werden erst nach der Erstellung des Trades gesetzt
    activated: Mapped[str] = mapped_column(nullable=True, default="")
    openprice: Mapped[float] = mapped_column(nullable=True, default=0.0)
    swap: Mapped[float] = mapped_column(nullable=True, default=0.0)
    profit: Mapped[float] = mapped_column(nullable=True, default=0.0)
    closed: Mapped[str] = mapped_column(nullable=True, default="")
    commision: Mapped[float] = mapped_column(nullable=True, default="")
    strategy: Mapped[str] = mapped_column(nullable=True, default="")

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

def storeTrade(trade: Trade):
    session.add(trade)
    session.commit()

@app.post("/signal")
async def signals(signal:SignalDto):
    print(signal)
    storeTrade(Trade(
        symbol=signal.symbol,
        type=signal.type,
        entry=signal.entry,
        sl=signal.sl,
        tp=signal.tp,
        lots=0.5,
        commision=0.0,
        strategy=signal.strategy
    ))

#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=80)