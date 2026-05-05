import requests
import json
from pathlib import Path
from config import Config

class JobAPIClient:

    def fetch_jobs_api_old(self,page=1,results_per_page=50):
        """
        Fetch jobs from real API (Adzuna)
        """
        url= f"{Config.BASE_URL}/{page}"
        params = {
            "app_id": Config.ADZUNA_APP_ID,
            "api_key": Config.ADZUNA_API_KEY,
            "results_per_page": results_per_page,
             "what" :  "software engineer",
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code}")

        return response.json()

    def fetch_jobs_api(self, page=1, results_per_page=50):
        print("CONFIG VALUES:", Config.ADZUNA_APP_ID, Config.ADZUNA_API_KEY)
        if not Config.ADZUNA_APP_ID or not Config.ADZUNA_API_KEY:
            raise ValueError("Missing Adzuna credentials")

        url = f"{Config.BASE_URL}/{page}"

        params = {
            "app_id": Config.ADZUNA_APP_ID,
            "app_key": Config.ADZUNA_API_KEY,
            "results_per_page": results_per_page,
            "what": "software engineer",
            "where": "Chicago",
        }

        print("PARAMS SENT:", params)
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print("URL:", response.url)
            print("Response:", response.text)
            raise Exception(f"API Error: {response.status_code}")

        return response.json()

    def fetch_jobs_mock(self, page=1):
        """
        Fetch jobs from local mock JSON file
        """

        file_path = Path(__file__).parent / "mock_data.json"

        with open(file_path, "r") as f:
            data = json.load(f)

        print(f"[MOCK] Returning data for page {page}")

        return data

    def fetch_jobs(self, source="mock", page=1):
        if source == "api":
            return self.fetch_jobs_api(page)
        else:
            return self.fetch_jobs_mock(page)


