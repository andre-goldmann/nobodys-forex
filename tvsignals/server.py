import enum
import logging
import os
import sys
from typing import Optional

import ecs_logging
import pandas as pd
import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
# Bellow the import create a job that will be executed on background
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import Enum
from sqlalchemy import String, DateTime, UniqueConstraint
from sqlalchemy import create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker

load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

engine = create_engine(os.environ['POSTGRES_URL'], pool_size=10, max_overflow=0)
Session = sessionmaker(bind=engine)
app = FastAPI()

symbols = ["AUDUSD", "AUDCHF", "AUDJPY", "AUDNZD", "CHFJPY", "EURUSD", "EURCHF", "EURNZD", "GBPUSD", "GBPCAD", "GBPCHF", "GBPNZD",  "XAGUSD", "USDCAD", "USDCHF", "XRPUSD"]
strategies = ["NNR",
              "NNR_WITHOUT_REG",

              "Multiple Logistic Regression",
              "Multiple Logistic Regression_WITHOUT_REG",

              "Turtle Soup",
              "Turtle Soup_WITHOUT_REG",

              "MTI",
              "MTI_WITHOUT_REG",

              "SuperTrend AI",
              "SuperTrend AI_WITHOUT_REG",

              "Super AI Trend",
              "Super AI Trend_WITHOUT_REG",

              "70% Strategy",

              "STD-Filtered-Close",
              "STD-Filtered-Close_WITHOUT_REG",

              "SSL Hybrid",
              "SSL Hybrid_WITHOUT_REG",

              "AI Volume Supertrend",
              "SSL + Wave Trend Strategy",

              "RedK-SMA-SMA",
              "RedK-SMA-SMA_WITHOUT_REG",

              "AI Volume Supertrend-WMA",
              "AI Volume Supertrend-WMA_WITHOUT_REG",

              "VHMA",
              "VHMA_WITHOUT_REG",

              "T3Fvma",
              "T3Fvma_WITHOUT_REG",

              "SentimentRangeMa",
              "SentimentRangeMa_WITHOUT_REG",

              "GaussianChannelTrendAI",
              "GaussianChannelTrendAI_WITHOUT_REG",

              "T3-LocallyWeightedRegression",
              "T3-LocallyWeightedRegression_WITHOUT_REG",

              "T3-HmaKahlman",
              "T3-HmaKahlman_WITHOUT_REG",

              "T3-JMaCrossover",
              "T3-JMaCrossover_WITHOUT_REG",

              "T3-MachineLearningLogisticRegression",
              "T3-MachineLearningLogisticRegression_WITHOUT_REG",

              "T3-GapFilling",
              "T3-GapFilling_WITHOUT_REG",

              "T3-EvwmaVwapMacd",
              "T3-EvwmaVwapMacd_WITHOUT_REG",

              "T3-BollingerBandsPinbar",
              "T3-BollingerBandsPinbar_WITHOUT_REG",

              "T3-TrendAI",
              "T3-TrendAI_WITHOUT_REG",

              "T3-NNFX",
              "T3-NNFX_WITHOUT_REG",

              "T3-EfficientTrendStepMod",
              "T3-EfficientTrendStepMod_WITHOUT_REG",

              "T3-AroonBased",
              "T3-AroonBased_WITHOUT_REG",

              "T3-EmaStrategy",
              "T3-EmaStrategy_WITHOUT_REG",

              "SOTT-Lorentzian",
              "SOTT-Lorentzian_WITHOUT_REG",

              "RSS_WMA",
              "RSS_WMA_WITHOUT_WITHOUT_REG",

              "T3-MesaPhasor",
              "T3-MesaPhasor_WITHOUT_REG",

              "T3-SupportAndResistanceLevels",
              "T3-SupportAndResistanceLevels_WITHOUT_REG",

              "T3-Eams",
              "T3-Eams_WITHOUT_REG",
              
              "T3-VolumeDifferenceDeltaCycleOscillator",
              "T3-VolumeDifferenceDeltaCycleOscillator_WITHOUT_REG",

              "T3-MacdScalp",
              "T3-MacdScalp_WITHOUT_REG",

              "T3-DiCrossingDaily",
              "T3-DiCrossingDaily_WITHOUT_REG",

              "T3-HalfTrend",
              "T3-HalfTrend_WITHOUT_REG",

              "T3-BernoulliEntropyFunction",
              "T3-BernoulliEntropyFunction_WITHOUT_REG",

              "T3-LinearTrend",
              "T3-LinearTrend_WITHOUT_REG",

              "T3-UtBot",
              "T3-UtBot_WITHOUT_REG",

              "T3-PivotPointSuperTrend",
              "T3-PivotPointSuperTrend_WITHOUT_REG",

              "T3-AntiBreakout",
              "T3-AntiBreakout_WITHOUT_REG",

              "T3-Lube",
              "T3-Lube_WITHOUT_REG",

              "T3-ThirdWave",
              "T3-ThirdWave_WITHOUT_REG",

              "T3-PinBarStrategy",
              "T3-PinBarStrategy_WITHOUT_REG",

              "T3-ReversalFinder",
              "T3-ReversalFinder_WITHOUT_REG",

              "T3-MacdHistogram-LLTDEMA",
              "T3-MacdHistogram-LLTDEMA_WITHOUT_REG",

              "T3-MacdHistogram-TDEMA",
              "T3-MacdHistogram-TDEMA_WITHOUT_REG",
              
              "T3-MacdHistogram-DEMA",
              "T3-MacdHistogram-DEMA_WITHOUT_REG",

              "T3-MacdHistogram-EMA",
              "T3-MacdHistogram-EMA_WITHOUT_REG",

              "T3-MacdHistogram-THMA",
              "T3-MacdHistogram-THMA_WITHOUT_REG",

              "T3-MacdHistogram-ZLEMA",
              "T3-MacdHistogram-ZLEMA_WITHOUT_REG",

              "T3-MacdHistogram-ZLTEMA",
              "T3-MacdHistogram-ZLTEMA_WITHOUT_REG",

              "T3-NeutronixAi",
              "T3-NeutronixAi_WITHOUT_REG",

              "T3-NeutronixSwing",
              "T3-NeutronixSwing_WITHOUT_REG",

              "T3-NeutronixScalping",
              "T3-NeutronixScalping_WITHOUT_REG",

              "T3-ThreeCommasBotStrategy-EMA",
              "T3-ThreeCommasBotStrategy-EMA_WITHOUT_REG",

              "T3-ThreeCommasBotStrategy-HEMA",
              "T3-ThreeCommasBotStrategy-HEMA_WITHOUT_REG",

              "T3-ThreeCommasBotStrategy-SMA",
              "T3-ThreeCommasBotStrategy-SMA_WITHOUT_REG",

              "T3-ThreeCommasBotStrategy-HMA",
              "T3-ThreeCommasBotStrategy-HMA_WITHOUT_REG",

              "T3-ThreeCommasBotStrategy-WMA",
              "T3-ThreeCommasBotStrategy-WMA_WITHOUT_REG",

              "T3-ThreeCommasBotStrategy-DEMA",
              "T3-ThreeCommasBotStrategy-DEMA_WITHOUT_REG",
              
              "T3-ThreeCommasBotStrategy-VWMA",
              "T3-ThreeCommasBotStrategy-VWMA_WITHOUT_REG",

              "T3-ThreeCommasBotStrategy-VWAP",
              "T3-ThreeCommasBotStrategy-VWAP_WITHOUT_REG",

              "T3-ThreeCommasBotStrategy-T3",
              "T3-ThreeCommasBotStrategy-T3_WITHOUT_REG",

              "T3-MomentumBasedZigZag",
              "T3-MomentumBasedZigZag_WITHOUT_REG",

              "T3-DekidakaAshiSignals",
              "T3-DekidakaAshiSignals_WITHOUT_REG",

              "T3-SuperTrendCleaned",
              "T3-SuperTrendCleaned_WITHOUT_REG",

              "T3-ScaledNormalizedVector",
              "T3-ScaledNormalizedVector_WITHOUT_REG",

              "T3-RangeFilters",
              "T3-RangeFilters_WITHOUT_REG",

              "T3-NeutronixDCAemu",
              "T3-NeutronixDCAemu_WITHOUT_REG",

              "T3-UhlMASystem",
              "T3-UhlMASystem_WITHOUT_REG",

              "T3-LlorensActivator",
              "T3-LlorensActivator_WITHOUT_REG",

              "T3-CustomSuperTrendCleaned",
              "T3-CustomSuperTrendCleaned_WITHOUT_REG",

              "T3-BilateralStochasticOscillator",
              "T3-BilateralStochasticOscillator_WITHOUT_REG",

              "T3-NickRypockTrailingReverse",
              "T3-NickRypockTrailingReverse_WITHOUT_REG",

              "T3-GridLike",
              "T3-GridLike_WITHOUT_REG",

              "AdxCrossover_M15",
              "AdxCrossover_H1",
              "AdxCrossover_H4",

              "ADXEMA14_M15",
              "ADXEMA14_H1",
              "ADXEMA14_H4",

              "AdxRsi_M15",
              "AdxRsi_H1",
              "AdxRsi_H4",

              "AroonAdx_M15",
              "AroonAdx_H1",
              "AroonAdx_H4",

              "AroonIndicator_M15",
              "AroonIndicator_H1",
              "AroonIndicator_H4",

              "AwesomeOscillator_M15",
              "AwesomeOscillator_H1",
              "AwesomeOscillator_H4",

              "AwesomeOscillatorSaucer_M15",
              "AwesomeOscillatorSaucer_H1",
              "AwesomeOscillatorSaucer_H4",

              "BladeRunner_M15",
              "BladeRunner_H1",
              "BladeRunner_H4",

              "BollingerBandsAndRSI_M15",
              "BollingerBandsAndRSI_H1",
              "BollingerBandsAndRSI_H4",

              "BollingerBandsAndRSI2_M15",
              "BollingerBandsAndRSI2_H1",
              "BollingerBandsAndRSI2_H4",

              "CciMacdPsar_M15",
              "CciMacdPsar_H1",
              "CciMacdPsar_H4",

              "CciMovingAverage_M15",
              "CciMovingAverage_H1",
              "CciMovingAverage_H4",

              "CommodityChannelIndex_M15",
              "CommodityChannelIndex_H1",
              "CommodityChannelIndex_H4",

              "DonchianATR_M15",
              "DonchianATR_H1",
              "DonchianATR_H4",

              "DonchianBreakout_M15",
              "DonchianBreakout_H1",
              "DonchianBreakout_H4",

              "DonchianMiddle_M15",
              "DonchianMiddle_H1",
              "DonchianMiddle_H4",

              "DpoCandlestick_M15",
              "DpoCandlestick_H1",
              "DpoCandlestick_H4",

              "ElderRay_M15",
              "ElderRay_H1",
              "ElderRay_H4",

              "ElderRayAlternative_M15",
              "ElderRayAlternative_H1",
              "ElderRayAlternative_H4",

              "ThreeEma_M15",
              "ThreeEma_H1",
              "ThreeEma_H4",

              "ThreeEmaAlternative_M15",
              "ThreeEmaAlternative_H1",
              "ThreeEmaAlternative_H4",

              "EMACrossover_M15",
              "EMACrossover_H1",
              "EMACrossover_H4",

              "EMACrossoverAlternative_M15",
              "EMACrossoverAlternative_H1",
              "EMACrossoverAlternative_H4",

              "EMACrossoverRSI_M15",
              "EMACrossoverRSI_H1",
              "EMACrossoverRSI_H4",

              "EMACrossoverRSIAlternative_M15",
              "EMACrossoverRSIAlternative_H1",
              "EMACrossoverRSIAlternative_H4",

              "EMAMACDRSI_M15",
              "EMAMACDRSI_H1",
              "EMAMACDRSI_H4",

              "EMAMI_M15",
              "EMAMI_H1",
              "EMAMI_H4",

              "ForceIndexEMA_M15",
              "ForceIndexEMA_H1",
              "ForceIndexEMA_H4",

              "KeltnerStochasticAdx_M15",
              "KeltnerStochasticAdx_H1",
              "KeltnerStochasticAdx_H4",

              "KAMA_M15",
              "KAMA_H1",
              "KAMA_H4",

              "KAMACrossover_M15",
              "KAMACrossover_H1",
              "KAMACrossover_H4",

              "KeltnerAdx_M15",
              "KeltnerAdx_H1",
              "KeltnerAdx_H4",

              "KeltnerRsi_M15",
              "KeltnerRsi_H1",
              "KeltnerRsi_H4",

              "KeltnerStochastic_M15",
              "KeltnerStochastic_H1",
              "KeltnerStochastic_H4",

              "MACDCrossover_M15",
              "MACDCrossover_H1",
              "MACDCrossover_H4",

              "MACDHistogramReversal_M15",
              "MACDHistogramReversal_H1",
              "MACDHistogramReversal_H4",

              "MacdRsiSma_M15",
              "MacdRsiSma_H1",
              "MacdRsiSma_H4",

              "MACDStochasticCrossover_M15",
              "MACDStochasticCrossover_H1",
              "MACDStochasticCrossover_H4",

              "MACDZeroCross_M15",
              "MACDZeroCross_H1",
              "MACDZeroCross_H4",

              "MFI_M15",
              "MFI_H1",
              "MFI_H4",

              "OopsSignals_M15",
              "OopsSignals_H1",
              "OopsSignals_H4",

              "PsarMovingAverage_M15",
              "PsarMovingAverage_H1",
              "PsarMovingAverage_H4",

              "Rsi2_M15",
              "Rsi2_H1",
              "Rsi2_H4",

              "Rsi8020_M15",
              "Rsi8020_H1",
              "Rsi8020_H4",

              "SimpleMAExponentialMA_M15",
              "SimpleMAExponentialMA_H1",
              "SimpleMAExponentialMA_H4",

              "SimpleMAExponentialMAAlternative_M15",
              "SimpleMAExponentialMAAlternative_H1",
              "SimpleMAExponentialMAAlternative_H4",

              "SMAMI_M15",
              "SMAMI_H1",
              "SMAMI_H4",

              "StochasticOscillatorNoExit_M15",
              "StochasticOscillatorNoExit_H1",
              "StochasticOscillatorNoExit_H4",

              "TripleBollingerBands_M15",
              "TripleBollingerBands_H1",
              "TripleBollingerBands_H4",

              "TrixEma_M15",
              "TrixEma_H1",
              "TrixEma_H4",

              "TrixMI_M15",
              "TrixMI_H1",
              "TrixMI_H4",

              "TrixRsi_M15",
              "TrixRsi_H1",
              "TrixRsi_H4",

              "TSICrossover_M15",
              "TSICrossover_H1",
              "TSICrossover_H4",

              "VortexCrossover_M15",
              "VortexCrossover_H1",
              "VortexCrossover_H4",

              "VortexSma_M15",
              "VortexSma_H1",
              "VortexSma_H4",

              "WilliamsIndicator_M15",
              "WilliamsIndicator_H1",
              "WilliamsIndicator_H4",

              "WilliamsRsi_M15",
              "WilliamsRsi_H1",
              "WilliamsRsi_H4",

              "WilliamsStochastic_M15",
              "WilliamsStochastic_H1",
              "WilliamsStochastic_H4",

              "ZigZag_M15",
              "ZigZag_H1",
              "ZigZag_H4",

              "EMACrossoverMACD_M15",
              "EMACrossoverMACD_H1",
              "EMACrossoverMACD_H4"]

