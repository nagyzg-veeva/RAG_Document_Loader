import pandas as pd
from utils.csv_transformer import DataFrameTransformer


df = pd.read_csv("tracker.csv")
print(df.head())

result = DataFrameTransformer.transform(
    df, 
    content_columns=['Question / Issue / Action','Area','Type','Topic','Notes','Imppact','Orgs','Response'],
    metadata_columns=['Date Created', 'Date Closed'])


print(result)