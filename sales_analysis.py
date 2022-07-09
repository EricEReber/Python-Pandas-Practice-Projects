import pandas as pd
import matplotlib.pyplot as plt
import os

# setter sammen filene til ett dataset
df = pd.DataFrame()
all_files = [file for file in os.listdir("./fiscal")]

for file in all_files:
    temp_df = pd.read_csv("./fiscal/" + file)
    df = pd.concat([df, temp_df])

# Remove duplicate rowsof description rows
df = df[df["Order Date"] != "Order Date"]

# rydder opp datasettet for NaNs slik vii videre kan behandle dataene
nan_df = df[df.isna().any(axis=1)]
nan_df.head()

#Ser at rader bestaar av NaN, fjerner dermed  via how=alll
df = df.dropna(how="all")

df.to_csv("all_data.csv", index=False)

#Find month with highest profit
df["Quantity Ordered"] = pd.to_numeric(df["Quantity Ordered"])
df["Price Each"] = pd.to_numeric(df["Price Each"])
df["Sales"] = df["Quantity Ordered"] * df["Price Each"]

df["Month"] = df["Order Date"].str[0:2].astype("int32")
monthly_sales = df.groupby("Month").sum()["Sales"]
months = range(1,13)

plt.bar(months, monthly_sales)
plt.xticks(months)
plt.xlabel("Month")
plt.ylabel("Sales in USD")
plt.title("Sales over months")
plt.show()


#Find the city with the  profit
df["City"] = df["Purchase Address"].apply(lambda x: x.split(',')[1] + " " + x.split(',')[2].split(' ')[1])

city_sales = df.groupby("City").sum()["Sales"]
cities = [city for city, temp in df.groupby("City")]

plt.bar(cities, city_sales)
plt.xticks(cities, rotation="vertical")
plt.ylabel("Sales in USD")
plt.xlabel("City name")
plt.title("Sales per city")
plt.show()


#Find the optimal time to advertise to maximize likelihood of customer buying product
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Hour"] = df["Order Date"].dt.hour
df["Minute"] = df["Order Date"].dt.minute
df["Count"] = 1

hours = [hour for hour, temp in df.groupby("Hour")]

plt.plot(hours, df.groupby(["Hour"]).count()["Count"])
plt.xticks(hours)
plt.xlabel("Hour")
plt.ylabel("# Orders")
plt.title("Orders time of day")
plt.grid()
plt.show()