# does not work
#app.add_middleware(
#    TrustedHostMiddleware, allowed_hosts=["52.89.214.238","34.212.75.30:47464","54.218.53.128","52.32.178.7:58232"]
#)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

class Base(DeclarativeBase):
    pass

class TimeFrame(enum.Enum):
    PERIOD_M1 = 1
    PERIOD_M15 = 15
    PERIOD_H1 = 60
    PERIOD_H4 = 240
    PERIOD_D1 = 6*240
    PERIOD_W1 = 30*6*240

class Regressions(Base):
    __tablename__ = "regressions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(6))
    timeFrame: Mapped[Enum] = mapped_column(Enum(TimeFrame))
    startTime: Mapped[str] = mapped_column(String(30))
    endTime: Mapped[str] = mapped_column(String(30))
    startValue: Mapped[float]
    endValue: Mapped[float]

    def __repr__(self) -> str:
        return (f"Regression(id={self.id!r}, symbol={self.symbol!r}, timeFrame={self.timeFrame!r}, startTime={self.startTime!r}, endTime={self.endTime!r})"
                f", startValue={self.startValue!r}, endValue={self.endValue!r})")

class IgnoredSignal(Base):
    __tablename__ = "IgnoredSignals"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    json: Mapped[str] = mapped_column(String(64000))
    reason: Mapped[str] = mapped_column(String(64000))

