import numpy as np
import pandas as pd
df = pd.read_csv("/home/user/task/data/business_metrics.csv")
print(df.head())
df["amount"]=int(df(df["amount"]))
print(df.head())

df["status"]=df["status"].trim()
print(df["txn_date"].groupby("date"))