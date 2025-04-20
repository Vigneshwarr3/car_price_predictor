import streamlit as st
from PIL import Image

# Title
st.title("📊 Model Performance Summary")

# Load and display the image
image = Image.open("./Images/model_summary.png")
st.image(image, caption="Model Comparison: MSE and R²")


# Description
st.markdown("""
### 🔍 Insights from the Model Evaluation

- **Gradient Boosting** performed the best overall, with the **lowest MSE** and the **highest R² (~0.83)**.
- **KNN Regressor** and **Decision Tree** also showed strong performance with R² scores above 0.78, indicating decent predictive power.
- **SVR (Support Vector Regressor)** underperformed significantly, showing the **highest MSE** and **lowest R² (~0.49)**.
- **Linear Regression**, **PLS Regression**, and **MLP Regressor** had moderate performance, with R² values ranging from **0.67 to 0.70**.
- This suggests that **non-linear models** like Gradient Boosting and KNN can capture the complexity in the data better than basic linear models.

➡️ Based on this analysis, I'm using **Gradient Boosting** for deployment.
""")