class Signal(Base):
    __tablename__ = "Trades"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(6))
    type: Mapped[str] = mapped_column(String(6))
    entry: Mapped[float]
    sl: Mapped[float]
    tp: Mapped[float]
    lots: Mapped[float]
    spread: Mapped[float] = mapped_column(nullable=True, default=0.0)
    stamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    # werden erst nach der Erstellung des Trades gesetzt
    activated: Mapped[str] = mapped_column(nullable=True, default="")
    openprice: Mapped[float] = mapped_column(nullable=True, default=0.0)
    swap: Mapped[float] = mapped_column(nullable=True, default=0.0)
    profit: Mapped[float] = mapped_column(nullable=True, default=0.0)
    closed: Mapped[str] = mapped_column(nullable=True, default="")
    commision: Mapped[float] = mapped_column(nullable=True, default="")
    strategy: Mapped[str] = mapped_column(nullable=True, default="")
    # here a string because of tradingview
    timeframe: Mapped[str]

class ProdSignal(Base):
    __tablename__ = "ProdTrades"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(6))
    type: Mapped[str] = mapped_column(String(6))
    entry: Mapped[float]
    sl: Mapped[float]
    tp: Mapped[float]
    lots: Mapped[float]
    spread: Mapped[float] = mapped_column(nullable=True, default=0.0)
    stamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    # werden erst nach der Erstellung des Trades gesetzt
    activated: Mapped[str] = mapped_column(nullable=True, default="")
    openprice: Mapped[float] = mapped_column(nullable=True, default=0.0)
    swap: Mapped[float] = mapped_column(nullable=True, default=0.0)
    profit: Mapped[float] = mapped_column(nullable=True, default=0.0)
    closed: Mapped[str] = mapped_column(nullable=True, default="")
    commision: Mapped[float] = mapped_column(nullable=True, default="")
    strategy: Mapped[str] = mapped_column(nullable=True, default="")
    # here a string because of tradingview
    timeframe: Mapped[str]

