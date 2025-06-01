import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS jobs (
        uid VARCHAR PRIMARY KEY NOT NULL,
        scheduled_dt VARCHAR,
        teacher VARCHAR,
        position VARCHAR,
        location VARCHAR,
        timestamp DATETIME)""")
        self.conn.commit()

    def insert_job(self, job):
        self.cursor.execute(
        """
        INSERT INTO jobs (
            uid,
            scheduled_dt,
            teacher,
            position,
            location,
            timestamp
        )
        VALUES (
            :uid,
            :scheduled_dt,
            :teacher,
            :position,
            :location,
            :timestamp
        )
        """,job)
        self.conn.commit()

    def delete_old_jobs(self):
        self.cursor.execute("""
        DELETE FROM jobs
        WHERE timestamp < DATE('now', 'weekday 0', '-7 days');
        """)
        self.conn.commit()

    def uid_exists(self, uid):
        self.cursor.execute(f"SELECT * FROM jobs WHERE uid = '{uid}'")
        if self.cursor.fetchone(): return True
        return False

    def close_connection(self):
        self.conn.close()