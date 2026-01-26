import psycopg2
import datetime
from contextlib import contextmanager


class FileVersionTracker:

    def __init__(self, config:dict):
        self.config = config


    @contextmanager
    def get_connection(self):
        conn = psycopg2.connect(
            host=self.config.DB_HOST,
            user=self.config.DB_USER,
            password=self.config.DB_PASS,
            database=self.config.DB_NAME
        )
        try:
            yield conn
        finally:
            conn.close()



    def get_last_version(self, filename: str) -> datetime.datetime | None:
        
        with self.get_connection() as conn:
            with conn.cursor as cursor:
                cursor.execute(f"SELECT tracker FROM {self.table} WHERE filename = %s", (filename,))
                result = cursor.fetchone()
                return datetime.datetime.fromisoformat(result[0].replace('Z', '+00:00')) if result else None


    def set_last_version(self, filename: str, version: str) -> None:
        with self.get_connection() as conn:
            with self.conn.cursor() as cursor:
                cursor.execute(f"UPDATE {self.table_name} SET tracker = NOW() WHERE filename = %s", (filename,))
                self.conn.commit()
        

    def is_new_version_available(self, filename: str, new_version_timestamp_str: str) -> bool:
        
        try:
            new_version_timestamp = datetime.datetime.fromisoformat(new_version_timestamp_str.replace('Z', '+00:00'))
            last_version = self.get_last_version(filename)

            if last_version is None:
                return True
            
            return new_version_timestamp > last_version
        except Exception as e:
            raise RuntimeError(f"The given timestamp string is not valid: {e}")
    