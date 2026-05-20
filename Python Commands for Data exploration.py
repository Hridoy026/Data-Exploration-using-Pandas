import pandas as pd

import numpy as np

df=pd.read_csv("D:/updated_Snitch_Fashion_Sales_Uncleaned.csv")



# Clear unwanted formats and spaces from Column Names

df.columns=df.columns.str.strip()



# Check if Null values exist

print(df.isnull().sum())



# Data Cleaning

df["Customer_Name"]=df["Customer_Name"].str.lstrip("Dr.")

df["Customer_Name"]=df["Customer_Name"].str.rstrip('PhD')   # To clean more values, we will use python list.



# Data Filtering

df = df[df["Status"] != "Cancelled"]

df = df.drop(df[df["Status"] == "Cancelled"].index)



# Drop Null values from a column

df=df.dropna(subset="Sales_Amount")



# Multiple columns

df=df.dropna(subset=["Sales_Amount","Order_date"])



# Drop a whole column

df=df.drop(columns="Sales_Amount")



# Forward fill

df["Unit_Price"]=df.groupby("Product_Name")['Unit_Price'].ffill()



# Fill Null values 

df=df.fillna(df["Units_Sold"]*df['Unit_Price']*(1-df["Discount_%"]).fillna(0))

df["Sales_Amount"]=df["Sales_Amount"].replace(np.nan,0)   # For more cells to be replaced, we can use python dictionary where Key and Value will be divided by :



# Converting O to Null Values/NaN

cols = ['Price', 'Quantity', 'Total']

df[cols] = df[cols].replace(0, np.nan)



# Using fillna to fill null values by Statistics

df["Segment"]=df["Segment"].fillna(df["Segment"].mode()[0])



# Sort Values

df=df.sort_values("Sales_Amount", ascending=True)



# Date time convert for analysis

df["Order_Date"]=pd.to_datetime(df["Order_Date"],format="mixed",errors="coerce") # Use errors="Coerce" if any abnormal value exists in Date Column

df['Order_Date']=df["Order_Date"].dt.strftime("%d-%m-%y")



# Converting a non numeric column into numeric

df["Price"]=pd.to_numeric(df["Price"],errors="coerce")

# Set Index

df=df.set_index("Order_Date")



# Same Product Name Different Category Solution

print(df.groupby("Product")["Category"].value_counts(dropna=False))

df['Category'] = df['Category'].astype(str).str.lower().str.strip()

df['Category'] = df['Category'].replace(['nan', 'none', 'null'], np.nan)

df['Category'] = df.groupby('Product')['Category'].transform(lambda x: x.mode()[0] if not x.mode().empty else np.nan)

df_result = df.groupby('Product')['Category'].first().reset_index()



# Filling NaN values in Price and Quantity Columns when Products and Categories are different

df['Price'] = df['Price'].fillna(df.groupby('Product')['Price'].transform('median'))  # For Price, median is more preferable as it lays between Mean and Mode

df['Quantity'] = df['Quantity'].fillna(df.groupby('Product')['Quantity'].transform('median'))

df["Total"]=df["Quantity"]*df["Price"]  # For Total, multiplication of Quantity and Price is more preferable. 







# For Filling Null values
  # We can use interpolation which is more accurate for Forecasting

df['total'] = df['total'].interpolate(method='time')


print(df.head(50))