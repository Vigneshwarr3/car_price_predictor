import streamlit as st
from PIL import Image

st.title("🚗 Used Car Price Prediction")

# Optional: Add a logo or illustration
image = Image.open("./Images/car_image.png")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(image)

st.markdown("""
Welcome to the **Used Car Price Analysis & Prediction App** — an interactive platform designed to help you explore car listings, compare predictive models, and estimate the price of a car based on its features.

### 🔍 What You Can Do:

- **EDA (Exploratory Data Analysis)**  
  Dive into interactive visualizations to explore trends in car prices, fuel types, body styles, mileage, and more.

- **Model Comparison**  
  Compare multiple machine learning models using evaluation metrics like Mean Squared Error and R² to understand which performs best.

- **Predict Price**  
  Input a car’s details (make, model, mileage, fuel type, etc.) and get an estimated selling price using the best-trained model.

---
### 👨‍💻 Technologies Used:
            
- Python  
- Selenium WebDriver + BeautifulSoup  
- Pandas, Matplotlib & Seaborn  
- Scikit-learn  
- FastAPI  
- Docker  
- Streamlit  
---

Enjoy exploring, analyzing, and predicting
""")
