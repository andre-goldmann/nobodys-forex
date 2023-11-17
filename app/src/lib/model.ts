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

export interface Trade {
    id:number,
    symbol:string,
    type:string,
    entry:number,
    sl:number,
    tp:number,
    lots:number,
    stamp:string
}

export interface IgnoredSignal {
    id: number,
    json: string,
    reason: string
}

export interface Strategy {
    strategy:string,
    profit:number,
    swap:number,
    trades:number,
    commission:number
}