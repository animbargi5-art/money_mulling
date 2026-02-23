#!/usr/bin/env python3
"""
AlgoGuard Deployment Script
Automates the deployment process for RIFT competition submission
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a shell command and return the result"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return None

def check_prerequisites():
    """Check if all required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    # Check Python
    result = run_command("python --version", check=False)
    if not result:
        print("❌ Python not found")
        return False
    print("✅ Python found")
    
    # Check AlgoKit
    result = run_command("algokit --version", check=False)
    if not result:
        print("❌ AlgoKit not found. Install with: pip install algokit")
        return False
    print("✅ AlgoKit found")
    
    # Check Node.js (for frontend)
    result = run_command("node --version", check=False)
    if not result:
        print("⚠️  Node.js not found. Frontend deployment will be skipped.")
    else:
        print("✅ Node.js found")
    
    return True

def setup_backend():
    """Set up the backend environment"""
    print("\n🐍 Setting up backend...")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt"):
        print("❌ Failed to install Python dependencies")
        return False
    
    print("✅ Backend setup complete")
    return True

def build_smart_contracts():
    """Build the smart contracts"""
    print("\n📜 Building smart contracts...")
    
    contract_dir = Path("d/projects/d")
    if not contract_dir.exists():
        print("❌ Smart contract directory not found")
        return False
    
    # Build contracts
    if not run_command("python -m smart_contracts build", cwd=contract_dir):
        print("❌ Failed to build smart contracts")
        return False
    
    print("✅ Smart contracts built successfully")
    return True

def test_system():
    """Run basic system tests"""
    print("\n🧪 Running system tests...")
    
    # Test ML detector
    try:
        from ml_detector import detector
        test_transaction = {
            'amount': 1000,
            'timestamp': '2024-01-01T12:00:00',
            'sender_account': 'test_sender',
            'receiver_account': 'test_receiver'
        }
        risk_score = detector.predict_risk(test_transaction)
        print(f"✅ ML detector test passed (risk score: {risk_score})")
    except Exception as e:
        print(f"❌ ML detector test failed: {e}")
        return False
    
    # Test Algorand integration
    try:
        from algorand_integration import algorand_client
        status = algorand_client.get_network_status()
        if status.get('connected'):
            print("✅ Algorand connection test passed")
        else:
            print("⚠️  Algorand connection test failed (network may be down)")
    except Exception as e:
        print(f"❌ Algorand integration test failed: {e}")
        return False
    
    return True

def deploy_to_testnet():
    """Deploy smart contracts to Algorand Testnet"""
    print("\n🚀 Deploying to Algorand Testnet...")
    
    contract_dir = Path("d/projects/d")
    env_file = contract_dir / ".env"
    
    if not env_file.exists():
        print("⚠️  .env file not found. Please configure your testnet credentials.")
        print("   Copy .env.example to .env and add your DEPLOYER_MNEMONIC")
        return False
    
    # Deploy contracts
    if not run_command("python -m smart_contracts deploy", cwd=contract_dir):
        print("❌ Failed to deploy to testnet")
        return False
    
    print("✅ Deployment to testnet complete!")
    print("📝 Check the output above for your App ID")
    return True

def generate_submission_info():
    """Generate information needed for RIFT submission"""
    print("\n📋 Generating RIFT submission information...")
    
    info = {
        "project_name": "AlgoGuard",
        "description": "Blockchain Money Muling Detection System",
        "tech_stack": "AlgoKit, Algorand Python, Flask, React.js, scikit-learn",
        "github_repo": "https://github.com/YOUR_USERNAME/algoguard-rift-submission",
        "live_demo": "To be deployed",
        "app_id": "Check deployment output above",
        "video_demo": "To be created on LinkedIn"
    }
    
    print("\n" + "="*50)
    print("🏆 RIFT SUBMISSION INFORMATION")
    print("="*50)
    for key, value in info.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    print("="*50)
    
    # Save to file
    with open("RIFT_SUBMISSION_INFO.txt", "w") as f:
        f.write("RIFT COMPETITION SUBMISSION - ALGOGUARD\n")
        f.write("="*50 + "\n\n")
        for key, value in info.items():
            f.write(f"{key.replace('_', ' ').title()}: {value}\n")
        f.write("\nGenerated by deploy.py script\n")
    
    print("📄 Submission info saved to RIFT_SUBMISSION_INFO.txt")

def main():
    """Main deployment function"""
    print("🚀 AlgoGuard Deployment Script")
    print("="*40)
    
    # Check prerequisites
    if not check_prerequisites():
        print("❌ Prerequisites check failed")
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed")
        sys.exit(1)
    
    # Build smart contracts
    if not build_smart_contracts():
        print("❌ Smart contract build failed")
        sys.exit(1)
    
    # Test system
    if not test_system():
        print("❌ System tests failed")
        sys.exit(1)
    
    # Ask about testnet deployment
    deploy_testnet = input("\n🤔 Deploy to Algorand Testnet? (y/N): ").lower().strip()
    if deploy_testnet == 'y':
        deploy_to_testnet()
    
    # Generate submission info
    generate_submission_info()
    
    print("\n🎉 Deployment script completed!")
    print("📋 Next steps:")
    print("   1. Create GitHub repository (see GITHUB_SETUP.md)")
    print("   2. Deploy frontend for live demo")
    print("   3. Create LinkedIn demonstration video")
    print("   4. Submit to RIFT competition")

if __name__ == "__main__":
    main()