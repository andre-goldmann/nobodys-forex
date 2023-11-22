from fastapi.testclient import TestClient

from server import app

client = TestClient(app)

def resendsignal():
    data ={'symbol': "EURUSD",
           'timestamp': "signal.timestamp",
           'type': "sell",
           'entry': 1.0,
           'sl': 1.0,
           'tp': 1.0,
           'strategy': "str"}
    response = client.get("/atr/?symbol=EURUSD&timeframe=PERIOD_W1")
    #response = client.post(
    #    "/test",
    #    headers={"X-Token": "coneofsilence"},
    #    json=data,
    #)
    print(response.json())
    assert response.status_code == 200
def test_read_main():
    response = client.get("/?strategy=Super AI Trend")
    print(response.json())

#resendsignal()
test_read_main()