import json
# from VWAPScalpingStrategy import runFirstStrategy
from typing import List

import uvicorn
from fastapi import FastAPI, WebSocket
# Bellow the import create a job that will be executed on background
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from CandleStorageHandler import CandlesDto

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])

class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        await manager.broadcast(f"Client {client_id}: {data}")

@app.get("/store")
async def storeCandleTes():
    candle = CandlesDto(
        symbol="Eur",
        TIMEFRAME="TimeFrame.PERIOD_D1",
        DATE="",
        TIME="time",
        OPEN=1.04979,
        HIGH=1.04979,
        LOW=1.04979,
        CLOSE=1.04979,
        VOL=1.0,
        TICKVOL=1.0,
        SPREAD=1.0
    )

    #print("Store: " , candle)
    #storeCandleInDb(candle)
    json_compatible_item_data = jsonable_encoder(candle)
    print(json_compatible_item_data.keys())
    await manager.broadcast(json.dumps(json_compatible_item_data))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)