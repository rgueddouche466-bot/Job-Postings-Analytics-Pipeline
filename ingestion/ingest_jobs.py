from api_client import JobAPIClient
from utils import normalize_jobs
from snowflake_loader import SnowflakeLoader

def run_pipeline():
    client = JobAPIClient()
    loader = SnowflakeLoader()

    # Extract
    data = client.fetch_all_jobs()

    # Transform
    df = normalize_jobs(data)
    print(f"📊 {len(df)} unique jobs after deduplication")

    # Load
    loader.load_jobs(df)

    print("✅ Pipeline completed")


if __name__ == "__main__":
    run_pipeline()