class CandlesEntity(Base):
    __tablename__ = "Candles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    SYMBOL: Mapped[str] = mapped_column(String(6))
    TIMEFRAME: Mapped[Enum] = mapped_column(Enum(TimeFrame))
    DATETIME: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    ##TIMESTAMP:Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    OPEN: Mapped[float]
    HIGH: Mapped[float]
    LOW: Mapped[float]
    CLOSE: Mapped[float]
    TICKVOL: Mapped[float]
    VOL: Mapped[float]
    SPREAD: Mapped[float]
    UniqueConstraint("SYMBOL", "TIMEFRAME", "DATETIME", "OPEN", "CLOSE", name="uix_1")
    #STAMP: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

    def __repr__(self) -> str:
        return (f"Candles(id={self.id!r}, DATETIME={self.DATETIME!r}"
                f", OPEN={self.OPEN!r}, CLOSE={self.CLOSE!r})")

class TrendInfoEntity(Base):
    __tablename__ = "TrendInfo"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(6))
    stamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    trendscore:Mapped[int]
    uptrend:Mapped[bool]
    r1: Mapped[float]
    s1: Mapped[float]


class SignalDto(BaseModel):
    symbol:str
    timestamp:str
    type:str
    entry:float
    sl:float
    tp:float
    strategy: str
    timeframe: Optional[str] = None

