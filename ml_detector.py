"""
Machine Learning based money muling detection
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class MoneyMulingDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def extract_features(self, transaction):
        """Extract features from transaction for ML model"""
        try:
            timestamp = datetime.fromisoformat(transaction['timestamp'])
            hour = timestamp.hour
            day_of_week = timestamp.weekday()
            
            features = {
                'amount': float(transaction['amount']),
                'hour': hour,
                'day_of_week': day_of_week,
                'is_weekend': 1 if day_of_week >= 5 else 0,
                'is_night': 1 if hour < 6 or hour > 22 else 0,
                'amount_log': np.log1p(float(transaction['amount'])),
            }
            
            return features
        except Exception as e:
            logger.error(f"Feature extraction error: {e}")
            return None
    
    def generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic transaction data for training"""
        np.random.seed(42)
        
        # Normal transactions
        normal_amounts = np.random.lognormal(mean=6, sigma=1.5, size=int(n_samples * 0.9))
        normal_hours = np.random.choice(range(8, 18), size=int(n_samples * 0.9))
        normal_days = np.random.choice(range(0, 5), size=int(n_samples * 0.9))
        
        # Suspicious transactions (money muling patterns)
        suspicious_amounts = np.random.lognormal(mean=8, sigma=0.5, size=int(n_samples * 0.1))
        suspicious_hours = np.random.choice([2, 3, 23, 0, 1], size=int(n_samples * 0.1))
        suspicious_days = np.random.choice(range(0, 7), size=int(n_samples * 0.1))
        
        # Combine data
        amounts = np.concatenate([normal_amounts, suspicious_amounts])
        hours = np.concatenate([normal_hours, suspicious_hours])
        days = np.concatenate([normal_days, suspicious_days])
        
        # Create feature matrix
        features = []
        for i in range(n_samples):
            feature_dict = {
                'amount': amounts[i],
                'hour': hours[i],
                'day_of_week': days[i],
                'is_weekend': 1 if days[i] >= 5 else 0,
                'is_night': 1 if hours[i] < 6 or hours[i] > 22 else 0,
                'amount_log': np.log1p(amounts[i]),
            }
            features.append(list(feature_dict.values()))
        
        return np.array(features)
    
    def train(self):
        """Train the anomaly detection model"""
        try:
            # Generate synthetic training data
            training_data = self.generate_synthetic_data()
            
            # Fit scaler and model
            scaled_data = self.scaler.fit_transform(training_data)
            self.model.fit(scaled_data)
            self.is_trained = True
            
            logger.info("Money muling detection model trained successfully")
            return True
        except Exception as e:
            logger.error(f"Training error: {e}")
            return False
    
    def predict_risk(self, transaction):
        """Predict risk score for a transaction"""
        if not self.is_trained:
            self.train()
        
        features = self.extract_features(transaction)
        if features is None:
            return 50  # Default medium risk
        
        try:
            # Convert to array and scale
            feature_array = np.array(list(features.values())).reshape(1, -1)
            scaled_features = self.scaler.transform(feature_array)
            
            # Get anomaly score
            anomaly_score = self.model.decision_function(scaled_features)[0]
            
            # Convert to risk score (0-100)
            # Anomaly scores are typically between -0.5 and 0.5
            # More negative = more anomalous = higher risk
            risk_score = max(0, min(100, (0.5 - anomaly_score) * 100))
            
            return int(risk_score)
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return 50  # Default medium risk

# Global detector instance
detector = MoneyMulingDetector()