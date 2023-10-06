import pandas as pd

class DataValidation:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
    
    # Check if dataframe is empty
    def isempty(self) -> bool:
        if self.df.empty:
            print('No songs downloaded. Finishing execution')
            return False
    
    # Primary Key Check
    def isuinique(self, column_name: str):
        if pd.Series(self.df[column_name]).is_unique: # verify column name to find some duplicated value
            pass
        else:
            raise Exception('Primary Key Check is violated')

    # Check for nulls
    def isnull(self) -> bool:
        if self.df.isnull().values.any(): # if any nullable value was found out, an exception it will raised
            raise Exception('Null valued found')