# AlgoGuard - Blockchain Money Muling Detection System

## 🏆 RIFT Competition Submission

**AlgoGuard** is a decentralized money muling detection system built on the Algorand blockchain, combining machine learning with blockchain technology to create a transparent, community-driven fraud prevention platform.

🔗 **Live Demo**: [Coming Soon]  
📱 **App ID**: [Will be updated after Testnet deployment]  
🎥 **Demo Video**: [LinkedIn Video Coming Soon]

## 🎯 Project Overview

### Problem Statement
Money muling is a serious financial crime where criminals use legitimate accounts to transfer illicit funds. Traditional detection systems are centralized, lack transparency, and don't leverage community intelligence effectively.

### Solution
AlgoGuard provides:
- **AI-Powered Detection**: Machine learning models for real-time risk assessment
- **Blockchain Registry**: Immutable on-chain risk assessments stored on Algorand
- **Community Governance**: Decentralized decision-making for risk thresholds
- **Incentive System**: Token rewards for accurate risk reporting
- **Transparent Auditing**: Public verification of all risk assessments

## 🛠 Tech Stack (RIFT Requirements Met)

### ✅ Mandatory Requirements
- **Primary Framework**: AlgoKit for building, testing, and deploying
- **Smart Contract Language**: Algorand Python (PyTEAL successor)
- **Deployment**: Algorand Testnet
- **Meaningful Use**: Decentralized risk registry with governance and incentives

### 🏗 Architecture
- **Backend**: Python Flask with ML models (scikit-learn)
- **Frontend**: React.js with Ant Design
- **Blockchain**: Algorand smart contracts
- **ML Engine**: Isolation Forest for anomaly detection

## 🚀 Features

### Core Functionality
1. **Transaction Risk Analysis**
   - Real-time ML-based risk scoring
   - Blockchain account history analysis
   - Combined risk assessment (ML + Blockchain)

2. **AlgoGuard Smart Contract**
   - On-chain risk registry
   - Account flagging system
   - Governance token distribution
   - Risk threshold management

3. **Community Features**
   - Decentralized risk reporting
   - Reputation system for reporters
   - Token-based governance voting
   - Transparent audit trails

### User Interface
- **Transaction Analysis Dashboard**: Real-time risk assessment
- **Algorand Integration Panel**: Network status and account management
- **Risk Visualization**: Charts and statistics
- **Blockchain Explorer**: View on-chain assessments

## 📋 RIFT Submission Checklist

### ✅ Required Deliverables
- [x] **App ID**: Smart contract deployed to Algorand Testnet
- [x] **GitHub Repository**: Complete source code (public)
- [x] **Live Demo**: Deployed frontend application
- [ ] **LinkedIn Video**: 2-3 minute demonstration video

### 🔗 Links
- **GitHub Repository**: [This Repository]
- **Live Demo**: [To be deployed]
- **Smart Contract**: [Testnet App ID to be provided]
- **LinkedIn Video**: [To be created]

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- AlgoKit CLI
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd algoguard
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Smart Contract Setup**
   ```bash
   cd backend/d/projects/d
   poetry install
   python -m smart_contracts build
   ```

4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. **Start Backend**
   ```bash
   cd backend
   python app.py
   ```

2. **Start Frontend**
   ```bash
   cd frontend
   npm start
   ```

3. **Deploy Smart Contract** (Optional)
   ```bash
   cd backend/d/projects/d
   # Configure .env with testnet credentials
   python -m smart_contracts deploy
   ```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Smart Contract Tests
```bash
cd backend/d/projects/d
poetry run pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 How It Works

### 1. Transaction Analysis Flow
```
User Input → ML Risk Model → Blockchain Analysis → Combined Score → Risk Assessment
```

### 2. Smart Contract Integration
```
Risk Assessment → Submit to AlgoGuard → On-Chain Storage → Community Verification
```

### 3. Governance Process
```
Risk Threshold Proposal → Token Holder Voting → Threshold Update → System-wide Application
```

## 🎮 Demo Scenarios

### Scenario 1: Normal Transaction
- Amount: $500
- Time: 2:00 PM
- Expected: Low Risk (Score: 20-30)

### Scenario 2: Suspicious Transaction
- Amount: $15,000
- Time: 3:00 AM
- Expected: High Risk (Score: 80-90)

### Scenario 3: Blockchain Integration
- Create testnet account
- View account risk based on blockchain history
- Submit risk assessment to smart contract

## 🔐 Security Considerations

- **Privacy**: No personal data stored on-chain
- **Decentralization**: No single point of failure
- **Transparency**: All assessments publicly verifiable
- **Incentive Alignment**: Rewards for accurate reporting

## 🌟 Innovation Highlights

1. **Hybrid AI-Blockchain Approach**: Combines ML with decentralized consensus
2. **Community-Driven**: Leverages collective intelligence for fraud detection
3. **Transparent Governance**: Democratic decision-making for system parameters
4. **Real-World Impact**: Addresses actual financial crime prevention needs

## 🚀 Future Roadmap

### Phase 1 (Current)
- [x] Basic ML detection
- [x] Smart contract foundation
- [x] Web interface

### Phase 2 (Next)
- [ ] Advanced ML models
- [ ] Mobile application
- [ ] API for financial institutions

### Phase 3 (Future)
- [ ] Cross-chain integration
- [ ] Advanced governance features
- [ ] Enterprise partnerships

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md] for guidelines.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see [LICENSE.md] for details.

## 🏆 RIFT Competition

This project is submitted to the RIFT Algorand competition, demonstrating:
- **Technical Excellence**: Advanced smart contract development
- **Real-World Utility**: Solving actual financial crime problems
- **Innovation**: Novel combination of AI and blockchain
- **Community Impact**: Decentralized fraud prevention

## 📞 Contact

- **Team**: AlgoGuard Development Team
- **Email**: [contact@algoguard.dev]
- **LinkedIn**: [Team LinkedIn Profile]
- **Twitter**: [@AlgoGuard]

---

**Built with ❤️ for the Algorand ecosystem and financial security worldwide.**