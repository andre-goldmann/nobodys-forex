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
    #response = client.post("/storecandle/",json.dumps(data))
    response = client.post(
        "/test",
        headers={"X-Token": "coneofsilence"},
        json=data,
    )
    print(response.json())
    assert response.status_code == 200

resendsignal()