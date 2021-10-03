import sqlite3
import config

init_query = """CREATE TABLE thm_grading_queue(
                username CHARACTER(20) NOT NULL,
                challenge_name CHARACTER(50) NOT NULL,
                CONSTRAINT thm_PK PRIMARY KEY (username, challenge_name));"""

conn = sqlite3.connect(config.DB_FILE_NAME)
conn.execute(init_query)

conn.close()
