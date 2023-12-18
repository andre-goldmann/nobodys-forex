from fastapi.testclient import TestClient

from server import app

client = TestClient(app)

def test_read_main():
    response = client.get("/linesinfo")
    #print(response.json())
    assert response.status_code == 200
    assert response.json() == {'startTime': '2023.07.19 05:00:00', 'endTime': '2023.09.21 21:00:00', 'startValue': 1.121976061538461, 'endValue': 1.0650417538461534}


def defaultsr():
    response = client.get("/defaultsr/?symbol=EURUSD&diff=0.005&actualLevel=1.0644")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {'supports': [1.05881, 1.05759, 1.05329, 1.04691], 'resistances': [1.07745, 1.07989, 1.08284, 1.08752]}

def adsar():
    response = client.get("/adsar/?file=data/EURUSD_H1_201601040000_202309212100.csv&peaksMax=20&sliceMax=30000")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {}

def deletedata():
    response = client.get("/deletedata")
    print(response.json())
    assert response.status_code == 200

def storecandle():
    data = {"symbol": "EURUSD",
            "TIMEFRAME": "PERIOD_M15",
            "DATETIME": "2023.10.12 11:15:00",
            "OPEN": 1.06207,
            "HIGH": 1.06269,
            "LOW": 1.06204,
            "CLOSE": 1.06259,
            "TICKVOL": 1.0553,
            "VOL": 1.0553,
            "SPREAD": 1}
    #response = client.post("/storecandle/",json.dumps(data))
    response = client.post(
        "/storecandle/",
        headers={"X-Token": "coneofsilence"},
        json=data,
    )
    print(response.json())
    assert response.status_code == 200

def linesInfo():
    response = client.get("/linesinfo/?symbol=EURUSD&timeframe=PERIOD_H4")
    print(response.json())
    assert response.status_code == 200
    #assert response.json() == {'stamp': '2023-10-12T11:15:00+00:00'}

def lastCandle():
    response = client.get("/lastCandle/?symbol=EURUSD&timeFrame=PERIOD_M15")
    print(response.json())
    assert response.status_code == 200
    #assert response.json() == {'stamp': '2023-10-12T11:15:00+00:00'}

def strategystats():
    response = client.get("/strategystats")
    print(response.json())
    assert response.status_code == 200
    #assert response.json() == {'stamp': '2023-10-12T11:15:00+00:00'}

def instrumentstats():
    response = client.get("/instrumentstats/?strategy=Super AI Trend")
    print(response.json())
    assert response.status_code == 200
    #assert response.json() == {'stamp': '2023-10-12T11:15:00+00:00'}

def deleteSignal():
    response = client.post(
        "/deletesignal/",
        headers={"X-Token": "coneofsilence"},
        json={"id": 1},
    )
    print(response.json())
    assert response.status_code == 200

#test_read_main()
#defaultsr()
#deletedata()
#adsar()
#2023-10-12 11:15:00.000000 +00:00
#linesInfo()
storecandle()
#lastCandle()
#trategystats()
#instrumentstats()
#deleteSignal()