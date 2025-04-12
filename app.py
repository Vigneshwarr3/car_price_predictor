from flask import Flask, request, jsonify
import pandas as pd
import joblib

# Load the trained pipeline
model = joblib.load('gb_pipeline.pkl')

# Start Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Gradient Boosting API is live 🚀"

@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON from POST
    data = request.get_json(force=True)

    # Convert to DataFrame (expecting a dict or list of dicts)
    input_df = pd.DataFrame([data]) if isinstance(data, dict) else pd.DataFrame(data)

    # Predict using the pipeline
    prediction = model.predict(input_df)

    # Return prediction as JSON
    return jsonify({'predicted_price': float(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)
