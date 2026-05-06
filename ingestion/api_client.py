import requests
import json
from pathlib import Path
from config import Config

class JobAPIClient:

    def fetch_jobs_api_old(self,page=1,results_per_page=50, what="data engineer", where=None):
        """
        Fetch jobs from real API (Adzuna)
        """
        if not Config.ADZUNA_APP_ID or not Config.ADZUNA_API_KEY:
            raise ValueError("Missing Adzuna credentials")

        url= f"{Config.BASE_URL}/{page}"
        params = {
            "app_id": Config.ADZUNA_APP_ID,
            "api_key": Config.ADZUNA_API_KEY,
            "results_per_page": results_per_page,
            "what": what,
        }

        if where:
            params["where"] = where
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print("URL:", response.url)
            print("Response:", response.text)
            raise Exception(f"API Error: {response.status_code}")

        return response.json()

    def fetch_jobs_api(self, page=1, results_per_page=50, what="data engineer", where=None):
        print("CONFIG VALUES:", Config.ADZUNA_APP_ID, Config.ADZUNA_API_KEY)
        if not Config.ADZUNA_APP_ID or not Config.ADZUNA_API_KEY:
            raise ValueError("Missing Adzuna credentials")

        url = f"{Config.BASE_URL}/{page}"

        params = {
            "app_id": Config.ADZUNA_APP_ID,
            "app_key": Config.ADZUNA_API_KEY,
            "results_per_page": results_per_page,
            "what": what,
        }
        # only add where if provided — omitting it catches remote roles nationwide
        if where:
            params["where"] = where

        print(f"PARAMS SENT: what='{what}' | where='{where or 'nationwide'}' | page={page}")
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

    def fetch_all_jobs(self):

        #  roles based
        search_terms = [
            "data engineer",
            "java backend engineer",
            "full stack java developer",
            "kafka snowflake engineer",
        ]

        # Chicago for local roles, None for remote/nationwide
        locations = ["Chicago", None]

        all_results = []

        for term in search_terms:
            for location in locations:
                location_label = location if location else "remote/nationwide"
                print(f"\n🔍 Searching: '{term}' | Location: {location_label}")

                for page in range(1, 4):
                    try:
                        data = self.fetch_jobs_api(
                            page=page,
                            results_per_page=50,
                            what=term,
                            where=location
                        )
                        results = data.get("results", [])
                        all_results.extend(results)
                        print(f"  ✅ Page {page}: {len(results)} jobs fetched")

                    except Exception as e:
                        print(f"  ❌ Page {page} failed: {e}")
                        break  # stop paginating this search if one page fails

        print(f"\n📦 Total raw results before dedup: {len(all_results)}")
        return {"results": all_results}
