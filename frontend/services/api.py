import requests

BASE_URL = "http://127.0.0.1:8000"


def generate_research(request: dict):
    response = requests.post(
        f"{BASE_URL}/research",
        json=request,
    )
    response.raise_for_status()
    return response.json()


def generate_campaign(request: dict):
    response = requests.post(
        f"{BASE_URL}/campaign",
        json=request,
    )
    response.raise_for_status()
    return response.json()


def regenerate_campaign(request: dict):
    response = requests.post(
        f"{BASE_URL}/campaign/regenerate",
        json=request,
    )
    response.raise_for_status()
    return response.json()


def save_campaign(request: dict):
    response = requests.post(
        f"{BASE_URL}/campaigns",
        json=request,
    )
    response.raise_for_status()
    return response.json()


def get_campaigns():
    response = requests.get(
        f"{BASE_URL}/campaigns"
    )
    response.raise_for_status()
    return response.json()


def get_campaign(campaign_id: int):
    response = requests.get(
        f"{BASE_URL}/campaigns/{campaign_id}"
    )
    response.raise_for_status()
    return response.json()


def update_campaign(
    campaign_id: int,
    request: dict,
):
    response = requests.put(
        f"{BASE_URL}/campaigns/{campaign_id}",
        json=request,
    )
    response.raise_for_status()
    return response.json()


def delete_campaign(campaign_id: int):
    response = requests.delete(
        f"{BASE_URL}/campaigns/{campaign_id}"
    )
    response.raise_for_status()
    return response.json()