class TrendInfoDto(BaseModel):
    symbol:str
    timestamp:str
    trendScore:int
    uptrend:bool
    r1: float
    s1: float
    strategy: str

def wwma(values, n):
    """
     J. Welles Wilder's EMA
    """
    return values.ewm(alpha=1/n, adjust=False).mean()

def atr(df, n=14):
    data = df.copy()
    high = data['HIGH']
    low = data['LOW']
    close = data['CLOSE']
    data['tr0'] = abs(high - low)
    data['tr1'] = abs(high - close.shift())
    data['tr2'] = abs(low - close.shift())
    tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = wwma(tr, n)
    return atr

def loadDfFromDb(symbol:str, timeFrame:TimeFrame, session, limit=250000):

    df = pd.read_sql_query(
        sql = session.query(CandlesEntity.SYMBOL,
                            CandlesEntity.TIMEFRAME,
                            CandlesEntity.DATETIME,
                            CandlesEntity.OPEN,
                            CandlesEntity.HIGH,
                            CandlesEntity.LOW,
                            CandlesEntity.CLOSE,
                            CandlesEntity.TICKVOL,
                            CandlesEntity.VOL,
                            CandlesEntity.SPREAD)
        .filter(CandlesEntity.SYMBOL == symbol, CandlesEntity.TIMEFRAME == timeFrame)
        .order_by(CandlesEntity.id.desc())
        .limit(limit)
        .statement,
        con = engine
    )
    #print(len(df), " database entries loaded for ",timeFrame)
    #print("Last row: ")
    #print(df.iloc[-1])
    df_no_duplicates = df.drop_duplicates(subset=['DATETIME'])
    return df_no_duplicates.drop_duplicates()

def lastCandle(symbol:str, timeFrame:TimeFrame):
    with Session.begin() as session:
        candle = session.query(CandlesEntity).filter(CandlesEntity.SYMBOL == symbol, CandlesEntity.TIMEFRAME == timeFrame).order_by(CandlesEntity.DATETIME.desc()).first()
        session.expunge(candle)
        session.close()
        return candle

@app.post("/trendinfo")
async def signals(trendInfo:TrendInfoDto):
    #print("########################################trendinfo########################################")
    #print(str(trendInfo))
    #print("########################################trendinfo########################################")
    #proceedSignal(signal)
    with Session.begin() as session:
        storedInfo = session.query(TrendInfoEntity).filter(TrendInfoEntity.symbol == trendInfo.symbol).first()
        if storedInfo is not None:
            session.delete(storedInfo)
        info = TrendInfoEntity(
            symbol=trendInfo.symbol,
            trendscore=trendInfo.trendScore,
            uptrend=trendInfo.uptrend,
            r1=trendInfo.r1,
            s1=trendInfo.s1
        )
        session.add(info)
        session.commit()
        session.close()

@app.post("/signal")
async def signals(signal:SignalDto):
    #print(str(signal))
    # only for testing connection ######################
    #data = {"symbol": signal.symbol,
    #        "timestamp": "",
    #        "type": signal.type,
    #        "entry": signal.entry,
    #        "sl": signal.sl,
    #        "tp": signal.tp,
    #        "strategy": signal.strategy}
    #response = requests.post(
    #    "http://javabackend:5080/forex/signal",
    #    json=data,
    #)
    #if response.status_code != 200:
    #    print(str(response.status_code))
    ######################################################
    proceedSignal(signal)
    return "Finished!"

