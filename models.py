"""
Data models for money muling detection
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Transaction:
    transaction_id: str
    amount: float
    sender_account: str
    receiver_account: str
    timestamp: datetime
    currency: str = "USD"
    description: Optional[str] = None

@dataclass
class RiskAnalysis:
    transaction_id: str
    risk_score: float
    risk_level: str
    flags: List[str]
    analysis_timestamp: datetime
    
    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "flags": self.flags,
            "analysis_timestamp": self.analysis_timestamp.isoformat()
        }

@dataclass
class Account:
    account_id: str
    account_type: str
    creation_date: datetime
    transaction_count: int = 0
    total_volume: float = 0.0
    risk_score: float = 0.0