from snowflake.connector.pandas_tools import write_pandas
from snowflake_client import SnowflakeClient

class SnowflakeLoader:

    def load_jobs(self, df, table_name="JOBS"):

        df = df.drop_duplicates(subset=["JOB_ID"])

        client = SnowflakeClient()
        conn = client.get_connection()
        cursor = conn.cursor()

        temp_table = "JOBS_STAGE"

        try:
            # Create temp staging table
            cursor.execute(f"""
                CREATE OR REPLACE TEMP TABLE {temp_table} LIKE {table_name}
            """)

            #  Load DataFrame into staging
            success, nchunks, nrows, _ = write_pandas(
                conn=conn,
                df=df,
                table_name=temp_table,
                auto_create_table=False
            )

            if not success:
                raise Exception("Failed to load staging table")

            print(f" Loaded {nrows} rows into staging table")

            # MERGE
            merge_sql = f"""
                MERGE INTO {table_name} t
                USING {temp_table} s
                ON t.JOB_ID = s.JOB_ID
                WHEN NOT MATCHED THEN
                    INSERT (
                        JOB_ID, TITLE, COMPANY, LOCATION,
                        SALARY_MIN, SALARY_MAX, CREATED
                    )
                    VALUES (
                        s.JOB_ID, s.TITLE, s.COMPANY, s.LOCATION,
                        s.SALARY_MIN, s.SALARY_MAX, s.CREATED
                    )
            """

            cursor.execute(merge_sql)

            print("MERGE completed (only new records inserted)")

        finally:
            cursor.close()
            client.close()