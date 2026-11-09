"""
API Integration tests for FastAPI endpoints.
"""
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"


def test_list_customers():
    res = client.get("/api/v1/customers?limit=5")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "customer_id" in data[0]


def test_spending_analysis_endpoint():
    # Fetch first customer
    cust_res = client.get("/api/v1/customers?limit=1")
    cid = cust_res.json()[0]["customer_id"]

    res = client.get(f"/api/v1/analysis/spending/{cid}")
    assert res.status_code == 200
    data = res.json()
    assert "total_spend_180d" in data
    assert "categories" in data
    assert "monthly_trends" in data


def test_recommendations_endpoint():
    cust_res = client.get("/api/v1/customers?limit=1")
    cid = cust_res.json()[0]["customer_id"]

    res = client.get(f"/api/v1/recommendations/{cid}")
    assert res.status_code == 200
    data = res.json()
    assert "offers" in data
    assert "total_eligible_offers" in data


def test_copilot_chat_endpoint():
    cust_res = client.get("/api/v1/customers?limit=1")
    cid = cust_res.json()[0]["customer_id"]

    payload = {
        "customer_id": cid,
        "message": "Tóm tắt hành vi chi tiêu của khách hàng này",
        "conversation_history": []
    }
    res = client.post("/api/v1/copilot/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data
    assert len(data["tools_executed"]) > 0

