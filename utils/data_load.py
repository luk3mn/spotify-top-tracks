import sqlite3
import sqlalchemy
import pandas as pd

class DataLoad:
    """To load all structured data in a SQL database"""
    def __init__(self, df: pd.DataFrame, tb_name: str = 'my_played_tracks') -> None:
        """
        :param df (object): to work with a pandas DataFrame in particular
        """
        self.df = df
        self.tb_name = tb_name
        self.DATABASE_LOCATION = 'sqlite:///my_played_tracks.sqlite'

    def sql_store(self) -> None:
        """ this method is be able to create the database structure
            - convert pandas to sql
            - load it to database 
        """
        engine = sqlalchemy.create_engine(self.DATABASE_LOCATION)
        conn = sqlite3.connect('my_played_tracks.sqlite')
        cursor = conn.cursor()

        sql_query = f"""
            CREATE TABLE IF NOT EXISTS {self.tb_name} (
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
            self.df.to_sql(f"{self.tb_name}", engine, index=False, if_exists='append')
        except:
            print("Data already exists in the database")
        
        conn.close()
        print('Close database Successfully')