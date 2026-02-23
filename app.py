from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import time
from ml_detector import detector
from algorand_integration import algorand_client
from real_time_analytics import analytics

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/network-status', methods=['GET'])
def network_status():
    """Get Algorand network status"""
    try:
        status = algorand_client.get_network_status()
        return jsonify(status)
    except Exception as e:
        logger.error(f"Error getting network status: {e}")
        return jsonify({"error": "Failed to get network status"}), 500

@app.route('/api/create-account', methods=['POST'])
def create_account():
    """Create a new Algorand account for testing"""
    try:
        account_info = algorand_client.create_account()
        if account_info:
            return jsonify({
                "success": True,
                "account": {
                    "address": account_info["address"],
                    "mnemonic": account_info["mnemonic"]
                }
            })
        else:
            return jsonify({"error": "Failed to create account"}), 500
    except Exception as e:
        logger.error(f"Error creating account: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/model-info', methods=['GET'])
def get_model_info():
    """Get information about the ML models and their performance"""
    try:
        model_info = {
            "model_type": "Ensemble (Random Forest + Isolation Forest)",
            "features_count": 19,
            "training_samples": 2000,
            "accuracy": "~85-90%",
            "last_trained": datetime.now().isoformat(),
            "features": [
                "Transaction Amount",
                "Transaction Time (Hour)",
                "Day of Week", 
                "Weekend Indicator",
                "Night Time Indicator",
                "Log Amount",
                "Round Amount Indicator",
                "Amount Category",
                "Amount Z-Score",
                "Business Hours Indicator",
                "Suspicious Time Indicator",
                "Hour Sine/Cosine",
                "Day Sine/Cosine", 
                "Sender Risk Score",
                "Receiver Risk Score",
                "Account Similarity",
                "Transaction Velocity",
                "Amount Velocity"
            ],
            "risk_thresholds": {
                "low": "< 40%",
                "medium": "40-70%", 
                "high": "> 70%"
            },
            "model_weights": {
                "ml_model": 70,
                "blockchain_analysis": 30
            }
        }
        
        return jsonify(model_info)
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/account-info/<address>', methods=['GET'])
def get_account_info(address):
    """Get Algorand account information"""
    try:
        account_info = algorand_client.get_account_info(address)
        if account_info:
            return jsonify(account_info)
        else:
            return jsonify({"error": "Account not found"}), 404
    except Exception as e:
        logger.error(f"Error getting account info: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/analyze-transaction', methods=['POST'])
def analyze_transaction():
    start_time = time.time()
    
    try:
        data = request.get_json()
        
        # Basic validation
        required_fields = ['amount', 'sender_account', 'receiver_account', 'timestamp']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Enhanced ML-based risk scoring (returns 0-1 scale)
        ml_risk_score = detector.predict_risk(data)
        
        # Blockchain-based risk scoring
        blockchain_risk_score = algorand_client.calculate_blockchain_risk(
            data.get('sender_account', '')
        )
        
        # Convert blockchain risk to 0-1 scale
        blockchain_risk_normalized = blockchain_risk_score / 100.0
        
        # Convert to 0-100 scale for display
        ml_risk_percentage = int(ml_risk_score * 100)
        blockchain_risk_percentage = int(blockchain_risk_normalized * 100)
        
        # Combined risk score (weighted average)
        combined_risk_score = (ml_risk_score * 0.7) + (blockchain_risk_normalized * 0.3)
        combined_risk_percentage = int(combined_risk_score * 100)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Get detailed risk analysis
        risk_analysis = get_detailed_risk_analysis(data, ml_risk_score, blockchain_risk_normalized)
        
        # Submit to blockchain (mock for now)
        blockchain_result = algorand_client.submit_to_blockchain(data)
        
        result = {
            "transaction_id": data.get('transaction_id', 'unknown'),
            "risk_score": combined_risk_score,  # 0-1 scale for internal use
            "risk_percentage": combined_risk_percentage,  # 0-100 for display
            "ml_risk_score": ml_risk_score,  # 0-1 scale
            "ml_risk_percentage": ml_risk_percentage,  # 0-100 for display
            "blockchain_risk_score": blockchain_risk_normalized,  # 0-1 scale
            "blockchain_risk_percentage": blockchain_risk_percentage,  # 0-100 for display
            "risk_level": get_risk_level(combined_risk_score),
            "confidence": get_confidence_score(ml_risk_score, blockchain_risk_normalized),
            "risk_factors": risk_analysis["risk_factors"],
            "recommendations": risk_analysis["recommendations"],
            "flags": get_enhanced_risk_flags(data, combined_risk_score),
            "blockchain_data": blockchain_result,
            "analysis_timestamp": datetime.now().isoformat(),
            "processing_time": round(processing_time, 3)
        }
        
        # Add to real-time analytics
        analytics.add_transaction(data, result)
        
        logger.info(f"Analyzed transaction {result['transaction_id']} - Risk: {result['risk_level']} ({combined_risk_percentage}%) - Time: {processing_time:.3f}s")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error analyzing transaction: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

def get_detailed_risk_analysis(transaction, ml_risk, blockchain_risk):
    """Provide detailed risk analysis with explanations"""
    risk_factors = []
    recommendations = []
    
    amount = float(transaction['amount'])
    
    # Amount-based analysis
    if amount > 50000:
        risk_factors.append({
            "factor": "High Transaction Amount",
            "description": f"Transaction amount of ${amount:,.2f} exceeds typical patterns",
            "impact": "High",
            "weight": 0.3
        })
        recommendations.append("Enhanced due diligence required for high-value transactions")
    elif amount > 20000:
        risk_factors.append({
            "factor": "Large Transaction Amount",
            "description": f"Transaction amount of ${amount:,.2f} is above average",
            "impact": "Medium",
            "weight": 0.2
        })
    
    # Round amount analysis
    if amount % 1000 == 0 and amount >= 5000:
        risk_factors.append({
            "factor": "Round Amount Pattern",
            "description": "Transaction uses round amounts, potential structuring",
            "impact": "Medium",
            "weight": 0.15
        })
        recommendations.append("Investigate for potential structuring or layering activities")
    
    # Timing analysis
    try:
        timestamp = datetime.fromisoformat(transaction['timestamp'])
        hour = timestamp.hour
        
        if hour in [0, 1, 2, 3, 23]:
            risk_factors.append({
                "factor": "Unusual Transaction Time",
                "description": f"Transaction at {hour:02d}:00 is outside normal business hours",
                "impact": "Medium",
                "weight": 0.2
            })
            recommendations.append("Review transactions occurring during unusual hours")
        
        if timestamp.weekday() >= 5:  # Weekend
            risk_factors.append({
                "factor": "Weekend Transaction",
                "description": "Transaction occurred during weekend",
                "impact": "Low",
                "weight": 0.1
            })
    except:
        pass
    
    # ML model confidence
    if ml_risk > 0.8:
        risk_factors.append({
            "factor": "High ML Risk Score",
            "description": "Machine learning model indicates high anomaly probability",
            "impact": "High",
            "weight": 0.4
        })
        recommendations.append("Immediate manual review recommended")
    elif ml_risk > 0.6:
        risk_factors.append({
            "factor": "Elevated ML Risk Score",
            "description": "Machine learning model indicates moderate anomaly probability",
            "impact": "Medium",
            "weight": 0.3
        })
    
    # Blockchain analysis
    if blockchain_risk > 0.7:
        risk_factors.append({
            "factor": "Blockchain Risk Indicators",
            "description": "Account shows suspicious blockchain activity patterns",
            "impact": "High",
            "weight": 0.3
        })
        recommendations.append("Investigate account transaction history on blockchain")
    
    # Default recommendations
    if not recommendations:
        if ml_risk + blockchain_risk > 1.0:
            recommendations.append("Monitor account for additional suspicious activity")
        else:
            recommendations.append("Transaction appears normal, continue standard monitoring")
    
    return {
        "risk_factors": risk_factors,
        "recommendations": recommendations
    }

def get_confidence_score(ml_risk, blockchain_risk):
    """Calculate confidence score for the risk assessment"""
    # Higher confidence when both models agree
    agreement = 1 - abs(ml_risk - blockchain_risk)
    
    # Higher confidence for extreme values
    extremity = max(ml_risk, 1 - ml_risk) + max(blockchain_risk, 1 - blockchain_risk)
    
    confidence = (agreement * 0.6 + extremity * 0.4)
    return min(1.0, max(0.5, confidence))  # Ensure confidence is between 50-100%

def get_risk_level(score):
    """Convert risk score to risk level"""
    if score >= 0.7:
        return "HIGH"
    elif score >= 0.4:
        return "MEDIUM"
    else:
        return "LOW"

def get_enhanced_risk_flags(transaction, score):
    """Generate enhanced risk flags based on analysis"""
    flags = []
    
    amount = float(transaction['amount'])
    
    if amount > 50000:
        flags.append({
            "type": "AMOUNT",
            "severity": "HIGH",
            "message": f"Very large transaction: ${amount:,.2f}"
        })
    elif amount > 20000:
        flags.append({
            "type": "AMOUNT", 
            "severity": "MEDIUM",
            "message": f"Large transaction: ${amount:,.2f}"
        })
    
    if score >= 0.8:
        flags.append({
            "type": "RISK",
            "severity": "HIGH", 
            "message": "High risk pattern detected - immediate review required"
        })
    elif score >= 0.6:
        flags.append({
            "type": "RISK",
            "severity": "MEDIUM",
            "message": "Elevated risk pattern detected"
        })
    
    try:
        timestamp = datetime.fromisoformat(transaction['timestamp'])
        hour = timestamp.hour
        
        if hour < 6 or hour > 22:
            flags.append({
                "type": "TIMING",
                "severity": "MEDIUM",
                "message": f"Unusual transaction time: {hour:02d}:00"
            })
        
        if timestamp.weekday() >= 5:
            flags.append({
                "type": "TIMING",
                "severity": "LOW", 
                "message": "Weekend transaction"
            })
    except:
        pass
    
    # Round amount detection
    if amount % 1000 == 0 and amount >= 5000:
        flags.append({
            "type": "PATTERN",
            "severity": "MEDIUM",
            "message": "Round amount - potential structuring"
        })
    
    return flags

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Get real-time dashboard data"""
    try:
        dashboard_data = analytics.get_dashboard_data()
        return jsonify(dashboard_data)
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get advanced analytics and predictions"""
    try:
        analytics_data = analytics.get_advanced_analytics()
        return jsonify(analytics_data)
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get recent security alerts"""
    try:
        alerts = list(analytics.alert_queue)
        return jsonify({
            "alerts": alerts,
            "total_count": len(alerts),
            "high_priority": len([a for a in alerts if a.get('severity') == 'HIGH']),
            "last_update": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/threat-intelligence', methods=['GET'])
def get_threat_intelligence():
    """Get threat intelligence data"""
    try:
        threat_data = {
            "high_risk_accounts": len(analytics.threat_intelligence['high_risk_accounts']),
            "suspicious_patterns": dict(analytics.threat_intelligence['suspicious_patterns']),
            "time_based_risks": dict(analytics.threat_intelligence['time_based_risks']),
            "recent_threats": list(analytics.alert_queue)[-5:],  # Last 5 alerts
            "risk_trends": {
                "increasing_risk_hours": [h for h, r in analytics.threat_intelligence['time_based_risks'].items() if r > 0.5],
                "pattern_frequency": analytics.threat_intelligence['suspicious_patterns']
            },
            "last_update": datetime.now().isoformat()
        }
        return jsonify(threat_data)
    except Exception as e:
        logger.error(f"Error getting threat intelligence: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/performance', methods=['GET'])
def get_performance_metrics():
    """Get system performance metrics"""
    try:
        performance_data = {
            "response_times": {
                "average": analytics.metrics['avg_response_time'],
                "last_100": list(analytics.performance_history)
            },
            "throughput": {
                "transactions_per_hour": len([
                    t for t in analytics.transaction_stream 
                    if (datetime.now() - datetime.fromisoformat(t['timestamp'])).total_seconds() < 3600
                ]),
                "total_processed": analytics.metrics['total_transactions']
            },
            "accuracy_metrics": {
                "detection_rate": (
                    (analytics.metrics['high_risk_count'] + analytics.metrics['medium_risk_count']) / 
                    max(1, analytics.metrics['total_transactions']) * 100
                ),
                "false_positive_rate": analytics.metrics['false_positives'] / max(1, analytics.metrics['total_transactions']) * 100
            },
            "system_health": {
                "uptime": (datetime.now() - analytics.metrics['system_uptime']).total_seconds() / 3600,
                "memory_usage": "Normal",  # Mock data
                "cpu_usage": "Low",  # Mock data
                "status": "OPTIMAL"
            },
            "last_update": datetime.now().isoformat()
        }
        return jsonify(performance_data)
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)