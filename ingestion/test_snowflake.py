from snowflake_client import SnowflakeClient

def test_connection():
    client = SnowflakeClient()
    client.test_connection()
    client.close()

if __name__ == "__main__":
    test_connection()