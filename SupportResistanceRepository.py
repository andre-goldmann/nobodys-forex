import enum
import sys
import traceback

from sqlalchemy import Enum
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from DataBaseManagement import Base, Session, TimeFrame

class SupportResistanceType(enum.Enum):
    SUPPORT = 0
    RESISTANCE = 1

class SupportResistance(Base):
    __tablename__ = "SupportResistance"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(6))
    timeframe: Mapped[Enum] = mapped_column(Enum(TimeFrame))
    type: Mapped[Enum] = mapped_column(Enum(SupportResistanceType))
    level: Mapped[float]
    caclulator: Mapped[str]

def deleteSupportResistance(symbol:str, timeFrame:TimeFrame):
    with Session.begin() as session:
        try:
            results = session.query(SupportResistance).filter(
                SupportResistance.symbol==symbol,
                SupportResistance.timeframe==timeFrame).all()
            for r in results:
                session.delete(r)
            session.commit()
        except Exception:
            print("Exception while deleting SupportResistance:")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
            session.rollback()

def storeSupportResistance(sr:SupportResistance):
    # nur jeden Tage einmal löschen
    #deleteSupportResistance(sr.symbol)

    with Session.begin() as session:
        session.add(sr)
        session.commit()

def loadSrs(symbol:str):
    with Session.begin() as session:
            return session.query(SupportResistance).filter(SupportResistance.symbol==symbol).all()