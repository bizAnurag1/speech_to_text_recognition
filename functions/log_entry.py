import pytz
from datetime import datetime
import json
import logging
from psycopg2.pool import SimpleConnectionPool

def insert_log_entry(log_level, message, additional_info=None,filename=None ,timestamp=None, source=None):
    """
    Inserts a log entry into the call_logs table.
    Ensures the connection is returned to the pool in all cases.
    """
    conn = None
    try:
        # Set default timestamp if not provided
        if timestamp is None:
            india_tz = pytz.timezone('Asia/Kolkata')
            timestamp = datetime.now(india_tz).strftime('%Y-%m-%d %H:%M:%S')

        # Ensure additional_info is JSON-serializable
        additional_info_json = json.dumps(additional_info) if additional_info else None
        host = "localhost"
        dbname = "postgres"
        user = "postgres"
        password = "root123"
        table_name = "calldetailscanara"
        log_table_name = "call_logs_speech"

        # PostgreSQL connection pool setup (assume these environment variables are set)
        postgreSQL_pool = SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            user=user,
            password=password,
            host=host,
            database=dbname
        )
        # log_table_name = "call_logs".
        conn = postgreSQL_pool.getconn()
        with conn.cursor() as cursor:
            sql = f"""INSERT INTO {log_table_name} (log_level, message, additional_info, filename, timestamp, source)
                VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (log_level, message, additional_info_json, filename, timestamp, source))
            conn.commit()
        logging.info(f"Log entry inserted: {message}")
    except Exception as e:
        logging.error(f"Failed to insert log entry: {e}")
    finally:
        if conn:
            postgreSQL_pool.putconn(conn)