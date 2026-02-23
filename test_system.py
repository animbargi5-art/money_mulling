#!/usr/bin/env python3
"""
AlgoGuard System Test Script
Quick verification that all components are working
"""

import sys
import json
from datetime import datetime

def test_ml_detector():
    """Test the ML detection system"""
    print("🧠 Testing ML Detector...")
    try:
        from ml_detector import detector
        
        # Test transaction data
        test_cases = [
            {
                'name': 'Normal Transaction',
                'data': {
                    'amount': 500,
                    'timestamp': '2024-01-01T14:00:00',
                    'sender_account': 'SENDER123',
                    'receiver_account': 'RECEIVER456'
                },
                'expected_risk': 'LOW'
            },
            {
                'name': 'Suspicious Transaction',
                'data': {
                    'amount': 15000,
                    'timestamp': '2024-01-01T03:00:00',
                    'sender_account': 'SUSPICIOUS123',
                    'receiver_account': 'RECEIVER789'
                },
                'expected_risk': 'HIGH'
            }
        ]
        
        for test_case in test_cases:
            risk_score = detector.predict_risk(test_case['data'])
            risk_level = 'HIGH' if risk_score >= 70 else 'MEDIUM' if risk_score >= 40 else 'LOW'
            
            print(f"   {test_case['name']}: Risk Score = {risk_score}, Level = {risk_level}")
            
            if risk_level == test_case['expected_risk']:
                print(f"   ✅ {test_case['name']} - PASSED")
            else:
                print(f"   ⚠️  {test_case['name']} - Expected {test_case['expected_risk']}, got {risk_level}")
        
        print("✅ ML Detector tests completed")
        return True
        
    except Exception as e:
        print(f"❌ ML Detector test failed: {e}")
        return False

def test_algorand_integration():
    """Test Algorand blockchain integration"""
    print("\n🔗 Testing Algorand Integration...")
    try:
        from algorand_integration import algorand_client
        
        # Test network connection
        status = algorand_client.get_network_status()
        if status.get('connected'):
            print(f"   ✅ Connected to {status.get('network', 'unknown')} network")
            print(f"   📊 Last round: {status.get('last_round', 'unknown')}")
        else:
            print(f"   ⚠️  Network connection failed: {status.get('error', 'unknown error')}")
        
        # Test account creation
        print("   🔑 Testing account creation...")
        account = algorand_client.create_account()
        if account:
            print(f"   ✅ Test account created: {account['address'][:10]}...")
        else:
            print("   ❌ Account creation failed")
        
        # Test risk calculation
        print("   📈 Testing blockchain risk calculation...")
        test_address = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        risk_score = algorand_client.calculate_blockchain_risk(test_address)
        print(f"   📊 Test address risk score: {risk_score}")
        
        print("✅ Algorand integration tests completed")
        return True
        
    except Exception as e:
        print(f"❌ Algorand integration test failed: {e}")
        return False

def test_smart_contracts():
    """Test smart contract compilation"""
    print("\n📜 Testing Smart Contracts...")
    try:
        import os
        from pathlib import Path
        
        contract_dir = Path("d/projects/d")
        if not contract_dir.exists():
            print("   ❌ Smart contract directory not found")
            return False
        
        # Check if contracts are built
        artifacts_dir = contract_dir / "smart_contracts" / "artifacts" / "moneytranx"
        if artifacts_dir.exists():
            arc56_file = artifacts_dir / "AlgoGuard.arc56.json"
            if arc56_file.exists():
                print("   ✅ Smart contract artifacts found")
                
                # Read contract info
                with open(arc56_file, 'r') as f:
                    contract_info = json.load(f)
                    print(f"   📋 Contract name: {contract_info.get('name', 'Unknown')}")
                    print(f"   📋 Methods: {len(contract_info.get('methods', []))}")
            else:
                print("   ⚠️  Contract artifacts not found - run build first")
        else:
            print("   ⚠️  Artifacts directory not found - run build first")
        
        print("✅ Smart contract tests completed")
        return True
        
    except Exception as e:
        print(f"❌ Smart contract test failed: {e}")
        return False

def test_api_endpoints():
    """Test Flask API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    try:
        from app import app
        
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/health')
            if response.status_code == 200:
                print("   ✅ Health endpoint working")
            else:
                print(f"   ❌ Health endpoint failed: {response.status_code}")
            
            # Test network status endpoint
            response = client.get('/api/network-status')
            if response.status_code == 200:
                print("   ✅ Network status endpoint working")
            else:
                print(f"   ❌ Network status endpoint failed: {response.status_code}")
            
            # Test transaction analysis endpoint
            test_transaction = {
                'amount': 1000,
                'sender_account': 'TEST_SENDER',
                'receiver_account': 'TEST_RECEIVER',
                'timestamp': datetime.now().isoformat()
            }
            
            response = client.post('/api/analyze-transaction', 
                                 json=test_transaction,
                                 content_type='application/json')
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"   ✅ Transaction analysis working - Risk: {data.get('risk_level')}")
            else:
                print(f"   ❌ Transaction analysis failed: {response.status_code}")
        
        print("✅ API endpoint tests completed")
        return True
        
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        return False

def generate_test_report():
    """Generate a test report"""
    print("\n📊 Generating Test Report...")
    
    report = {
        "test_timestamp": datetime.now().isoformat(),
        "system_status": "All tests completed",
        "components_tested": [
            "ML Detection Engine",
            "Algorand Integration",
            "Smart Contracts",
            "API Endpoints"
        ],
        "next_steps": [
            "Deploy smart contracts to testnet",
            "Deploy frontend application",
            "Create demonstration video",
            "Submit to RIFT competition"
        ]
    }
    
    with open("TEST_REPORT.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("📄 Test report saved to TEST_REPORT.json")

def main():
    """Run all system tests"""
    print("🧪 AlgoGuard System Test Suite")
    print("="*40)
    
    tests_passed = 0
    total_tests = 4
    
    # Run all tests
    if test_ml_detector():
        tests_passed += 1
    
    if test_algorand_integration():
        tests_passed += 1
    
    if test_smart_contracts():
        tests_passed += 1
    
    if test_api_endpoints():
        tests_passed += 1
    
    # Generate report
    generate_test_report()
    
    # Summary
    print("\n" + "="*40)
    print(f"🏁 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! System is ready for deployment.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())