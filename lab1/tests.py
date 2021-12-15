# tests.py

from fastapi.testclient import TestClient
from main import app  # Assuming lab1 is the name of your module containing FastAPI app
from time import sleep
client = TestClient(app)

def test_divide_endpoint():
    # Given: two numbers a and b
    a = 10
    b = 5
    
    response = client.get(f"/divide-celery?a={a}&b={b}")
    
    assert response.status_code == 200

    assert len(response.json()["task_id"]) == 36

def test_query_task_status():

    a = 10
    b = 5
    
    response = client.get(f"/divide-celery?a={a}&b={b}")
    task_id = response.json()["task_id"]
    sleep(5
          )
    # When: the /query-task-status endpoint is called
    response = client.get(f"/query-task-status?task_id={task_id}")
    
    assert response.status_code == 200
    assert "result" in response.json() or response.json()["status"] == "pendsing"


