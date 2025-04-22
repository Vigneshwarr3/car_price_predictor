# 🚗 Carvana Used Car Price Prediction

This project involves building a machine learning pipeline to predict used car prices using data scraped from Carvana. The pipeline includes data collection, preprocessing, model evaluation, API deployment, and a user-friendly Streamlit app.

Project link: [findyourcarprice.streamlit.app](https://findyourcarprice.streamlit.app/)

## 📊 Project Highlights

- **Data Collection**: Scraped over **19,000** used car listings from the [Carvana website](https://www.carvana.com/cars) using **Selenium WebDriver** and **BeautifulSoup**.
- **Data Cleaning**: Processed and cleaned raw HTML data into a structured format using **Pandas** to make it ML-ready.
- **Model Training**: Tested **7 regression models** using **Scikit-learn**:
  - Linear Regression  
  - KNN Regressor  
  - Gradient Boosting Regressor  
  - Support Vector Regressor (SVR)  
  - Decision Tree Regressor  
  - Partial Least Squares (PLS)  
  - Multi-layer Perceptron (MLP)  
  The best-performing model was selected based on performance metrics such as RMSE and R².
- **API Deployment**: Built a **FastAPI** backend with **API key & token-based authentication** for secure access to:
  - Fetch cleaned vehicle data
  - Predict car prices using the trained model  
  The API is containerized and deployed on a private server using **Docker**.
- **Frontend Interface**: Developed a **Streamlit** web application that allows users to:
  - Enter vehicle specifications
  - Get real-time price predictions from the trained ML model  

## 📁 Dataset

You can find the scraped data on **Kaggle** here:  
🔗 [Carvana Used Car Dataset on Kaggle](https://www.kaggle.com/datasets/vigneshwarr3/carvana-used-cars-dataset/data)

## 🚀 Tech Stack

- Python  
- Selenium WebDriver + BeautifulSoup  
- Pandas, Matplotlib & Seaborn  
- Scikit-learn  
- FastAPI  
- Docker  
- Streamlit  

## 📸 Screenshots

![Price Prediction UI](/Images/prediction_UI.png)
![EDA UI](/Images/EDA_UI.png)

## 📬 Contact

For any queries or contributions, feel free to reach out me through [LinkedIn](https://www.linkedin.com/in/vigneshwarravirao/)

---