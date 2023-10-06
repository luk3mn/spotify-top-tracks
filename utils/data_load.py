import sqlite3
import sqlalchemy
import pandas as pd

class DataLoad:
    """ Module to load our structured data in a sqlite database
    """
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.DATABASE_LOCATION = 'sqlite:///my_played_tracks.sqlite'

    def sql_store(self) -> None:
        """ this method is be able to create the database structure
            - convert pandas to sql
            - load it to database 
        """
        engine = sqlalchemy.create_engine(self.DATABASE_LOCATION)
        conn = sqlite3.connect('my_played_tracks.sqlite')
        cursor = conn.cursor()

        sql_query = """
            CREATE TABLE IF NOT EXISTS my_played_tracks (
                song_id VARCHAR(200),
                song VARCHAR(200),
                artist VARCHAR(200),
                album VARCHAR(200),
                release VARCHAR(200),
                popularity VARCHAR(200),
                CONSTRAINT primary_key_constraint PRIMARY KEY (song_id)
            );
        """

        cursor.execute(sql_query)
        print("Opened database successfully")

        try:
            ### convert pandas to sql and make the sql ingestion on database
            self.df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
        except:
            print("Data already exists in the database")
        
        conn.close()
        print('Close database Successfully')