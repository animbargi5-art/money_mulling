"""
Advanced Machine Learning based money muling detection with enhanced accuracy
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from datetime import datetime, timedelta
import logging
import hashlib
import re

logger = logging.getLogger(__name__)

class AdvancedMoneyMulingDetector:
    def __init__(self):
        # Use multiple models for ensemble prediction
        self.anomaly_model = IsolationForest(
            contamination=0.15, 
            random_state=42,
            n_estimators=200,
            max_samples='auto'
        )
        self.classification_model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        
        # Use RobustScaler for better handling of outliers
        self.scaler = RobustScaler()
        self.is_trained = False
        
        # Account behavior tracking
        self.account_history = {}
        self.suspicious_patterns = {
            'rapid_transactions': [],
            'round_amounts': [],
            'unusual_times': [],
            'high_velocity': []
        }
        
    def extract_advanced_features(self, transaction):
        """Extract comprehensive features from transaction"""
        try:
            timestamp = datetime.fromisoformat(transaction['timestamp'])
            hour = timestamp.hour
            day_of_week = timestamp.weekday()
            amount = float(transaction['amount'])
            
            # Basic temporal features
            basic_features = {
                'amount': amount,
                'hour': hour,
                'day_of_week': day_of_week,
                'is_weekend': 1 if day_of_week >= 5 else 0,
                'is_night': 1 if hour < 6 or hour > 22 else 0,
                'amount_log': np.log1p(amount),
            }
            
            # Advanced behavioral features
            advanced_features = {
                # Amount patterns
                'is_round_amount': 1 if amount % 100 == 0 or amount % 1000 == 0 else 0,
                'amount_category': self._categorize_amount(amount),
                'amount_zscore': self._calculate_amount_zscore(amount),
                
                # Temporal patterns
                'is_business_hours': 1 if 9 <= hour <= 17 and day_of_week < 5 else 0,
                'is_suspicious_time': 1 if hour in [0, 1, 2, 3, 23] else 0,
                'hour_sin': np.sin(2 * np.pi * hour / 24),
                'hour_cos': np.cos(2 * np.pi * hour / 24),
                'day_sin': np.sin(2 * np.pi * day_of_week / 7),
                'day_cos': np.cos(2 * np.pi * day_of_week / 7),
                
                # Account behavior features
                'sender_risk': self._get_account_risk(transaction.get('sender_account', '')),
                'receiver_risk': self._get_account_risk(transaction.get('receiver_account', '')),
                'account_similarity': self._check_account_similarity(
                    transaction.get('sender_account', ''), 
                    transaction.get('receiver_account', '')
                ),
                
                # Velocity features
                'transaction_velocity': self._calculate_velocity(transaction),
                'amount_velocity': self._calculate_amount_velocity(transaction),
            }
            
            # Combine all features
            all_features = {**basic_features, **advanced_features}
            return all_features
            
        except Exception as e:
            logger.error(f"Advanced feature extraction error: {e}")
            return None
    
    def _categorize_amount(self, amount):
        """Categorize transaction amount"""
        if amount < 100:
            return 1  # Micro
        elif amount < 1000:
            return 2  # Small
        elif amount < 10000:
            return 3  # Medium
        elif amount < 50000:
            return 4  # Large
        else:
            return 5  # Very Large
    
    def _calculate_amount_zscore(self, amount):
        """Calculate z-score for amount based on typical transaction patterns"""
        # Typical transaction amounts follow log-normal distribution
        typical_mean = 1000
        typical_std = 2000
        return abs(amount - typical_mean) / typical_std
    
    def _get_account_risk(self, account_id):
        """Get historical risk score for an account"""
        if not account_id:
            return 0.5
        
        account_hash = hashlib.md5(account_id.encode()).hexdigest()[:8]
        
        # Simulate account risk based on hash (deterministic but pseudo-random)
        risk_score = (int(account_hash, 16) % 100) / 100
        
        # Adjust based on account patterns
        if account_id in self.account_history:
            history = self.account_history[account_id]
            if history['transaction_count'] > 10:
                risk_score *= 0.8  # Established accounts are less risky
            if history['avg_amount'] > 50000:
                risk_score *= 1.3  # High-value accounts are riskier
        
        return min(1.0, risk_score)
    
    def _check_account_similarity(self, sender, receiver):
        """Check if sender and receiver accounts are suspiciously similar"""
        if not sender or not receiver:
            return 0
        
        # Check for similar patterns (simplified)
        if len(sender) == len(receiver):
            similarity = sum(1 for a, b in zip(sender, receiver) if a == b) / len(sender)
            return similarity
        
        return 0
    
    def _calculate_velocity(self, transaction):
        """Calculate transaction velocity for the account"""
        account = transaction.get('sender_account', '')
        if not account:
            return 0
        
        current_time = datetime.fromisoformat(transaction['timestamp'])
        
        if account not in self.account_history:
            self.account_history[account] = {
                'transactions': [],
                'transaction_count': 0,
                'total_amount': 0,
                'avg_amount': 0,
                'last_transaction': current_time
            }
        
        history = self.account_history[account]
        
        # Calculate transactions in last hour
        recent_transactions = [
            t for t in history['transactions'] 
            if (current_time - t['timestamp']).total_seconds() < 3600
        ]
        
        # Update history
        history['transactions'].append({
            'timestamp': current_time,
            'amount': float(transaction['amount'])
        })
        history['transaction_count'] += 1
        history['total_amount'] += float(transaction['amount'])
        history['avg_amount'] = history['total_amount'] / history['transaction_count']
        history['last_transaction'] = current_time
        
        # Keep only recent transactions (last 24 hours)
        cutoff_time = current_time - timedelta(hours=24)
        history['transactions'] = [
            t for t in history['transactions'] 
            if t['timestamp'] > cutoff_time
        ]
        
        return len(recent_transactions)
    
    def _calculate_amount_velocity(self, transaction):
        """Calculate amount velocity (total amount in recent period)"""
        account = transaction.get('sender_account', '')
        if not account or account not in self.account_history:
            return 0
        
        current_time = datetime.fromisoformat(transaction['timestamp'])
        history = self.account_history[account]
        
        # Calculate total amount in last 6 hours
        recent_amount = sum(
            t['amount'] for t in history['transactions']
            if (current_time - t['timestamp']).total_seconds() < 21600  # 6 hours
        )
        
        return recent_amount / 10000  # Normalize
    
    def generate_enhanced_synthetic_data(self, n_samples=2000):
        """Generate more realistic synthetic transaction data"""
        np.random.seed(42)
        
        features_list = []
        labels = []
        
        # Generate normal transactions (80%)
        normal_count = int(n_samples * 0.8)
        for _ in range(normal_count):
            # Normal business patterns
            hour = np.random.choice(range(9, 17))  # Simplified to avoid probability array issues
            day = np.random.choice(range(0, 5))  # Weekdays
            amount = np.random.lognormal(mean=6.5, sigma=1.2)
            
            features = self._create_feature_vector(amount, hour, day, is_suspicious=False)
            features_list.append(features)
            labels.append(0)  # Normal
        
        # Generate suspicious transactions (20%)
        suspicious_count = int(n_samples * 0.2)
        for _ in range(suspicious_count):
            # Suspicious patterns
            rand_val = np.random.random()
            if rand_val < 0.4:
                # Late night transactions
                hour = np.random.choice([0, 1, 2, 3, 23])
                day = np.random.choice(range(0, 7))
                amount = np.random.lognormal(mean=8.5, sigma=0.8)  # Higher amounts
            elif rand_val < 0.7:
                # Round amounts
                hour = np.random.choice(range(0, 24))
                day = np.random.choice(range(0, 7))
                amount = np.random.choice([1000, 2000, 5000, 10000, 15000, 20000])
            else:
                # Weekend high-value transactions
                hour = np.random.choice(range(0, 24))
                day = np.random.choice([5, 6])  # Weekend
                amount = np.random.lognormal(mean=9, sigma=0.6)
            
            features = self._create_feature_vector(amount, hour, day, is_suspicious=True)
            features_list.append(features)
            labels.append(1)  # Suspicious
        
        # Ensure we have exactly n_samples
        total_generated = len(features_list)
        if total_generated < n_samples:
            # Add more normal transactions to reach n_samples
            for _ in range(n_samples - total_generated):
                hour = np.random.choice(range(9, 17))
                day = np.random.choice(range(0, 5))
                amount = np.random.lognormal(mean=6.5, sigma=1.2)
                features = self._create_feature_vector(amount, hour, day, is_suspicious=False)
                features_list.append(features)
                labels.append(0)
        
        return np.array(features_list), np.array(labels)
    
    def _create_feature_vector(self, amount, hour, day, is_suspicious=False):
        """Create feature vector for synthetic data"""
        features = [
            amount,
            hour,
            day,
            1 if day >= 5 else 0,  # is_weekend
            1 if hour < 6 or hour > 22 else 0,  # is_night
            np.log1p(amount),  # amount_log
            1 if amount % 100 == 0 or amount % 1000 == 0 else 0,  # is_round_amount
            1 if amount < 100 else 2 if amount < 1000 else 3 if amount < 10000 else 4 if amount < 50000 else 5,  # amount_category
            abs(amount - 1000) / 2000,  # amount_zscore
            1 if 9 <= hour <= 17 and day < 5 else 0,  # is_business_hours
            1 if hour in [0, 1, 2, 3, 23] else 0,  # is_suspicious_time
            np.sin(2 * np.pi * hour / 24),  # hour_sin
            np.cos(2 * np.pi * hour / 24),  # hour_cos
            np.sin(2 * np.pi * day / 7),  # day_sin
            np.cos(2 * np.pi * day / 7),  # day_cos
            np.random.random() * 0.5 if is_suspicious else np.random.random() * 0.3,  # sender_risk
            np.random.random() * 0.5 if is_suspicious else np.random.random() * 0.3,  # receiver_risk
            np.random.random() * 0.3 if is_suspicious else np.random.random() * 0.1,  # account_similarity
            np.random.poisson(3) if is_suspicious else np.random.poisson(1),  # transaction_velocity
            np.random.exponential(2) if is_suspicious else np.random.exponential(0.5),  # amount_velocity
        ]
        return features
    
    def train(self):
        """Train both anomaly detection and classification models"""
        try:
            # Generate enhanced synthetic training data
            X, y = self.generate_enhanced_synthetic_data()
            
            # Split data for classification model
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Fit scaler
            X_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train anomaly detection model (unsupervised)
            self.anomaly_model.fit(X_scaled)
            
            # Train classification model (supervised)
            self.classification_model.fit(X_scaled, y_train)
            
            # Evaluate classification model
            y_pred = self.classification_model.predict(X_test_scaled)
            accuracy = np.mean(y_pred == y_test)
            
            self.is_trained = True
            
            logger.info(f"Enhanced money muling detection models trained successfully")
            logger.info(f"Classification accuracy: {accuracy:.3f}")
            
            return True
        except Exception as e:
            logger.error(f"Training error: {e}")
            return False
    
    def predict_risk(self, transaction):
        """Predict risk score using ensemble of models"""
        if not self.is_trained:
            self.train()
        
        features = self.extract_advanced_features(transaction)
        if features is None:
            return 0.5  # Default medium risk
        
        try:
            # Convert to array and scale
            feature_array = np.array(list(features.values())).reshape(1, -1)
            scaled_features = self.scaler.transform(feature_array)
            
            # Get predictions from both models
            anomaly_score = self.anomaly_model.decision_function(scaled_features)[0]
            classification_proba = self.classification_model.predict_proba(scaled_features)[0][1]
            
            # Ensemble prediction (weighted average)
            anomaly_risk = max(0, min(1, (0.5 - anomaly_score) * 2))  # Convert to 0-1 scale
            classification_risk = classification_proba
            
            # Weighted ensemble (60% classification, 40% anomaly)
            final_risk = 0.6 * classification_risk + 0.4 * anomaly_risk
            
            # Apply business rules for additional accuracy
            final_risk = self._apply_business_rules(transaction, final_risk)
            
            return min(1.0, max(0.0, final_risk))
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return 0.5  # Default medium risk
    
    def _apply_business_rules(self, transaction, base_risk):
        """Apply business rules to adjust risk score"""
        try:
            amount = float(transaction['amount'])
            timestamp = datetime.fromisoformat(transaction['timestamp'])
            hour = timestamp.hour
            
            adjusted_risk = base_risk
            
            # High amount transactions
            if amount > 50000:
                adjusted_risk *= 1.3
            elif amount > 20000:
                adjusted_risk *= 1.2
            
            # Suspicious timing
            if hour in [0, 1, 2, 3, 23]:
                adjusted_risk *= 1.4
            
            # Weekend transactions
            if timestamp.weekday() >= 5:
                adjusted_risk *= 1.1
            
            # Round amounts (potential structuring)
            if amount % 1000 == 0 and amount >= 5000:
                adjusted_risk *= 1.2
            
            return min(1.0, adjusted_risk)
            
        except Exception as e:
            logger.error(f"Business rules error: {e}")
            return base_risk

# Global enhanced detector instance
detector = AdvancedMoneyMulingDetector()