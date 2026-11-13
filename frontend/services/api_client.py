"""
API Client for communication between Streamlit Frontend and FastAPI Backend.
"""
from typing import Dict, Any, List, Optional
import requests
from frontend.config import API_BASE_URL


class APIClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip("/")

    def get_portfolio_overview(self) -> Optional[Dict[str, Any]]:
        try:
            res = requests.get(f"{self.base_url}/analysis/portfolio/overview", timeout=15)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(f"Error fetching portfolio overview: {e}")
            return None

    def get_customers(self, limit: int = 50, segment: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {"limit": limit}
        if segment:
            params["segment"] = segment
        try:
            res = requests.get(f"{self.base_url}/customers", params=params, timeout=10)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(f"Error fetching customers: {e}")
            return []

    def get_customer_profile(self, customer_id: str) -> Optional[Dict[str, Any]]:
        try:
            res = requests.get(f"{self.base_url}/customers/{customer_id}", timeout=10)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(f"Error fetching profile: {e}")
            return None

    def get_spending_analysis(self, customer_id: str) -> Optional[Dict[str, Any]]:
        try:
            res = requests.get(f"{self.base_url}/analysis/spending/{customer_id}", timeout=10)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(f"Error fetching spending analysis: {e}")
            return None

    def get_insights(self, customer_id: str) -> Optional[Dict[str, Any]]:
        try:
            res = requests.get(f"{self.base_url}/analysis/insights/{customer_id}", timeout=10)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(f"Error fetching insights: {e}")
            return None

    def get_recommendations(self, customer_id: str) -> Optional[Dict[str, Any]]:
        try:
            res = requests.get(f"{self.base_url}/recommendations/{customer_id}", timeout=10)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(f"Error fetching recommendations: {e}")
            return None

    def get_transactions(self, customer_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            res = requests.get(f"{self.base_url}/transactions/{customer_id}", params={"limit": limit}, timeout=10)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []

    def chat_copilot(
        self,
        customer_id: str,
        message: str,
        history: List[Dict[str, str]],
        gemini_api_key: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        payload = {
            "customer_id": customer_id,
            "message": message,
            "conversation_history": history,
            "gemini_api_key": gemini_api_key
        }
        try:
            res = requests.post(f"{self.base_url}/copilot/chat", json=payload, timeout=60)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(f"Error chatting with copilot: {e}")
            return None


api_client = APIClient()

