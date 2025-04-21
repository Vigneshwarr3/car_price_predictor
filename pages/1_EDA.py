import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

column_display_names = {
    "make": "Car Make",
    "model": "Car Model",
    "bodyType": "Body Type",
    "seats": "Number of Seats",
    "numOfOwners": "Number of Previous Owners",
    "fuelType": "Fuel Type",
    "horsePower": "Horsepower",
    "driveTrain": "Drivetrain",
    "transmission": "Transmission Type",
    "mileage": "Miles Driven",
    "mpgCity": "MPG (City)",
    "mpgHighway": "MPG (Highway)",
    "evRange": "EV Range (mi)",
    "evMpgeCity": "EV MPGe (City)",
    "evMpgeHighway": "EV MPGe (Highway)",
    "hasReportedAccident": "Reported Accident",
    "price": "Price ($)",
    "age": "Vehicle Age (years)"
}

display_to_column = {
    "Car Make": "make",
    "Car Model": "model",
    "Body Type": "bodyType",
    "Number of Seats": "seats",
    "Number of Previous Owners": "numOfOwners",
    "Fuel Type": "fuelType",
    "Horsepower": "horsePower",
    "Drivetrain": "driveTrain",
    "Transmission Type": "transmission",
    "Miles Driven": "mileage",
    "MPG (City)": "mpgCity",
    "MPG (Highway)": "mpgHighway",
    "EV Range (mi)": "evRange",
    "EV MPGe (City)": "evMpgeCity",
    "EV MPGe (Highway)": "evMpgeHighway",
    "Reported Accident": "hasReportedAccident",
    "Price ($)": "price",
    "Vehicle Age (years)": "age"
}


# Format y-axis labels to K/M
def format_k_m(x, pos):
    if x >= 1_000_000:
        return f'{x/1_000_000:.1f}M'
    elif x >= 1_000:
        return f'{x/1_000:.0f}K'
    else:
        return f'{x:.0f}'

# General plotting function
def plot_box_and_count_by_column(df, column):
    # Order categories by average price
    order = df.groupby(column)['price'].mean().sort_values(ascending=False).index

    # If plotting "Car Make", use two rows
    if column in ['make', 'age']:
        fig, axes = plt.subplots(2, 1, figsize=(20, 17))
        if column == 'make':
            rotation = 90
        else:
            rotation = 0
    else:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        rotation = 0


    # Boxplot
    sns.boxplot(
        data=df,
        x=column,
        y='price',
        order=order,
        ax=axes[0],
        fliersize=2,
        flierprops=dict(marker='o', markersize=3, markerfacecolor='gray', alpha=0.3)
    )
    axes[0].set_title(f"Price by {column_display_names[column]}", fontsize=12)
    axes[0].set_xlabel(column_display_names[column])
    axes[0].set_ylabel("Price")
    axes[0].tick_params(axis='x', rotation=rotation)
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(format_k_m))

    # Countplot
    sns.countplot(
        data=df,
        x=column,
        order=df[column].value_counts().index,
        ax=axes[1]
    )
    for p in axes[1].patches:
        height = p.get_height()
        axes[1].annotate(f'{int(height)}', (p.get_x() + p.get_width() / 2., height),
                         ha='center', va='bottom', fontsize=9)
    axes[1].set_title(f"Count of {column_display_names[column]}", fontsize=12)
    axes[1].set_xlabel(column_display_names[column])
    axes[1].set_ylabel("Count")
    axes[1].tick_params(axis='x', rotation=rotation)

    plt.tight_layout()
    return fig


# Title
st.title("🔍 Interactive Column Visualizer")

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")
# name: key
headers = {API_KEY_NAME: API_KEY}
url = "https://server.tailca7ba6.ts.net/get-data" #change this url to the docker's url

@st.cache_data(ttl=3600)  # cache for 1 hour
def fetch_eda_data():
    res = requests.get(url, headers=headers, verify=False)
    if res.status_code == 200:
        return pd.DataFrame(res.json())
    else:
        st.error("❌ Failed to fetch EDA data.")
        return pd.DataFrame()

df = fetch_eda_data()

