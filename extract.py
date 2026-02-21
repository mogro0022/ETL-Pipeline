import requests


def extract_fred_data(series_id: str, api_key: str) -> list:

    url = "https://api.stlouisfed.org/fred/series/observations"

    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": "2020-01-01",
    }

    try:
        print(f"Fetching data for series: {series_id}...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json().get("observations", [])
        return data

    except requests.exceptions.RequestException as e:
        print(f"Network error occurred while hitting the FRED API: {e}")
        return []
