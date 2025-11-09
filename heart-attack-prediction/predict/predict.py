"""
Prediction script for heart attack risk
Fetches latest patient data from API and makes heart attack prediction
"""

import os
import requests
import joblib
import pandas as pd
import numpy as np
from datetime import datetime

# Configuration
# Allow overriding the API endpoint via environment variable so the script can target
# a hosted API (ngrok / Render / Railway etc.). Default remains the local endpoint.

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api/latest-entry")
MODEL_PATH = "heart_attack_model.pkl"
FEATURE_NAMES_PATH = "feature_names.pkl"

def fetch_latest_patient_data():
    """Fetch latest patient data from API"""
    print("HEART ATTACK PREDICTION SYSTEM")
    print("\n Fetching latest patient data from API...")
    print(f" API Endpoint: {API_URL}")
    
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("Data fetched successfully!")
        return data
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API")
        print("Make sure the API is running: python main.py")
        return None
    except requests.exceptions.Timeout:
        print("Error: API request timed out")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Error: API returned error {e.response.status_code}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def prepare_features(data):
    """Extract and prepare features for prediction"""
    print("\nPreparing data for prediction...")
    
    # Extract patient data
    patient = data['patient']
    medical_record = data['medical_record']
    
    # Create feature dictionary matching training data
    features = {
        'Age': patient['age'],
        'Gender': patient['gender'],
        'Heart rate': medical_record['heart_rate'],
        'Systolic blood pressure': medical_record['systolic_blood_pressure'],
        'Diastolic blood pressure': medical_record['diastolic_blood_pressure'],
        'Blood sugar': medical_record['blood_sugar'],
        'CK-MB': data['heart_attack_test']['ck_mb'],
        'Troponin': data['heart_attack_test']['troponin']
    }
    
    # Handle outliers (same as training)
    if features['Heart rate'] > 200:
        features['Heart rate'] = 80  # Use median value
    
    print("Data prepared!")
    return features

def display_patient_info(data, features):
    """Display patient information"""
    print("PATIENT INFORMATION")

    patient = data['patient']
    medical_record = data['medical_record']
    test = data['heart_attack_test']
    
    print(f"\n Patient ID: {patient['patient_id']}")
    print(f"   Age: {features['Age']} years")
    print(f"   Gender: {'Male' if features['Gender'] == 1 else 'Female'}")
    
    print(f"\n Vital Signs:")
    print(f"   Heart Rate: {features['Heart rate']} bpm")
    print(f"   Blood Pressure: {features['Systolic blood pressure']}/{features['Diastolic blood pressure']} mmHg")
    print(f"   Blood Sugar: {features['Blood sugar']} mg/dL")
    
    print(f"\n Cardiac Biomarkers:")
    print(f"   CK-MB: {features['CK-MB']}")
    print(f"   Troponin: {features['Troponin']}")
    
    print(f"\n Actual Result: {test['result'].upper()}")

def load_model():
    """Load trained machine learning model"""
    print("\n Loading prediction model...")
    
    try:
        model = joblib.load(MODEL_PATH)
        feature_names = joblib.load(FEATURE_NAMES_PATH)
        
        # Convert to list if it's a pandas Series
        if hasattr(feature_names, 'tolist'):
            feature_names = feature_names.tolist()
        
        print(f"Model loaded: Random Forest Classifier")
        print(f"Features: {len(feature_names)}")
        
        # Debug info
        if hasattr(model, 'feature_names_in_'):
            print("Expected features:", model.feature_names_in_)
            print("Provided features:", feature_names)
        
        return model, feature_names
    except FileNotFoundError:
        print(f"Error: Model file not found")
        print(f"Looking for: {MODEL_PATH}")
        return None, None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None
    
def make_prediction(model, feature_names, features):
    """Make prediction using the model"""
    print("Making prediction")
    
    try:
        # Create DataFrame with your features
        X = pd.DataFrame([features], columns=feature_names)
        
        # Reorder columns to match what the model expects
        if hasattr(model, 'feature_names_in_'):
            expected_features = model.feature_names_in_
            print(f"Reordering features to match model expectations")
            X = X[expected_features]  # Reorder columns to match training order
        
        # Make prediction
        prediction = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]
        confidence = max(probabilities) * 100
        
        return prediction, confidence, probabilities
        
    except Exception as e:
        print(f"Error making prediction: {e}")
        return None, None, None

def display_prediction(prediction, confidence, probability):
    """Display prediction results"""
    print("PREDICTION RESULTS")
    
    if prediction == 1:
        print("\n PREDICTION: POSITIVE")
        print(" Risk of heart attack detected")
        print(f" Confidence: {confidence:.1f}%")
    else:
        print("\n PREDICTION: NEGATIVE")
        print(" No immediate heart attack risk detected")
        print(f" Confidence: {confidence:.1f}%")
    
    print(f"\nProbability Breakdown:")
    print(f" Negative (No risk): {probability[0]*100:.1f}%")
    print(f" Positive (At risk): {probability[1]*100:.1f}%")

    # Risk interpretation
    risk_score = probability[1] * 100
    if risk_score < 30:
        risk_level = "LOW RISK"
        color = "(G)"
    elif risk_score < 70:
        risk_level = "MODERATE RISK"
        color = "(Y)"
    else:
        risk_level = "HIGH RISK"
        color = "(R)"
    
    print(f"\n{color} Risk Level: {risk_level}")

def main():
    """Main execution function"""
    
    # Step 1: Fetch data from API
    data = fetch_latest_patient_data()
    if data is None:
        print("\nCannot proceed without data")
        return
    
    # Step 2: Prepare features
    features = prepare_features(data)
    
    # Step 3: Display patient info
    display_patient_info(data, features)
    
    # Step 4: Load model
    model, feature_names = load_model()
    if model is None:
        print("\nCannot proceed without model")
        return
    
    # Step 5: Make prediction
    prediction, confidence, probability = make_prediction(model, feature_names, features)
    
    # Step 6: Display results
    display_prediction(prediction, confidence, probability)
    
    # Step 7: Compare with actual result
    actual_result = data['heart_attack_test']['result']
    predicted_result = 'positive' if prediction == 1 else 'negative'
    
    print(f"\nComparison:")
    print(f" Actual Result: {actual_result.upper()}")
    print(f" Predicted Result: {predicted_result.upper()}")

    if actual_result.lower() == predicted_result.lower():
        print("Prediction MATCHES actual result!")
    else:
        print("Prediction DIFFERS from actual result")

    print("PREDICTION COMPLETE")
   
    # Save prediction log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"\n[{timestamp}] Patient: {data['patient']['patient_id']}, Predicted: {predicted_result}, Actual: {actual_result}, Confidence: {confidence:.1f}%"
    
    with open("prediction_log.txt", "a") as f:
        f.write(log_entry)
    
    print(f"\nPrediction logged to prediction_log.txt")

if __name__ == "__main__":
    main()