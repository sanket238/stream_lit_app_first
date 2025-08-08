import pandas as pd

class Dataloader:

    def __init__(self,file_path):
        self.df=pd.read_csv(file_path)
        self.df['amount']=self.df["amount"].apply(self.to_inr)
        self.df['date']=pd.to_datetime(self.df['date'],errors="coerce")
        self.df['month']=self.df['date'].dt.month
        self.df['year']=self.df['date'].dt.year

    
    def to_inr(self,dollar):
        inr= dollar*87.5
        return round(inr/10000000,2)
        