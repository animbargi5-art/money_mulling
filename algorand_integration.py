"""
Algorand blockchain integration for AlgoGuard
"""
import os
import logging
from typing import Optional, Dict, Any
from algosdk import account, mnemonic
from algosdk.v2client import algod, indexer
import algokit_utils

logger = logging.getLogger(__name__)

class AlgorandClient:
    def __init__(self):
        """Initialize Algorand client for Testnet"""
        self.algod_address = "https://testnet-api.algonode.cloud"
        self.algod_token = ""
        self.indexer_address = "https://testnet-idx.algonode.cloud"
        self.indexer_token = ""
        
        # Initialize clients
        self.algod_client = algod.AlgodClient(self.algod_token, self.algod_address)
        self.indexer_client = indexer.IndexerClient(self.indexer_token, self.indexer_address)
        
        # Contract configuration (will be set after deployment)
        self.app_id = None
        self.app_address = None
        
    def create_account(self) -> Dict[str, str]:
        """Create a new Algorand account"""
        try:
            private_key, address = account.generate_account()
            mnemonic_phrase = mnemonic.from_private_key(private_key)
            
            return {
                "address": address,
                "private_key": private_key,
                "mnemonic": mnemonic_phrase
            }
        except Exception as e:
            logger.error(f"Error creating account: {e}")
            return None
    
    def get_account_info(self, address: str) -> Optional[Dict[str, Any]]:
        """Get account information from Algorand"""
        try:
            account_info = self.algod_client.account_info(address)
            return {
                "address": address,
                "balance": account_info.get("amount", 0),
                "min_balance": account_info.get("min-balance", 0),
                "created_at_round": account_info.get("created-at-round", 0),
                "apps_total_schema": account_info.get("apps-total-schema", {}),
                "assets": account_info.get("assets", [])
            }
        except Exception as e:
            logger.error(f"Error getting account info for {address}: {e}")
            return None
    
    def calculate_blockchain_risk(self, address: str) -> int:
        """Calculate risk score based on blockchain activity"""
        try:
            account_info = self.get_account_info(address)
            if not account_info:
                return 50  # Default medium risk
            
            balance = account_info["balance"]
            created_round = account_info["created_at_round"]
            
            # Get current round for age calculation
            status = self.algod_client.status()
            current_round = status["last-round"]
            account_age = current_round - created_round
            
            # Risk calculation logic
            risk_score = 50  # Base risk
            
            # Lower risk for older accounts
            if account_age > 100000:  # Very old account
                risk_score -= 20
            elif account_age > 50000:  # Moderately old account
                risk_score -= 10
            
            # Lower risk for higher balance accounts
            if balance > 10000000:  # > 10 ALGO
                risk_score -= 15
            elif balance > 1000000:  # > 1 ALGO
                risk_score -= 10
            
            # Higher risk for very new accounts with high activity
            if account_age < 1000 and balance > 5000000:  # New account with > 5 ALGO
                risk_score += 20
            
            # Ensure risk score is within bounds
            risk_score = max(0, min(100, risk_score))
            
            return risk_score
            
        except Exception as e:
            logger.error(f"Error calculating blockchain risk for {address}: {e}")
            return 50  # Default medium risk
    
    def submit_to_blockchain(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit risk assessment to AlgoGuard smart contract"""
        try:
            # For now, return a mock response
            # In production, this would interact with the deployed smart contract
            
            blockchain_risk = self.calculate_blockchain_risk(
                transaction_data.get("sender_account", "")
            )
            
            return {
                "blockchain_submitted": True,
                "blockchain_risk_score": blockchain_risk,
                "transaction_hash": "mock_txn_hash_" + str(hash(str(transaction_data))),
                "app_id": self.app_id or "not_deployed",
                "timestamp": transaction_data.get("timestamp")
            }
            
        except Exception as e:
            logger.error(f"Error submitting to blockchain: {e}")
            return {
                "blockchain_submitted": False,
                "error": str(e)
            }
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get Algorand network status"""
        try:
            status = self.algod_client.status()
            return {
                "network": "testnet",
                "last_round": status["last-round"],
                "time_since_last_round": status["time-since-last-round"],
                "catchup_time": status["catchup-time"],
                "connected": True
            }
        except Exception as e:
            logger.error(f"Error getting network status: {e}")
            return {
                "network": "testnet",
                "connected": False,
                "error": str(e)
            }

# Global instance
algorand_client = AlgorandClient()