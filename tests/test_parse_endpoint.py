from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_parse_endpoint():
    payload = {"text": "Title: Hi\nAuthor: Bob\nSummary: Works"}
    r = client.post("/parse", json=payload)
    assert r.status_code == 200
    assert r.json() == {"parsed": {"Title": "Hi", "Author": "Bob", "Summary": "Works"}}