insight_dict = {
    "make" : """
    - 📦 **Box Plot** shows how car prices vary by make, highlighting medians, price spread, and outliers.
    - 💰 **Rivian, Porsche, and Maserati** have the highest median prices with wider variation.
    - 🚗 **Chevrolet, Ford, and Nissan** are the most listed makes, dominating the dataset.
    - 📊 **Chevrolet** leads with over **2200 listings**, showing high market availability.
    - 🔍 Makes like **smart, FIAT, and Genesis** have low listing counts, limiting their statistical significance.
""", 
    "bodyType" : """
- 🚘 **Trucks and Coupes** have the highest median prices among all body types.
- 🧳 **SUVs and Sedans** dominate the listings, making up the majority of the dataset.
- 💸 **Hatchbacks and Wagons** have the lowest median prices, ideal for budget-conscious buyers.
- ⚠️ **Minivans and Vans** have fewer listings, so conclusions should be made cautiously.
""",

    "fuelType": """
- 🔋 **Hybrid and Diesel** vehicles show higher median prices, reflecting efficiency or niche value.
- ⛽ **Gas-powered** vehicles overwhelmingly dominate the dataset with 16,000+ listings.
- ⚡ **Electric and Plug-In Hybrid** options show moderate pricing but are less frequent.
- 📉 **Flexible fuel types** are rare and typically priced lower.
""",

    "driveTrain": """
- ⚙️ **4WD and AWD** vehicles tend to have higher median prices than FWD and RWD.
- 🔧 **FWD** (Front-Wheel Drive) is the most common drivetrain by count.
- 🧊 **2WD** listings are rare and should be interpreted with care due to limited data.
""",

    "transmission": """
- 🕹️ **Manual transmissions** show slightly higher price variation.
- ⚙️ **Automatic** vehicles dominate the dataset with over 17,000 listings.
- 💡 Price difference between transmission types is minimal on average.
""",

    "seats": """
- 👨‍👩‍👧 Most vehicles have **5 seats**, making up the vast majority of listings.
- 🪑 Higher seat counts (6–10) show higher price ranges, often indicating larger SUVs or vans.
- ⚠️ Some listings with **0 or 1 seats** might be anomalies or data entry errors.
""",

    "numOfOwners": """
- 👤 Vehicles with **fewer previous owners (1–2)** tend to have higher prices.
- 📉 Price generally decreases as the number of previous owners increases.
- 📊 Majority of vehicles had 1 or 2 owners; 3+ is relatively rare.
""",

    "age": """
- ⏳ **Newer vehicles (1–3 years)** have higher prices, as expected.
- 📉 There is a steady decline in price as vehicle age increases.
- 🔢 Listing count drops off sharply after 10 years of age.
"""
}



# Title
st.subheader("📊 Boxplot + Countplot by Column")

# Dropdown for selecting column
categorical_cols = ["Car Make", "Body Type", "Fuel Type", "Drivetrain", "Transmission Type", "Number of Seats", "Number of Previous Owners", "Vehicle Age (years)"]
selected_col = st.selectbox("Select a categorical column:", categorical_cols)

# Generate the figure using your function
fig = plot_box_and_count_by_column(df, display_to_column[selected_col])
st.pyplot(fig)

st.subheader("📊 View Insights")
st.markdown(insight_dict.get(display_to_column[selected_col], "No insights available."))

# Numeric columns for scatter
cols = ["Vehicle Age (years)", "Miles Driven", "Horsepower", "Number of Previous Owners", "Number of Seats", "MPG (City)", "MPG (Highway)", "EV Range (mi)", "EV MPGe (City)", "EV MPGe (Highway)"]

st.divider()

st.subheader("📈 Scatter Plot")

# User selects x, y, and optional size/color
x_col = display_to_column[st.selectbox("X-axis:", cols, index=0)]
y_col = 'price'

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

sns.scatterplot(data=df, x=x_col, y=y_col, sizes=(30, 300), alpha=0.7, ax=ax, palette="viridis")
sns.regplot(data=df, x=x_col, y=y_col, scatter_kws={'alpha': 0.6, 's': 60}, line_kws={'color': 'red'}, ax=ax)

ax.set_title(f"{column_display_names[y_col]} vs {column_display_names[x_col]}")
ax.set_xlabel(column_display_names[x_col])
ax.set_ylabel(column_display_names[y_col])
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(format_k_m))
plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(format_k_m))

st.pyplot(fig)