import psycopg2
from psycopg2 import sql
import datetime
from contextlib import contextmanager


class FileVersionTracker:
    def __init__(self, config):
        self.config = config
        # Handle both dict and module config
        if hasattr(config, "DB_TABLE_NAME"):
            self.table_name = config.DB_TABLE_NAME
        else:
            self.table_name = config.get("DB_TABLE_NAME", "file_tracker")

    @contextmanager
    def get_connection(self):
        # Handle both dict and module config
        if hasattr(self.config, "DB_HOST"):
            # config is a module
            db_host = self.config.DB_HOST
            db_user = self.config.DB_USER
            db_pass = self.config.DB_PASS
            db_name = self.config.DB_NAME
        else:
            # config is a dict
            db_host = self.config.get("DB_HOST")
            db_user = self.config.get("DB_USER")
            db_pass = self.config.get("DB_PASS")
            db_name = self.config.get("DB_NAME")

        conn = psycopg2.connect(
            host=db_host, user=db_user, password=db_pass, database=db_name
        )
        try:
            yield conn
        finally:
            conn.close()

    def get_last_version(self, filename: str) -> datetime.datetime | None:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                query = sql.SQL("SELECT tracker FROM {} WHERE filename = %s").format(
                    sql.Identifier(self.table_name)
                )
                cursor.execute(query, (filename,))
                result = cursor.fetchone()
                return (
                    datetime.datetime.fromisoformat(result[0].replace("Z", "+00:00"))
                    if result
                    else None
                )

    def set_last_version(self, filename: str, version: str) -> None:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                query = sql.SQL(
                    "UPDATE {} SET tracker = NOW() WHERE filename = %s"
                ).format(sql.Identifier(self.table_name))
                cursor.execute(query, (filename,))
                conn.commit()

    def is_new_version_available(
        self, filename: str, new_version_timestamp_str: str
    ) -> bool:
        try:
            new_version_timestamp = datetime.datetime.fromisoformat(
                new_version_timestamp_str.replace("Z", "+00:00")
            )
            last_version = self.get_last_version(filename)

            if last_version is None:
                return True

            return new_version_timestamp > last_version
        except Exception as e:
            raise RuntimeError(f"The given timestamp string is not valid: {e}")
