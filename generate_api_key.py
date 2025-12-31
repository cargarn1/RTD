#!/usr/bin/env python3
"""
API Key Generator
Quick tool to generate secure API keys for your RTD API server
"""

import secrets
import sys

def generate_key(length=32):
    """Generate a cryptographically secure API key"""
    return secrets.token_urlsafe(length)

def main():
    print("\n" + "="*80)
    print("🔑 RTD API Key Generator")
    print("="*80)
    print("\nGenerating secure API keys...\n")
    
    # Generate multiple keys
    print("Generated API Keys (store these securely!):\n")
    
    for i in range(1, 4):
        key = generate_key()
        print(f"{i}. {key}")
    
    print("\n" + "-"*80)
    print("\n📋 How to use these keys:\n")
    print("1. Copy one of the keys above")
    print("2. Edit api_server.py and add to API_KEYS dictionary:")
    print("\n   API_KEYS = {")
    print(f"       '{generate_key()}': {{")
    print("           'name': 'Zapier Integration',")
    print("           'permissions': ['read']")
    print("       }")
    print("   }")
    print("\n3. Or set as environment variable:")
    print("   export RTD_API_KEY='your-key-here'")
    print("\n4. Give the key to Zapier in the X-API-Key header")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()

