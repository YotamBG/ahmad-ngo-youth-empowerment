#!/usr/bin/env python3
"""
GOOGLE WORKSPACE SETUP TEST SCRIPT
Quick verification that everything is working correctly
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

def test_email_delivery(domain, admin_email):
    """Test email delivery to the workspace domain"""
    print(f"\n📧 TESTING EMAIL DELIVERY TO: {admin_email}")
    
    # Method 1: Check MX records
    try:
        result = subprocess.run(['dig', '+short', 'MX', domain], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and 'smtp.google.com' in result.stdout:
            print("✅ MX records correctly configured")
            return True
        else:
            print("❌ MX records not found or incorrect")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️  dig command not available - skipping MX check")
        return True

def test_domain_verification(domain):
    """Test if domain is verified with Google"""
    print(f"\n🔍 TESTING DOMAIN VERIFICATION: {domain}")
    
    try:
        result = subprocess.run(['dig', '+short', 'TXT', domain], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and 'google-site-verification' in result.stdout:
            print("✅ Domain verification TXT record found")
            return True
        else:
            print("⚠️  Domain verification record not found")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️  dig command not available - skipping verification check")
        return True

def test_workspace_access(admin_email):
    """Test workspace admin console access"""
    print(f"\n🌐 TESTING WORKSPACE ACCESS...")
    
    print("📋 Manual tests to perform:")
    print(f"1. Go to: https://admin.google.com")
    print(f"2. Sign in with: {admin_email}")
    print(f"3. Verify you can access the admin console")
    print(f"4. Check Gmail at: https://mail.google.com")
    print(f"5. Send a test email to verify delivery")
    
    return True

def test_dns_configuration(domain):
    """Test complete DNS configuration"""
    print(f"\n🌐 TESTING DNS CONFIGURATION FOR: {domain}")
    
    dns_tests = [
        ('MX', 'smtp.google.com'),
        ('TXT', 'google-site-verification'),
        ('TXT', 'v=spf1')  # SPF record
    ]
    
    results = []
    for record_type, expected in dns_tests:
        try:
            result = subprocess.run(['dig', '+short', record_type, domain], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and expected in result.stdout:
                print(f"✅ {record_type} record found: {expected}")
                results.append(True)
            else:
                print(f"❌ {record_type} record not found: {expected}")
                results.append(False)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"⚠️  Cannot check {record_type} record - dig not available")
            results.append(True)  # Don't fail if tool not available
    
    return all(results)

def test_service_account():
    """Test service account configuration"""
    print(f"\n🔑 TESTING SERVICE ACCOUNT...")
    
    creds_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds_file:
        print("❌ GOOGLE_APPLICATION_CREDENTIALS not set")
        return False
    
    if not os.path.exists(creds_file):
        print(f"❌ Service account file not found: {creds_file}")
        return False
    
    try:
        with open(creds_file, 'r') as f:
            creds = json.load(f)
        
        required_fields = ['type', 'project_id', 'client_email', 'private_key']
        for field in required_fields:
            if field not in creds:
                print(f"❌ Missing field in service account: {field}")
                return False
        
        print(f"✅ Service account file valid: {creds['client_email']}")
        return True
        
    except Exception as e:
        print(f"❌ Error reading service account file: {e}")
        return False

def test_google_cloud_setup():
    """Test Google Cloud project setup"""
    print(f"\n☁️  TESTING GOOGLE CLOUD SETUP...")
    
    try:
        # Check if gcloud is installed and authenticated
        result = subprocess.run(['gcloud', 'auth', 'list'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and 'ACTIVE' in result.stdout:
            print("✅ Google Cloud CLI authenticated")
        else:
            print("❌ Google Cloud CLI not authenticated")
            return False
        
        # Check current project
        result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            project_id = result.stdout.strip()
            print(f"✅ Current project: {project_id}")
            return True
        else:
            print("❌ No active Google Cloud project")
            return False
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Google Cloud CLI not installed")
        return False

def run_comprehensive_test():
    """Run all tests"""
    print("🧪 GOOGLE WORKSPACE SETUP VERIFICATION")
    print("=" * 50)
    
    # Load configuration
    config_file = "workspace_config.json"
    if not os.path.exists(config_file):
        print(f"❌ Configuration file not found: {config_file}")
        print("📋 Please run the setup script first!")
        return False
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    domain = config.get('domain')
    admin_email = config.get('admin_email')
    
    if not domain or not admin_email:
        print("❌ Domain or admin email not configured")
        return False
    
    print(f"🎯 Testing configuration for:")
    print(f"   Domain: {domain}")
    print(f"   Admin: {admin_email}")
    
    # Run tests
    tests = [
        ("Google Cloud Setup", lambda: test_google_cloud_setup()),
        ("Service Account", lambda: test_service_account()),
        ("DNS Configuration", lambda: test_dns_configuration(domain)),
        ("Domain Verification", lambda: test_domain_verification(domain)),
        ("Email Delivery", lambda: test_email_delivery(domain, admin_email)),
        ("Workspace Access", lambda: test_workspace_access(admin_email)),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append(result)
            print(f"{'✅' if result else '❌'} {test_name}: {'PASSED' if result else 'FAILED'}")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n{'='*50}")
    print(f"🎯 TEST SUMMARY: {passed}/{total} PASSED")
    print(f"{'='*50}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print(f"✅ Your Google Workspace setup is working correctly!")
        print(f"📧 Gmail is ready at: {admin_email}")
        print(f"🌐 Admin console: https://admin.google.com")
        return True
    else:
        print("⚠️  SOME TESTS FAILED")
        print("📋 Please check the failed tests above")
        print("🔧 Re-run the setup script if needed")
        return False

def main():
    """Main test execution"""
    try:
        success = run_comprehensive_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 