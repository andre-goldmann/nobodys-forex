export interface Candle
{   SYMBOL:string,
    TIMEFRAME: string, 
    DATETIME: string,
    OPEN: number, 
    HIGH: number, 
    LOW: number, 
    CLOSE: number, 
    TICKVOL: number, 
    VOL: number, 
    SPREAD: number
}

export interface SrLevel{
    symbol: string,
    timeframe: string,
    level: number,
    id: number,
    type: number,
    caclulator: string,
    distance?: number
}