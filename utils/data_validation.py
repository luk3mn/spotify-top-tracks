import pandas as pd

class DataValidation:
    """To make validation on data collection"""
    def __init__(self, df: pd.DataFrame) -> None:
        """
        :param df (object): to work with a pandas DataFrame in particular
        """
        self.df = df
    
    def isempty(self) -> bool:
        """Check if DataFrame is empty
        
        :return check (bool): application exit
        """
        if self.df.empty:
            print('No songs downloaded. Finishing execution')
            return False
    
    def isuinique(self, column_name: str) -> None:
        """Primary Key Check
        
        :param column_name (str): specify the DataFrame column name
        """
        if pd.Series(self.df[column_name]).is_unique: # verify column name to find some duplicated value
            pass
        else:
            raise Exception('Primary Key Check is violated')

    def isnull(self) -> None:
        """Check for nulls values"""
        if self.df.isnull().values.any(): # if any nullable value was found out, an exception it will raised
            raise Exception('Null valued found')