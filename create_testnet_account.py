#!/usr/bin/env python3
"""
Create a testnet account for AlgoGuard deployment
"""

from algorand_integration import algorand_client
import os

def create_and_configure_testnet_account():
    """Create testnet account and update environment"""
    print("🔑 Creating testnet account for AlgoGuard deployment...")
    
    # Create a new testnet account
    account = algorand_client.create_account()
    if not account:
        print("❌ Failed to create testnet account")
        return False
    
    print("\n=== TESTNET ACCOUNT CREATED ===")
    print(f"Address: {account['address']}")
    print(f"Mnemonic: {account['mnemonic']}")
    print("================================")
    
    # Update .env file
    env_path = 'd/projects/d/.env'
    try:
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Replace the placeholder mnemonic
        updated_content = content.replace('your_testnet_mnemonic_here', account['mnemonic'])
        
        with open(env_path, 'w') as f:
            f.write(updated_content)
        
        print("✅ Environment file updated with testnet account")
        print(f"\n⚠️  IMPORTANT: Fund this account with testnet ALGOs")
        print(f"🔗 Testnet Dispenser: https://testnet.algoexplorer.io/dispenser")
        print(f"📋 Account to fund: {account['address']}")
        print(f"\n💡 You need at least 0.1 ALGO for deployment")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to update environment file: {e}")
        return False

if __name__ == "__main__":
    create_and_configure_testnet_account()