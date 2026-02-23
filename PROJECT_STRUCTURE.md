# AlgoGuard Project Structure

## Overview
This repository contains the complete AlgoGuard system - a blockchain-based money muling detection platform built for the RIFT Algorand competition.

## Directory Structure

```
algoguard/
├── README.md                          # Main project documentation
├── PROJECT_STRUCTURE.md              # This file
├── .gitignore                         # Git ignore rules
├── requirements.txt                   # Python dependencies
├── app.py                            # Main Flask application
├── ml_detector.py                    # Machine learning detection engine
├── algorand_integration.py           # Algorand blockchain integration
├── models.py                         # Data models
├── d/projects/d/                     # AlgoKit smart contract project
│   ├── smart_contracts/
│   │   └── moneytranx/
│   │       ├── contract.py           # AlgoGuard smart contract
│   │       └── deploy_config.py      # Deployment configuration
│   ├── tests/                        # Smart contract tests
│   ├── pyproject.toml               # Poetry configuration
│   └── .env                         # Environment variables
└── ../frontend/                      # React frontend (separate workspace)
    ├── src/
    │   ├── App.js                   # Main React application
    │   └── App.css                  # Styling
    ├── public/                      # Static assets
    └── package.json                 # Node.js dependencies
```

## Key Components

### Backend (Python Flask)
- **app.py**: Main API server with endpoints for transaction analysis
- **ml_detector.py**: Machine learning models for risk assessment
- **algorand_integration.py**: Blockchain interaction layer

### Smart Contracts (Algorand Python)
- **contract.py**: AlgoGuard smart contract with risk registry and governance
- **deploy_config.py**: Deployment and testing configuration

### Frontend (React.js)
- **App.js**: User interface with transaction analysis and blockchain integration
- Ant Design components for professional UI

## Technology Stack

### Blockchain
- **Algorand**: Layer 1 blockchain platform
- **AlgoKit**: Development framework
- **Algorand Python**: Smart contract language

### Backend
- **Python 3.9+**: Core language
- **Flask**: Web framework
- **scikit-learn**: Machine learning
- **py-algorand-sdk**: Blockchain integration

### Frontend
- **React.js**: UI framework
- **Ant Design**: Component library
- **Recharts**: Data visualization
- **Axios**: HTTP client

## Getting Started

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd algoguard
   ```

2. **Backend Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Smart Contract Setup**
   ```bash
   cd d/projects/d
   poetry install
   python -m smart_contracts build
   ```

4. **Frontend Setup** (in separate terminal)
   ```bash
   cd ../frontend
   npm install
   npm start
   ```

5. **Run Backend**
   ```bash
   python app.py
   ```

## RIFT Competition Requirements

### ✅ Completed
- [x] AlgoKit framework usage
- [x] Algorand Python smart contracts
- [x] Meaningful blockchain integration
- [x] Complete source code
- [x] Professional documentation

### 🔄 In Progress
- [ ] Testnet deployment
- [ ] Live demo URL
- [ ] LinkedIn demonstration video

## Features Implemented

### Core Functionality
1. **ML-Based Risk Detection**: Real-time transaction analysis
2. **Blockchain Integration**: Account risk assessment using on-chain data
3. **Smart Contract Registry**: Decentralized risk storage
4. **Governance System**: Token-based threshold management
5. **Web Interface**: Professional React dashboard

### Smart Contract Features
- Risk assessment submission
- Account flagging system
- Governance token distribution
- Transparent audit trails
- Community-driven reporting

## Next Steps

1. **Deploy to Testnet**: Get App ID for submission
2. **Create Demo Video**: LinkedIn demonstration
3. **Deploy Frontend**: Public URL for live demo
4. **Final Testing**: End-to-end system validation

## Contact

Built for the RIFT Algorand Competition 2026
- **GitHub**: This repository
- **Demo**: [Coming Soon]
- **Video**: [LinkedIn - Coming Soon]