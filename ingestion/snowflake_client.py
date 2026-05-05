import snowflake.connector
from config import Config

class SnowflakeClient:
    def __init__(self):
        try:
            self.conn = snowflake.connector.connect(
                user=Config.SNOWFLAKE_CONFIG["user"],
                password=Config.SNOWFLAKE_CONFIG["password"],
                account=Config.SNOWFLAKE_CONFIG["account"],
                warehouse=Config.SNOWFLAKE_CONFIG["warehouse"],
                database=Config.SNOWFLAKE_CONFIG["database"],
                schema=Config.SNOWFLAKE_CONFIG["schema"],
            )
            print("✅ Snowflake connection established")

            # ✅ CRITICAL FIX: Set session context explicitly
            self._set_context()

        except Exception as e:
            print("❌ Failed to connect to Snowflake")
            raise e

    def _set_context(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute(f"USE WAREHOUSE {Config.SNOWFLAKE_CONFIG['warehouse']}")
            cursor.execute(f"USE DATABASE {Config.SNOWFLAKE_CONFIG['database']}")
            cursor.execute(f"USE SCHEMA {Config.SNOWFLAKE_CONFIG['schema']}")
        finally:
            cursor.close()

    def get_connection(self):
        return self.conn

    def test_connection(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE()")
            print("Context:", cursor.fetchone())
        finally:
            cursor.close()

    def close(self):
        if self.conn:
            self.conn.close()
            print("🔌 Snowflake connection closed")
