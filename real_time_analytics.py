"""
Real-time analytics and dashboard for AlgoGuard
Advanced monitoring and threat intelligence
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import logging
from collections import defaultdict, deque
import threading
import time

logger = logging.getLogger(__name__)

class RealTimeAnalytics:
    def __init__(self):
        self.transaction_stream = deque(maxlen=1000)  # Last 1000 transactions
        self.threat_intelligence = {
            'high_risk_accounts': set(),
            'suspicious_patterns': defaultdict(int),
            'geographic_risks': defaultdict(float),
            'time_based_risks': defaultdict(float)
        }
        
        # Real-time metrics
        self.metrics = {
            'total_transactions': 0,
            'high_risk_count': 0,
            'medium_risk_count': 0,
            'low_risk_count': 0,
            'blocked_transactions': 0,
            'false_positives': 0,
            'avg_response_time': 0,
            'system_uptime': datetime.now(),
            'last_update': datetime.now()
        }
        
        # Performance tracking
        self.performance_history = deque(maxlen=100)
        self.alert_queue = deque(maxlen=50)
        
        # Start background analytics
        self.start_background_processing()
    
    def add_transaction(self, transaction_data, risk_result):
        """Add transaction to real-time stream"""
        timestamp = datetime.now()
        
        # Enhanced transaction record
        enhanced_record = {
            'timestamp': timestamp.isoformat(),
            'transaction_id': transaction_data.get('transaction_id'),
            'amount': float(transaction_data.get('amount', 0)),
            'sender': transaction_data.get('sender_account', ''),
            'receiver': transaction_data.get('receiver_account', ''),
            'risk_score': risk_result.get('risk_score', 0),
            'risk_level': risk_result.get('risk_level', 'LOW'),
            'ml_confidence': risk_result.get('confidence', 0.5),
            'flags': risk_result.get('flags', []),
            'processing_time': risk_result.get('processing_time', 0)
        }
        
        self.transaction_stream.append(enhanced_record)
        self.update_metrics(enhanced_record)
        self.update_threat_intelligence(enhanced_record)
        
        # Generate alerts for high-risk transactions
        if enhanced_record['risk_level'] == 'HIGH':
            self.generate_alert(enhanced_record)
    
    def update_metrics(self, transaction):
        """Update real-time metrics"""
        self.metrics['total_transactions'] += 1
        self.metrics['last_update'] = datetime.now()
        
        risk_level = transaction['risk_level']
        if risk_level == 'HIGH':
            self.metrics['high_risk_count'] += 1
        elif risk_level == 'MEDIUM':
            self.metrics['medium_risk_count'] += 1
        else:
            self.metrics['low_risk_count'] += 1
        
        # Update average response time
        if transaction['processing_time'] > 0:
            current_avg = self.metrics['avg_response_time']
            total_txns = self.metrics['total_transactions']
            self.metrics['avg_response_time'] = (
                (current_avg * (total_txns - 1) + transaction['processing_time']) / total_txns
            )
    
    def update_threat_intelligence(self, transaction):
        """Update threat intelligence database"""
        if transaction['risk_level'] == 'HIGH':
            # Add to high-risk accounts
            self.threat_intelligence['high_risk_accounts'].add(transaction['sender'])
            self.threat_intelligence['high_risk_accounts'].add(transaction['receiver'])
        
        # Track suspicious patterns
        hour = datetime.fromisoformat(transaction['timestamp']).hour
        if hour in [0, 1, 2, 3, 23]:  # Late night
            self.threat_intelligence['time_based_risks'][hour] += 0.1
        
        # Track amount patterns
        amount = transaction['amount']
        if amount % 1000 == 0 and amount >= 5000:
            self.threat_intelligence['suspicious_patterns']['round_amounts'] += 1
        
        if amount > 50000:
            self.threat_intelligence['suspicious_patterns']['large_amounts'] += 1
    
    def generate_alert(self, transaction):
        """Generate real-time alert for high-risk transaction"""
        alert = {
            'id': f"ALERT_{len(self.alert_queue) + 1:04d}",
            'timestamp': transaction['timestamp'],
            'severity': 'HIGH',
            'type': 'SUSPICIOUS_TRANSACTION',
            'transaction_id': transaction['transaction_id'],
            'amount': transaction['amount'],
            'risk_score': transaction['risk_score'],
            'description': f"High-risk transaction detected: ${transaction['amount']:,.2f}",
            'recommended_action': 'IMMEDIATE_REVIEW',
            'flags': transaction['flags']
        }
        
        self.alert_queue.append(alert)
        logger.warning(f"HIGH RISK ALERT: {alert['description']}")
    
    def get_dashboard_data(self):
        """Get comprehensive dashboard data"""
        current_time = datetime.now()
        
        # Calculate uptime
        uptime_delta = current_time - self.metrics['system_uptime']
        uptime_hours = uptime_delta.total_seconds() / 3600
        
        # Recent transaction trends (last hour)
        recent_transactions = [
            t for t in self.transaction_stream 
            if (current_time - datetime.fromisoformat(t['timestamp'])).total_seconds() < 3600
        ]
        
        # Risk distribution
        risk_distribution = {
            'high': len([t for t in recent_transactions if t['risk_level'] == 'HIGH']),
            'medium': len([t for t in recent_transactions if t['risk_level'] == 'MEDIUM']),
            'low': len([t for t in recent_transactions if t['risk_level'] == 'LOW'])
        }
        
        # Hourly transaction volume
        hourly_volume = defaultdict(int)
        for transaction in recent_transactions:
            hour = datetime.fromisoformat(transaction['timestamp']).hour
            hourly_volume[hour] += 1
        
        # Top risk factors
        top_risk_factors = [
            {'factor': 'Large Amounts', 'count': self.threat_intelligence['suspicious_patterns']['large_amounts']},
            {'factor': 'Round Amounts', 'count': self.threat_intelligence['suspicious_patterns']['round_amounts']},
            {'factor': 'High-Risk Accounts', 'count': len(self.threat_intelligence['high_risk_accounts'])},
        ]
        
        return {
            'system_metrics': {
                **self.metrics,
                'uptime_hours': round(uptime_hours, 2),
                'transactions_per_hour': len(recent_transactions),
                'risk_detection_rate': (
                    (self.metrics['high_risk_count'] + self.metrics['medium_risk_count']) / 
                    max(1, self.metrics['total_transactions']) * 100
                )
            },
            'risk_distribution': risk_distribution,
            'hourly_volume': dict(hourly_volume),
            'recent_alerts': list(self.alert_queue)[-10:],  # Last 10 alerts
            'threat_intelligence': {
                'high_risk_accounts_count': len(self.threat_intelligence['high_risk_accounts']),
                'suspicious_patterns': dict(self.threat_intelligence['suspicious_patterns']),
                'top_risk_factors': top_risk_factors
            },
            'performance_stats': {
                'avg_response_time': round(self.metrics['avg_response_time'], 3),
                'system_health': 'EXCELLENT' if self.metrics['avg_response_time'] < 0.5 else 'GOOD',
                'last_update': self.metrics['last_update'].isoformat()
            }
        }
    
    def get_advanced_analytics(self):
        """Get advanced analytics and predictions"""
        if len(self.transaction_stream) < 10:
            return {'message': 'Insufficient data for advanced analytics'}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(list(self.transaction_stream))
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        
        # Risk trend analysis
        risk_trend = df.groupby(df['timestamp'].dt.floor('H'))['risk_score'].mean().tail(24)
        
        # Pattern detection
        patterns = {
            'peak_risk_hours': df.groupby('hour')['risk_score'].mean().nlargest(3).to_dict(),
            'risk_by_day': df.groupby('day_of_week')['risk_score'].mean().to_dict(),
            'amount_risk_correlation': df['amount'].corr(df['risk_score']),
            'high_risk_percentage': (df['risk_level'] == 'HIGH').mean() * 100
        }
        
        # Predictions (simple trend-based)
        recent_risk_scores = df.tail(20)['risk_score'].values
        if len(recent_risk_scores) >= 5:
            trend = np.polyfit(range(len(recent_risk_scores)), recent_risk_scores, 1)[0]
            prediction = {
                'trend_direction': 'INCREASING' if trend > 0.01 else 'DECREASING' if trend < -0.01 else 'STABLE',
                'trend_strength': abs(trend),
                'next_hour_risk_estimate': max(0, min(1, recent_risk_scores[-1] + trend))
            }
        else:
            prediction = {'message': 'Insufficient data for trend analysis'}
        
        return {
            'risk_trends': {k.isoformat(): v for k, v in risk_trend.items()},
            'patterns': patterns,
            'predictions': prediction,
            'data_quality': {
                'total_samples': len(df),
                'time_span_hours': (df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 3600,
                'completeness': 100.0  # Assuming complete data
            }
        }
    
    def start_background_processing(self):
        """Start background analytics processing"""
        def background_worker():
            while True:
                try:
                    # Clean old data
                    self.cleanup_old_data()
                    
                    # Update threat intelligence
                    self.update_background_intelligence()
                    
                    time.sleep(60)  # Run every minute
                except Exception as e:
                    logger.error(f"Background processing error: {e}")
                    time.sleep(60)
        
        thread = threading.Thread(target=background_worker, daemon=True)
        thread.start()
    
    def cleanup_old_data(self):
        """Clean up old data to maintain performance"""
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(hours=24)
        
        # Remove old alerts
        self.alert_queue = deque([
            alert for alert in self.alert_queue 
            if datetime.fromisoformat(alert['timestamp']) > cutoff_time
        ], maxlen=50)
    
    def update_background_intelligence(self):
        """Update threat intelligence in background"""
        # Decay old threat intelligence
        for hour in self.threat_intelligence['time_based_risks']:
            self.threat_intelligence['time_based_risks'][hour] *= 0.99  # Gradual decay

# Global analytics instance
analytics = RealTimeAnalytics()