def calculateSlAndStoreSignal(signal, strategy, session):
    df = loadDfFromDb(signal.symbol, TimeFrame.PERIOD_D1, session, 200)
    atrValue = atr(df)

    sl = 0.0
    tp = 0.0
    if signal.type == "sell":
        sl = signal.entry + atrValue.iloc[-1]
        tp = signal.entry - atrValue.iloc[-1]
    if signal.type == "buy":
        sl = signal.entry - atrValue.iloc[-1]
        tp = signal.entry + atrValue.iloc[-1]

    # Immer an Java Backend senden
    data = {"symbol": signal.symbol,
            "timestamp": signal.timestamp,
            "type": signal.type,
            "entry": signal.entry,
            "sl": sl,
            "tp": tp,
            "lots": 0.1,
            "strategy": strategy,
            "timeframe": signal.timeframe}
    #logger.info("Sending signal to backend ...")
    response = requests.post(
        "http://javabackend:5080/forex/signals",
        json=data,
    )
    if response.status_code != 200:
        #logger.error("#############################Error sending to Java Backend##############################")
        #logger.error(str(response.status_code))
        #print(str(response))
        logger.error("Error sending to Java Backend" + str(response))
    #else:
    #    #print(f"Signal sent to Java Backend")
    #    logger.info(f"{signal} send to Java Backend")

