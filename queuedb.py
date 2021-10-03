import sqlite3
import config


class Queuedb:

    def __init__(self, DB_FILE_NAME):
        # connect to the db file
        self.conn = sqlite3.connect(DB_FILE_NAME, check_same_thread=False)
        self.TABLE_NAME = config.TABLE_NAME
        self.USERNAME_COL_NAME = config.USERNAME_COL_NAME
        self.CHALLENGE_COL_NAME = config.CHALLENGE_COL_NAME

    def size(self):
        """returns number of rows in the table"""
        rows = self.conn.execute(f'SELECT COUNT(*) FROM {self.TABLE_NAME};')
        self.conn.commit()
        return rows.fetchall()[0][0]

    def push(self, data_list: list):
        """Insert a row into the table"""
        if len(data_list) == 2:
            try:
                self.conn.execute(
                    f'INSERT INTO {self.TABLE_NAME} ({self.USERNAME_COL_NAME}, {self.CHALLENGE_COL_NAME}) VALUES (?, ?);',
                    data_list)
                self.conn.commit()
            except sqlite3.IntegrityError:
                print('already exists')

    def check_existence(self, data_list: list):
        """Checks if data list exists in the table"""
        # execute query to search for the data list in the db
        if len(data_list) == 2:
            rows = self.conn.execute(
                f'SELECT * FROM {self.TABLE_NAME} WHERE {self.USERNAME_COL_NAME} = ? AND {self.CHALLENGE_COL_NAME} = ?;',
                data_list)
            self.conn.commit()
            # check if number of returned rows is greater than 0
            if len(rows.fetchall()) > 0:
                return True
            return False

    def front(self):
        """returns first row in the table"""
        rows = self.conn.execute(f'SELECT * FROM {self.TABLE_NAME};')
        self.conn.commit()
        # check if number of rows is greater than 0
        if self.size() > 0:
            return rows.fetchall()[0]
        else:
            return None

    def pop(self, data_list: list):
        """delete row from the db"""
        self.conn.execute(f'DELETE FROM {self.TABLE_NAME} WHERE {self.USERNAME_COL_NAME} = ? AND {self.CHALLENGE_COL_NAME} = ?;',
            data_list)
        self.conn.commit()

    def close_db_connection(self):
        """Closes db connection"""
        self.conn.close()
