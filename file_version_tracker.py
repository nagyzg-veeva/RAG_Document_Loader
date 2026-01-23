import psycopg2
import datetime


class FileVersionTracker:

    def __init__(self, config:dict):
        self.connection = psycopg2.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASS,
            database=config.DB_NAME
        )
        self.table_name = config.DB_TABLE_NAME


    def get_last_version(self, filename: str) -> datetime.datetime | None:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT tracker FROM {self.table_name} WHERE filename = %s", (filename,))
                result = cursor.fetchone()
                return datetime.datetime.fromisoformat(result[0].replace('Z', '+00:00')) if result else None
        except psycopg2.Error as e:
            raise RuntimeError(f"Database error in get_last_version: {e}")


    def set_last_version(self, filename: str, version: str) -> None:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"UPDATE {self.table_name} SET tracker = NOW() WHERE filename = %s", (filename,))
                self.connection.commit()
        except psycopg2.Error as e:
            raise RuntimeError(f"Database error in set_last_version: {e}")
        

    def is_new_version_available(self, filename: str, new_version_timestamp_str: str) -> bool:
        
        try:
            new_version_timestamp = datetime.datetime.fromisoformat(new_version_timestamp_str.replace('Z', '+00:00'))
            last_version = self.get_last_version(filename)

            if last_version is None:
                return True
            
            return new_version_timestamp > last_version
        except Exception as e:
            raise RuntimeError(f"The given timestamp string is not valid: {e}")
    