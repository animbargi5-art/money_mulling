from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime
import logging
from ml_detector import detector
from algorand_integration import algorand_client

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
    try:
        data = request.get_json()
        
        # Basic validation
        required_fields = ['amount', 'sender_account', 'receiver_account', 'timestamp']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        # ML-based risk scoring
        ml_risk_score = detector.predict_risk(data)
        
        # Blockchain-based risk scoring
        blockchain_risk_score = algorand_client.calculate_blockchain_risk(
            data.get('sender_account', '')
        )
        
        # Combined risk score (weighted average)
        combined_risk_score = int((ml_risk_score * 0.7) + (blockchain_risk_score * 0.3))
        
        # Submit to blockchain (mock for now)
        blockchain_result = algorand_client.submit_to_blockchain(data)
        
        result = {
            "transaction_id": data.get('transaction_id', 'unknown'),
            "risk_score": combined_risk_score,
            "ml_risk_score": ml_risk_score,
            "blockchain_risk_score": blockchain_risk_score,
            "risk_level": get_risk_level(combined_risk_score),
            "flags": get_risk_flags(data, combined_risk_score),
            "blockchain_data": blockchain_result
        }
        
        logger.info(f"Analyzed transaction {result['transaction_id']} - Risk: {result['risk_level']}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error analyzing transaction: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

def get_risk_level(score):
    """Convert risk score to risk level"""
    if score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"

def get_risk_flags(transaction, score):
    """Generate risk flags based on analysis"""
    flags = []
    
    if float(transaction['amount']) > 10000:
        flags.append("Large amount transaction")
    
    if score >= 70:
        flags.append("High risk pattern detected")
    
    try:
        hour = datetime.fromisoformat(transaction['timestamp']).hour
        if hour < 6 or hour > 22:
            flags.append("Unusual transaction time")
    except:
        pass
    
    return flags

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)