## Pandas Practice Project: SALES ANALYSIS
In this notebook I will execute basic pandas data science tasks in order to learn a new python library. Tasks include merging .CSV files into one dataset, cleaning dataset for NaN values and duplicates, sorting dataset and adding new columns for analysis, finding which month yeld the highest profit, at what time of day customers order products, and which products are often sold together, plotting these results via matplotlib and drawing conclusions.

Notebook was made on the basis of Keith Galli's youtube tutorial 'Solving real world data science tasks with Python Pandas!'


```python
import pandas as pd
import matplotlib.pyplot as plt
import os
```

1) The dataset is given month by month, each in a seperate .csv file. Since I will perform analysis for the whole year, I wish to combine these files into one .csv, along with removing empty (NaN) rows


```python
df = pd.DataFrame()
all_files = [file for file in os.listdir("./fiscal")]

for file in all_files:
    temp_df = pd.read_csv("./fiscal/" + file)
    df = pd.concat([df, temp_df])

# Remove duplicate description rows
df = df[df["Order Date"] != "Order Date"]

# Find NaN values
nan_df = df[df.isna().any(axis=1)]
nan_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Order ID</th>
      <th>Product</th>
      <th>Quantity Ordered</th>
      <th>Price Each</th>
      <th>Order Date</th>
      <th>Purchase Address</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>356</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>735</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1433</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1553</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Remove NaN rows
df = df.dropna(how="all")

# Combine data into one .csv
df.to_csv("all_data.csv", index=False)
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Order ID</th>
      <th>Product</th>
      <th>Quantity Ordered</th>
      <th>Price Each</th>
      <th>Order Date</th>
      <th>Purchase Address</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>176558</td>
      <td>USB-C Charging Cable</td>
      <td>2</td>
      <td>11.95</td>
      <td>04/19/19 08:46</td>
      <td>917 1st St, Dallas, TX 75001</td>
    </tr>
    <tr>
      <th>2</th>
      <td>176559</td>
      <td>Bose SoundSport Headphones</td>
      <td>1</td>
      <td>99.99</td>
      <td>04/07/19 22:30</td>
      <td>682 Chestnut St, Boston, MA 02215</td>
    </tr>
    <tr>
      <th>3</th>
      <td>176560</td>
      <td>Google Phone</td>
      <td>1</td>
      <td>600</td>
      <td>04/12/19 14:38</td>
      <td>669 Spruce St, Los Angeles, CA 90001</td>
    </tr>
    <tr>
      <th>4</th>
      <td>176560</td>
      <td>Wired Headphones</td>
      <td>1</td>
      <td>11.99</td>
      <td>04/12/19 14:38</td>
      <td>669 Spruce St, Los Angeles, CA 90001</td>
    </tr>
    <tr>
      <th>5</th>
      <td>176561</td>
      <td>Wired Headphones</td>
      <td>1</td>
      <td>11.99</td>
      <td>04/30/19 09:27</td>
      <td>333 8th St, Los Angeles, CA 90001</td>
    </tr>
  </tbody>
</table>
</div>



2) I wish to find the sales in USD every month. This sounds like a simple task but there is some groundwork to be done since the dataset does not have a column showing sales in USD, and the month the order occured is buried with other currently irrelevant information in the 'order date' column.


```python
# Columns are in String format
df["Quantity Ordered"] = pd.to_numeric(df["Quantity Ordered"])
df["Price Each"] = pd.to_numeric(df["Price Each"])

# New sales column
df["Sales"] = df["Quantity Ordered"] * df["Price Each"]

# New month column
df["Month"] = df["Order Date"].str[0:2].astype("int32")
monthly_sales = df.groupby("Month").sum()["Sales"]
months = range(1,13)

plt.bar(months, monthly_sales)
plt.xticks(months)
plt.xlabel("Month")
plt.ylabel("Sales in USD")
plt.title("Sales over months")
plt.show()
```


    
![png](output_6_0.png)
    


From the figure we can conclude that December had the most sales. Considering this dataset looks at electronics sales it's unsurprising that the peak occurs around Christmas time.

3) Next I want to find the city which is responsible for the most sales.


```python
# New city column. Added the state code because of duplicate named cities
df["City"] = df["Purchase Address"].apply(lambda x: x.split(',')[1] + " " + x.split(',')[2].split(' ')[1])

city_sales = df.groupby("City").sum()["Sales"]
cities = [city for city, temp in df.groupby("City")]

plt.bar(cities, city_sales)
plt.xticks(cities, rotation="vertical")
plt.ylabel("Sales in USD")
plt.xlabel("City name")
plt.title("Sales per city")
plt.show()
```


    
![png](output_9_0.png)
    


We conclude that San Francisco is responsible for the most sales. Note that this plot does not account for population size, meaning cities like Portland, Oregon don't perform as well even though they might have a greater sales per capita.

4) Finally I wish to find the time of day most sales occur


```python
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Hour"] = df["Order Date"].dt.hour
df["Minute"] = df["Order Date"].dt.minute
df["Count"] = 1

hours = [hour for hour, temp in df.groupby("Hour")]

plt.plot(hours, df.groupby(["Hour"]).count()["Count"])
plt.xticks(hours)
plt.xlabel("Hour")
plt.ylabel("Order Amount")
plt.title("Orders time of day")
plt.grid()
plt.show()
```


    
![png](output_12_0.png)
    


Looking at the figure we can identify peaks between 11-13, and between 18-20 with the highest peak at 19.
