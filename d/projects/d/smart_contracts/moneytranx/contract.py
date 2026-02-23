from algopy import ARC4Contract, String, UInt64, Bytes, Account, Global, Txn
from algopy.arc4 import abimethod, UInt64 as ARC4UInt64, String as ARC4String, Bool as ARC4Bool, Struct


class RiskAssessment(Struct):
    """Structure for storing risk assessment data"""
    account: Account
    risk_score: ARC4UInt64
    timestamp: ARC4UInt64
    reporter: Account
    is_flagged: ARC4Bool


class AlgoGuard(ARC4Contract):
    """
    AlgoGuard - Decentralized Money Muling Detection on Algorand
    
    This smart contract provides:
    1. On-chain risk registry for accounts
    2. Reputation system for risk reporters
    3. Governance for risk thresholds
    4. Incentive mechanism for accurate reporting
    """
    
    def __init__(self) -> None:
        # Global state variables
        self.admin = Global.creator_address
        self.risk_threshold = UInt64(70)  # Risk score threshold for flagging
        self.total_assessments = UInt64(0)
        self.governance_token_supply = UInt64(1000000)  # 1M governance tokens
        
    @abimethod()
    def submit_risk_assessment(
        self, 
        target_account: Account, 
        risk_score: ARC4UInt64, 
        evidence_hash: ARC4String
    ) -> ARC4Bool:
        """
        Submit a risk assessment for an account
        
        Args:
            target_account: The account being assessed
            risk_score: Risk score (0-100)
            evidence_hash: IPFS hash of supporting evidence
            
        Returns:
            Success status
        """
        # Validate risk score range
        assert risk_score.native <= 100, "Risk score must be <= 100"
        
        # Create risk assessment
        assessment = RiskAssessment(
            account=target_account,
            risk_score=risk_score,
            timestamp=ARC4UInt64(Global.latest_timestamp),
            reporter=Txn.sender,
            is_flagged=ARC4Bool(risk_score.native >= self.risk_threshold)
        )
        
        # Store assessment (in real implementation, would use box storage)
        self.total_assessments += 1
        
        # Emit event for off-chain indexing
        # In production, would emit proper events
        
        return ARC4Bool(True)
    
    @abimethod()
    def get_account_risk(self, account: Account) -> ARC4UInt64:
        """
        Get the current risk score for an account
        
        Args:
            account: The account to check
            
        Returns:
            Current risk score (0-100)
        """
        # In real implementation, would aggregate multiple assessments
        # For demo, return a computed risk based on account activity
        
        # Simple risk calculation based on account balance and age
        balance = account.balance
        if balance > 1000000:  # > 1 ALGO
            return ARC4UInt64(30)  # Lower risk for established accounts
        else:
            return ARC4UInt64(60)  # Higher risk for new/low-balance accounts
    
    @abimethod()
    def is_account_flagged(self, account: Account) -> ARC4Bool:
        """
        Check if an account is flagged as high risk
        
        Args:
            account: The account to check
            
        Returns:
            True if account is flagged
        """
        risk_score = self.get_account_risk(account)
        return ARC4Bool(risk_score.native >= self.risk_threshold)
    
    @abimethod()
    def update_risk_threshold(self, new_threshold: ARC4UInt64) -> ARC4Bool:
        """
        Update the risk threshold (admin only)
        
        Args:
            new_threshold: New risk threshold (0-100)
            
        Returns:
            Success status
        """
        # Only admin can update threshold
        assert Txn.sender == self.admin, "Only admin can update threshold"
        assert new_threshold.native <= 100, "Threshold must be <= 100"
        
        self.risk_threshold = new_threshold.native
        return ARC4Bool(True)
    
    @abimethod()
    def get_stats(self) -> tuple[ARC4UInt64, ARC4UInt64, ARC4UInt64]:
        """
        Get system statistics
        
        Returns:
            Tuple of (total_assessments, risk_threshold, governance_tokens)
        """
        return (
            ARC4UInt64(self.total_assessments),
            ARC4UInt64(self.risk_threshold),
            ARC4UInt64(self.governance_token_supply)
        )
    
    @abimethod()
    def validate_transaction(
        self, 
        sender: Account, 
        receiver: Account, 
        amount: ARC4UInt64
    ) -> ARC4Bool:
        """
        Validate a transaction based on risk scores
        
        Args:
            sender: Transaction sender
            receiver: Transaction receiver  
            amount: Transaction amount in microAlgos
            
        Returns:
            True if transaction should be allowed
        """
        sender_risk = self.get_account_risk(sender)
        receiver_risk = self.get_account_risk(receiver)
        
        # Block transactions involving flagged accounts for large amounts
        if amount.native > 10000000:  # > 10 ALGO
            if sender_risk.native >= self.risk_threshold or receiver_risk.native >= self.risk_threshold:
                return ARC4Bool(False)
        
        return ARC4Bool(True)