def proceedSignal(signal:SignalDto):
    # no need to check for trend in TradingView we send everything
    # and do the check here
    # D-EMA200, H4-EMA, D-Regression, H4-Regression
    # Support Resistance
    #print(f"Received: {signal}")
    #ignored XRPUSD

    if signal.timeframe is None or signal.timeframe == "TimeFrame.PERIOD_M15":
        signal.timeframe = "15"
    if signal.timeframe == "TimeFrame.PERIOD_H1":
        signal.timeframe = "60"
    if signal.timeframe == "TimeFrame.PERIOD_H4":
        signal.timeframe = "240"

    if signal.symbol == "XRPUSD":
        return
    #generates too much signals
    if "T3-MesaPhasor" == signal.strategy \
            or "T3-ScaledNormalizedVector" == signal.strategy \
            or "T3-VolumeDifferenceDeltaCycleOscillator" == signal.strategy:
        return

    strategy = signal.strategy.replace("GaussianChannelTrendAi", "GaussianChannelTrendAI")
    strategy = strategy.replace("T3-machineLearningLogisticRegression","T3-MachineLearningLogisticRegression")
    jsonSignal =str({'symbol': signal.symbol,
                     'timestamp': signal.timestamp,
                     'type': signal.type,
                     'entry': signal.entry,
                     'sl': signal.sl,
                     'tp': signal.tp,
                     'strategy': strategy,
                     'timeframe': signal.timeframe})

    logger.info(f"Received {jsonSignal} ..")

    with (Session.begin() as session):

        if signal.symbol not in symbols:
            #print(f"Ignore Signal because symbol is not handled yet: {signal}")
            storeIgnoredSignal(IgnoredSignal(
                json=jsonSignal,
                reason=f"Ignore Signal because symbol is not handled yet: {signal}"
            ),session)
            session.commit()
            session.close()
            return

        if strategy not in strategies:
            logger.info(f"Ignore Signal because strategy is unknown: {strategy}")
            storeIgnoredSignal(IgnoredSignal(
                json=jsonSignal,
                reason=f"Ignore Signal because strategy is unknown: {strategy}"
            ),session)
            session.commit()
            session.close()
            return

        trendInfo = session.query(TrendInfoEntity).filter(TrendInfoEntity.symbol == signal.symbol).first()
        if trendInfo is not None:
            if trendInfo.trendscore > -7 and signal.type == "sell":
                logger.info(f"Ignore Signal because signal {signal} is against trendscore: {trendInfo.trendscore} \n")
                #if trendInfo.trendscore == -6:
                #    storeIgnoredSignal(IgnoredSignal(
                #        json=jsonSignal,
                #        reason=f"Ignore Signal because signal {signal} is against trendscore: {trendInfo.trendscore}"
                #    ),session)
                session.close()
                return
            if trendInfo.trendscore < 7 and signal.type == "buy":
                logger.info(f"Ignore Signal because signal {signal} is against trendscore: {trendInfo.trendscore} \n")
                #if trendInfo.trendscore == 6:
                #    storeIgnoredSignal(IgnoredSignal(
                #        json=jsonSignal,
                #        reason=f"Ignore Signal because signal {signal} is against trendscore: {trendInfo.trendscore}"
                #    ),session)
                session.close()
                return
        if trendInfo is None:
            logger.warning(f"Ignore Signal {signal} because TrendInfo not found!")
            storeIgnoredSignal(IgnoredSignal(
                json=jsonSignal,
                reason=f"Ignore Signal {signal} because TrendInfo not found!"
            ),session)
            session.commit()
            session.close()
            return

        #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        #logger.info("++++++++++++++++++++++++FIRST CHECKS PASSED++++++++++++++++++++++++")
        #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        if strategy == "T3-GridLike" \
                or strategy == "T3-NickRypockTrailingReverse" \
                or strategy == "T3-BilateralStochasticOscillator" \
                or strategy == "T3-CustomSuperTrendCleaned" \
                or strategy == "T3-LlorensActivator" \
                or strategy == "T3-UhlMASystem" \
                or strategy == "T3-NeutronixDCAemu" \
                or strategy == "T3-MacdHistogram-LLTDEMA" \
                or strategy == "T3-MacdHistogram-TDEMA" \
                or strategy == "T3-MacdHistogram-DEMA" \
                or strategy == "T3-MacdHistogram-EMA" \
                or strategy == "T3-MacdHistogram-THMA" \
                or strategy == "T3-MacdHistogram-ZLEMA" \
                or strategy == "T3-MacdHistogram-ZLTEMA" \
                or strategy == "T3-NeutronixSwing" \
                or strategy == "T3-NeutronixAi" \
                or strategy == "T3-NeutronixScalping" \
                or strategy == "T3-ThreeCommasBotStrategy-EMA" \
                or strategy == "T3-ThreeCommasBotStrategy-HEMA" \
                or strategy == "T3-ThreeCommasBotStrategy-SMA" \
                or strategy == "T3-ThreeCommasBotStrategy-HMA" \
                or strategy == "T3-ThreeCommasBotStrategy-WMA" \
                or strategy == "T3-ThreeCommasBotStrategy-DEMA" \
                or strategy == "T3-ThreeCommasBotStrategy-VWMA" \
                or strategy == "T3-ThreeCommasBotStrategy-VWAP" \
                or strategy == "T3-ThreeCommasBotStrategy-T3" \
                or strategy == "T3-MomentumBasedZigZag" \
                or strategy == "T3-DekidakaAshiSignals" \
                or strategy == "T3-SuperTrendCleaned" \
                or strategy == "T3-ScaledNormalizedVector" \
                or strategy == "T3-RangeFilters" \
                or strategy == "T3-ReversalFinder" \
                or strategy == "T3-PinBarStrategy" \
                or strategy == "T3-ThirdWave" \
                or strategy == "T3-Lube" \
                or strategy == "T3-AntiBreakout" \
                or strategy == "T3-PivotPointSuperTrend" \
                or strategy == "T3-LinearTrend" \
                or strategy == "T3-UtBot" \
                or strategy == "T3-HalfTrend" \
                or strategy == "T3-BernoulliEntropyFunction" \
                or strategy == "T3-DiCrossingDaily" \
                or strategy == "T3-MacdScalp" \
                or strategy == "T3-VolumeDifferenceDeltaCycleOscillator" \
                or strategy == "NNR" \
                or strategy == "T3-LocallyWeightedRegression" \
                or strategy == "T3-HmaKahlman" or strategy == "T3-EvwmaVwapMacd" \
                or strategy == "T3-EfficientTrendStepMod" \
                or strategy == "SOTT-Lorentzian" \
                or strategy == "T3-Eams" \
                or strategy == "T3-SupportAndResistanceLevels" \
                or strategy == "T3-MesaPhasor" \
                or strategy == "T3-BollingerBandsPinbar" \
                or strategy == "T3-NNFX" \
                or strategy == "VHMA" \
                or strategy == "RSS_WMA" \
                or strategy == "Super AI Trend" \
                or strategy == "SSL Hybrid" \
                or strategy == "SentimentRangeMa" \
                or strategy == "T3-EmaStrategy" \
                or strategy == "T3-AroonBased" \
                or strategy == "T3Fvma" \
                or strategy == "T3-JMaCrossover" \
                or strategy == "T3-GapFilling" \
                or strategy == "SuperTrend AI" \
                or strategy == "STD-Filtered-Close" \
                or strategy == "AI Volume Supertrend-WMA" \
                or strategy == "RedK-SMA-SMA" \
                or strategy == "MTI" \
                or strategy == "Turtle Soup" \
                or strategy == "Multiple Logistic Regression":
            # Ohne Beachtung der Regression Line speichern
            calculateSlAndStoreSignal(signal, strategy + "_WITHOUT_REG", session)


        regressionLineH4 = session.query(Regressions).filter(
            Regressions.symbol == signal.symbol, Regressions.timeFrame == TimeFrame.PERIOD_H4).all()

        if len(regressionLineH4) > 0:

            if "buy" == signal.type and signal.entry < regressionLineH4[0].endValue:
                logger.warning(f"Ignore (2. Condition) Buy-Signal: {signal}, Regression-End: {regressionLineH4[0].endValue}")
                #storeIgnoredSignal(IgnoredSignal(
                #    json=jsonSignal,
                #    reason=f"Ignore (2. Condition) Buy-Signal: {signal.entry}, Regression-End: {regressionLineH4[0].endValue}"
                #))
                # session weiterhin beenden, da Stats aus DB geladen werden
                #session.commit()
                session.close()
                return

            if "sell" == signal.type and signal.entry > regressionLineH4[0].endValue:
                logger.warning(f"Ignore (2. Condition) Sell-Signal: {signal}, Regression-End: {regressionLineH4[0].endValue}")
                #storeIgnoredSignal(IgnoredSignal(
                #    json=jsonSignal,
                #    reason=f"Ignore (2. Condition) Sell-Signal: {signal.entry}, Regression-End: {regressionLineH4[0].endValue}"
                #))
                # session weiterhin beenden, da Stats aus DB geladen werden
                #session.commit()
                session.close()
                return
            # Mit Beachtung der Regression Line speichern
            calculateSlAndStoreSignal(signal, strategy, session)
            # session weiterhin beenden, da Stats aus DB geladen werden
            session.commit()
            session.close()
            #print(f"######## {signal} stored ########")
        else:
            #storeIgnoredSignal(IgnoredSignal(
            #    json=jsonSignal,
            #    reason=f"Ignored because Regression Line for H4 was not found!"
            #), session)
            #session.commit()
            logger.warning(f"Ignored because Regression Line for H4 was not found!")
            session.close()
        #    regressionLineD1 = session.query(Regressions).filter(
        #        Regressions.symbol == signal.symbol, Regressions.timeFrame == TimeFrame.PERIOD_D1).all()
        #    if len(regressionLineD1) > 0:
        #        if "buy" == signal.type and signal.entry < regressionLineD1[0].endValue:
        #            print(f"Ignore (2. Condition) Buy-Signal: {signal}, Regression-End: {regressionLineD1[0].endValue}")
        #            #storeIgnoredSignal(IgnoredSignal(
        #            #    json=jsonSignal,
        #            #    reason=f"Ignore (2. Condition) Buy-Signal: {signal.entry}, Regression-End: {regressionLineD1[0].endValue}"
        #            #))
        #            session.commit()
        #            session.close()
        #            return

        #        if "sell" == signal.type and signal.entry > regressionLineD1[0].endValue:
        #            print(f"Ignore (2. Condition) Sell-Signal: {signal}, Regression-End: {regressionLineD1[0].endValue}")
        #            #storeIgnoredSignal(IgnoredSignal(
        #            #    json=jsonSignal,
        #            #    reason=f"Ignore (2. Condition) Sell-Signal: {signal.entry}, Regression-End: {regressionLineD1[0].endValue}"
        #            #))
        #            session.commit()
        #            session.close()
        #            return

        #        df = loadDfFromDb(signal.symbol, TimeFrame.PERIOD_D1, session)
        #        atrValue = atr(df)

        #        sl = 0.0
        #        tp = 0.0
        #        if signal.type == "sell":
        #            sl = signal.entry + atrValue.iloc[-1]
        #            tp = signal.entry - atrValue.iloc[-1]
        #        if signal.type == "buy":
        #            sl = signal.entry - atrValue.iloc[-1]
        #            tp = signal.entry + atrValue.iloc[-1]

                #storeSignal(Signal(
                #    symbol=signal.symbol,
                #    type=signal.type,
                #    entry=signal.entry,
                #    sl=sl,
                #    tp=tp,
                #    lots=0.1,
                #    commision=0.0,
                #    strategy=strategy
                #), session)
                #session.commit()
                #session.close()
        #        print(f"######## {signal} stored ########")
        #    else:
                #session.commit()
                #session.close()
        #        print(f"No Regression-Data found for {signal.symbol}")

def storeProdSignal(signal: ProdSignal, session):
    session.add(signal)

def storeSignal(signal: Signal, session):
    session.add(signal)

def storeIgnoredSignal(signal: IgnoredSignal, session):
    session.add(signal)

if __name__ == "__main__":



    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ecs_logging.StdlibFormatter())
    logger.addHandler(console_handler)

    # needs to be a different log files than default-server
    handler = logging.FileHandler('logs.json')
    handler.setFormatter(ecs_logging.StdlibFormatter())
    logger.addHandler(handler)
    Base.metadata.create_all(engine)
    #port can only be 80 see tradingview
    # almost no logs
    #uvicorn.run(app, host="0.0.0.0", port=80, log_level="critical", access_log=False)
    uvicorn.run(app, host="0.0.0.0", port=80, log_level="info", access_log=True)