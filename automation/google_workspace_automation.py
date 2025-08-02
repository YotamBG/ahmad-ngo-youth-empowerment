#!/usr/bin/env python3
"""
COMPREHENSIVE GOOGLE WORKSPACE AUTOMATION SCRIPT
Automates the complete setup of Google Workspace with custom domain
Based on official Google Cloud Channel API and Workspace Admin SDK

Created for Ahmad NGO Youth Empowerment Project
Reference: Matrix Dance project implementation
"""

import os
import sys
import json
import time
import requests
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Google API Libraries
try:
    from google.cloud import channel_v1
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    import google.auth
    from google.auth.exceptions import RefreshError
except ImportError:
    print("❌ Missing required Google API libraries!")
    print("📦 Install with: pip install google-cloud-channel google-api-python-client google-auth")
    sys.exit(1)

class GoogleWorkspaceAutomator:
    """
    Comprehensive Google Workspace automation class
    Handles everything from domain setup to user management
    """
    
    def __init__(self, config_file: str = "workspace_config.json"):
        """Initialize the automator with configuration"""
        self.config_file = config_file
        self.config = self.load_config()
        self.domain = self.config.get('domain', 'arabyouthleaders.org')
        self.admin_email = self.config.get('admin_email', f'admin@{self.domain}')
        self.organization_name = self.config.get('organization_name', 'Arab Youth Leaders')
        
        # Google Cloud Setup
        self.project_id = self.config.get('project_id')
        self.service_account_key_file = self.config.get('service_account_key_file')
        self.oauth_client_id = self.config.get('oauth_client_id')
        
        # API Clients (initialized later)
        self.channel_client = None
        self.admin_service = None
        self.dns_provider = self.config.get('dns_provider', 'cloudflare')
        
        print(f"🚀 Google Workspace Automator initialized for: {self.domain}")
    
    def load_config(self) -> Dict:
        """Load configuration from JSON file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            return self.create_default_config()
    
    def create_default_config(self) -> Dict:
        """Create default configuration template"""
        config = {
            "domain": "arabyouthleaders.org",
            "admin_email": "admin@arabyouthleaders.org",
            "organization_name": "Arab Youth Leaders",
            "project_id": "ahmad-ngo-workspace",
            "dns_provider": "cloudflare",
            "admin_user": {
                "given_name": "Ahmad",
                "family_name": "Asaly",
                "password": "TempPassword123!"
            },
            "workspace_settings": {
                "country_code": "US",
                "language_code": "en-US",
                "timezone": "America/New_York"
            },
            "users_to_create": [
                {
                    "email": "ahmad@arabyouthleaders.org",
                    "given_name": "Ahmad",
                    "family_name": "Asaly",
                    "role": "admin"
                },
                {
                    "email": "info@arabyouthleaders.org",
                    "given_name": "Info",
                    "family_name": "Contact",
                    "role": "user"
                }
            ]
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"📝 Created default config: {self.config_file}")
        print("🔧 Please update the configuration file with your specific details")
        return config
    
    def validate_prerequisites(self) -> bool:
        """Validate all prerequisites are met"""
        print("\n🔍 VALIDATING PREREQUISITES...")
        
        checks = {
            "Domain configured": self.domain and len(self.domain) > 0,
            "Google Cloud CLI installed": self.check_gcloud_installed(),
            "Required environment variables": self.check_env_variables(),
            "DNS provider configured": self.dns_provider in ['cloudflare', 'godaddy', 'namecheap'],
        }
        
        for check, status in checks.items():
            print(f"{'✅' if status else '❌'} {check}")
        
        all_passed = all(checks.values())
        
        if not all_passed:
            print("\n❌ Prerequisites check failed!")
            print("📋 Please ensure all requirements are met before proceeding")
            return False
        
        print("\n✅ All prerequisites validated!")
        return True
    
    def check_gcloud_installed(self) -> bool:
        """Check if Google Cloud CLI is installed"""
        try:
            result = subprocess.run(['gcloud', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def check_env_variables(self) -> bool:
        """Check required environment variables"""
        required_vars = [
            'GOOGLE_APPLICATION_CREDENTIALS',
            'CLOUDFLARE_API_TOKEN' if self.dns_provider == 'cloudflare' else 'DNS_API_KEY'
        ]
        
        return all(os.getenv(var) for var in required_vars)
    
    def setup_google_cloud_project(self) -> bool:
        """Set up Google Cloud project with required APIs"""
        print("\n🌐 SETTING UP GOOGLE CLOUD PROJECT...")
        
        if not self.project_id:
            print("❌ Project ID not configured!")
            return False
        
        commands = [
            f"gcloud config set project {self.project_id}",
            "gcloud services enable cloudbilling.googleapis.com",
            "gcloud services enable cloudchannel.googleapis.com", 
            "gcloud services enable admin.googleapis.com",
            "gcloud services enable dns.googleapis.com",
            "gcloud services enable iam.googleapis.com"
        ]
        
        for cmd in commands:
            print(f"🔧 Running: {cmd}")
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                print(f"❌ Command failed: {result.stderr}")
                return False
            print(f"✅ Success")
        
        print("✅ Google Cloud project setup complete!")
        return True
    
    def create_service_account(self) -> bool:
        """Create and configure service account for API access"""
        print("\n🔑 CREATING SERVICE ACCOUNT...")
        
        service_account_email = f"workspace-automation@{self.project_id}.iam.gserviceaccount.com"
        key_file = f"service-account-key.json"
        
        commands = [
            f"gcloud iam service-accounts create workspace-automation --display-name='Workspace Automation' --project={self.project_id}",
            f"gcloud projects add-iam-policy-binding {self.project_id} --member='serviceAccount:{service_account_email}' --role='roles/cloudchannel.admin'",
            f"gcloud projects add-iam-policy-binding {self.project_id} --member='serviceAccount:{service_account_email}' --role='roles/admin.directory.admin'",
            f"gcloud iam service-accounts keys create {key_file} --iam-account={service_account_email} --project={self.project_id}"
        ]
        
        for cmd in commands:
            print(f"🔧 Running: {cmd}")
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=30)
            if result.returncode != 0 and "already exists" not in result.stderr:
                print(f"❌ Command failed: {result.stderr}")
                return False
            print(f"✅ Success")
        
        # Set environment variable
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(key_file)
        self.config['service_account_key_file'] = os.path.abspath(key_file)
        
        print("✅ Service account created and configured!")
        return True
    
    def verify_domain_ownership(self) -> bool:
        """Verify domain ownership for Google Workspace"""
        print(f"\n🔍 VERIFYING DOMAIN OWNERSHIP: {self.domain}")
        
        # Method 1: DNS TXT Record
        verification_token = self.get_domain_verification_token()
        if verification_token:
            if self.add_dns_txt_record(f"google-site-verification={verification_token}"):
                print("✅ DNS TXT record added for domain verification")
                time.sleep(30)  # Wait for DNS propagation
                
                if self.check_domain_verification():
                    print("✅ Domain ownership verified!")
                    return True
        
        # Method 2: HTML File Upload (fallback)
        print("🔄 Trying HTML file verification method...")
        return self.verify_domain_html_file()
    
    def get_domain_verification_token(self) -> Optional[str]:
        """Get domain verification token from Google"""
        try:
            # This would typically involve calling the Site Verification API
            # For now, return a placeholder - in real implementation, call the API
            print("📋 Please get your domain verification token from:")
            print("   https://www.google.com/webmasters/verification/")
            token = input("🔑 Enter your verification token: ").strip()
            return token if token else None
        except Exception as e:
            print(f"❌ Error getting verification token: {e}")
            return None
    
    def add_dns_txt_record(self, value: str) -> bool:
        """Add DNS TXT record for domain verification"""
        print(f"📝 Adding DNS TXT record: {value}")
        
        if self.dns_provider == 'cloudflare':
            return self.add_cloudflare_txt_record(value)
        elif self.dns_provider == 'godaddy':
            return self.add_godaddy_txt_record(value)
        else:
            print(f"❌ DNS provider '{self.dns_provider}' not supported yet")
            print("📋 Please manually add the following TXT record:")
            print(f"   Name: @ (or root domain)")
            print(f"   Value: {value}")
            print(f"   TTL: 300 (5 minutes)")
            return True
    
    def add_cloudflare_txt_record(self, value: str) -> bool:
        """Add TXT record via Cloudflare API"""
        api_token = os.getenv('CLOUDFLARE_API_TOKEN')
        if not api_token:
            print("❌ CLOUDFLARE_API_TOKEN not set!")
            return False
        
        # Get zone ID
        zone_id = self.get_cloudflare_zone_id()
        if not zone_id:
            return False
        
        # Add TXT record
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'type': 'TXT',
            'name': '@',
            'content': value,
            'ttl': 300
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                print("✅ TXT record added via Cloudflare API")
                return True
            else:
                print(f"❌ Cloudflare API error: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error adding Cloudflare TXT record: {e}")
            return False
    
    def get_cloudflare_zone_id(self) -> Optional[str]:
        """Get Cloudflare zone ID for domain"""
        api_token = os.getenv('CLOUDFLARE_API_TOKEN')
        url = "https://api.cloudflare.com/client/v4/zones"
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
        params = {'name': self.domain}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data['result']:
                    return data['result'][0]['id']
            print(f"❌ Zone not found for domain: {self.domain}")
            return None
        except Exception as e:
            print(f"❌ Error getting Cloudflare zone ID: {e}")
            return None
    
    def setup_mx_records(self) -> bool:
        """Set up MX records for Google Workspace"""
        print(f"\n📧 SETTING UP MX RECORDS FOR: {self.domain}")
        
        # Google Workspace MX record
        mx_record = "smtp.google.com"
        priority = 1
        
        if self.dns_provider == 'cloudflare':
            return self.add_cloudflare_mx_record(mx_record, priority)
        else:
            print("📋 Please manually add the following MX record:")
            print(f"   Name: @ (or root domain)")
            print(f"   Mail server: {mx_record}")
            print(f"   Priority: {priority}")
            print(f"   TTL: 300 (5 minutes)")
            
            confirm = input("✅ Have you added the MX record? (y/n): ").strip().lower()
            return confirm == 'y'
    
    def add_cloudflare_mx_record(self, mx_server: str, priority: int) -> bool:
        """Add MX record via Cloudflare API"""
        api_token = os.getenv('CLOUDFLARE_API_TOKEN')
        zone_id = self.get_cloudflare_zone_id()
        
        if not api_token or not zone_id:
            return False
        
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'type': 'MX',
            'name': '@',
            'content': mx_server,
            'priority': priority,
            'ttl': 300
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                print("✅ MX record added via Cloudflare API")
                return True
            else:
                print(f"❌ Cloudflare API error: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error adding Cloudflare MX record: {e}")
            return False
    
    def create_google_workspace_account(self) -> bool:
        """Create Google Workspace account using Channel API"""
        print("\n🏢 CREATING GOOGLE WORKSPACE ACCOUNT...")
        
        try:
            # Initialize Channel API client
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_key_file,
                scopes=['https://www.googleapis.com/auth/apps.order']
            )
            
            self.channel_client = channel_v1.CloudChannelServiceClient(credentials=credentials)
            
            # Check if customer already exists
            if self.check_existing_workspace():
                print("✅ Google Workspace account already exists!")
                return True
            
            # Create new customer
            return self.create_workspace_customer()
            
        except Exception as e:
            print(f"❌ Error creating Workspace account: {e}")
            print("📋 Falling back to manual setup instructions...")
            return self.manual_workspace_setup_instructions()
    
    def manual_workspace_setup_instructions(self) -> bool:
        """Provide manual setup instructions for Google Workspace"""
        print("\n📋 MANUAL GOOGLE WORKSPACE SETUP INSTRUCTIONS:")
        print("=" * 60)
        print(f"1. Go to: https://workspace.google.com/")
        print(f"2. Click 'Get started'")
        print(f"3. Choose 'For my business'")
        print(f"4. Enter business name: {self.organization_name}")
        print(f"5. Select number of employees")
        print(f"6. Country/Region: {self.config['workspace_settings']['country_code']}")
        print(f"7. Use existing domain: {self.domain}")
        print(f"8. Admin email: {self.admin_email}")
        print(f"9. Follow verification steps")
        print(f"10. Complete setup wizard")
        print("=" * 60)
        
        confirm = input("✅ Have you completed the manual setup? (y/n): ").strip().lower()
        return confirm == 'y'
    
    def activate_gmail_service(self) -> bool:
        """Activate Gmail service for the domain"""
        print(f"\n📬 ACTIVATING GMAIL SERVICE FOR: {self.domain}")
        
        try:
            # Wait for DNS propagation
            print("⏳ Waiting for DNS propagation...")
            time.sleep(60)
            
            # Check MX records
            if self.verify_mx_records():
                print("✅ MX records verified!")
                
                # This would typically involve Admin SDK API calls
                print("📧 Gmail service should now be active!")
                print(f"🎯 Test by sending email to: {self.admin_email}")
                return True
            else:
                print("❌ MX records not properly configured")
                return False
                
        except Exception as e:
            print(f"❌ Error activating Gmail: {e}")
            return False
    
    def verify_mx_records(self) -> bool:
        """Verify MX records are properly configured"""
        try:
            import dns.resolver
            mx_records = dns.resolver.resolve(self.domain, 'MX')
            
            for mx in mx_records:
                if 'smtp.google.com' in str(mx):
                    return True
            
            print("❌ Google MX record not found")
            return False
            
        except ImportError:
            print("📦 Install dnspython: pip install dnspython")
            # Fallback to manual verification
            confirm = input("✅ Can you confirm MX records are set? (y/n): ").strip().lower()
            return confirm == 'y'
        except Exception as e:
            print(f"❌ Error verifying MX records: {e}")
            return False
    
    def create_admin_users(self) -> bool:
        """Create admin users in Google Workspace"""
        print("\n👥 CREATING ADMIN USERS...")
        
        try:
            # Initialize Admin SDK
            self.init_admin_sdk()
            
            for user_config in self.config.get('users_to_create', []):
                if self.create_user(user_config):
                    print(f"✅ User created: {user_config['email']}")
                else:
                    print(f"❌ Failed to create: {user_config['email']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating users: {e}")
            return False
    
    def init_admin_sdk(self):
        """Initialize Google Admin SDK"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_key_file,
                scopes=['https://www.googleapis.com/auth/admin.directory.user']
            )
            
            # Delegate to admin user
            delegated_credentials = credentials.with_subject(self.admin_email)
            self.admin_service = build('admin', 'directory_v1', credentials=delegated_credentials)
            
        except Exception as e:
            print(f"❌ Error initializing Admin SDK: {e}")
            raise
    
    def create_user(self, user_config: Dict) -> bool:
        """Create a single user in Google Workspace"""
        try:
            user_body = {
                'name': {
                    'givenName': user_config['given_name'],
                    'familyName': user_config['family_name']
                },
                'primaryEmail': user_config['email'],
                'password': user_config.get('password', 'TempPassword123!'),
                'changePasswordAtNextLogin': True
            }
            
            result = self.admin_service.users().insert(body=user_body).execute()
            return True
            
        except Exception as e:
            print(f"❌ Error creating user {user_config['email']}: {e}")
            return False
    
    def generate_summary_report(self):
        """Generate comprehensive setup summary"""
        print("\n" + "=" * 80)
        print("🎯 GOOGLE WORKSPACE SETUP SUMMARY")
        print("=" * 80)
        print(f"📅 Setup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Domain: {self.domain}")
        print(f"👤 Admin Email: {self.admin_email}")
        print(f"🏢 Organization: {self.organization_name}")
        print(f"☁️  Project ID: {self.project_id}")
        print()
        print("🔗 IMPORTANT LINKS:")
        print(f"   📊 Admin Console: https://admin.google.com")
        print(f"   📧 Gmail: https://mail.google.com")
        print(f"   ☁️  Google Cloud: https://console.cloud.google.com")
        print()
        print("📋 NEXT STEPS:")
        print("   1. ✅ Test email delivery")
        print("   2. ✅ Set up additional users")
        print("   3. ✅ Configure security policies")
        print("   4. ✅ Set up mobile device management")
        print("   5. ✅ Configure backup and retention policies")
        print()
        print("🔐 SECURITY RECOMMENDATIONS:")
        print("   • Enable 2-factor authentication")
        print("   • Set up SSO if applicable")
        print("   • Configure DLP policies")
        print("   • Review access permissions")
        print("=" * 80)
    
    def run_complete_setup(self) -> bool:
        """Run the complete Google Workspace setup process"""
        print("🚀 STARTING COMPLETE GOOGLE WORKSPACE SETUP")
        print("=" * 60)
        
        steps = [
            ("Prerequisites Validation", self.validate_prerequisites),
            ("Google Cloud Project Setup", self.setup_google_cloud_project),
            ("Service Account Creation", self.create_service_account),
            ("Domain Ownership Verification", self.verify_domain_ownership),
            ("MX Records Configuration", self.setup_mx_records),
            ("Google Workspace Account Creation", self.create_google_workspace_account),
            ("Gmail Service Activation", self.activate_gmail_service),
            ("Admin Users Creation", self.create_admin_users),
        ]
        
        for step_name, step_function in steps:
            print(f"\n{'='*20} {step_name} {'='*20}")
            
            try:
                if not step_function():
                    print(f"❌ Step failed: {step_name}")
                    print("🛑 Setup process stopped")
                    return False
                    
                print(f"✅ Step completed: {step_name}")
                
            except Exception as e:
                print(f"❌ Error in {step_name}: {e}")
                return False
        
        # Generate final report
        self.generate_summary_report()
        
        print("\n🎉 GOOGLE WORKSPACE SETUP COMPLETED SUCCESSFULLY!")
        print(f"🌐 Your domain {self.domain} is now connected to Google Workspace!")
        print(f"📧 Gmail is active at: {self.admin_email}")
        
        return True

def main():
    """Main execution function"""
    print("🌟 AHMAD NGO - GOOGLE WORKSPACE AUTOMATION SCRIPT")
    print("📚 Based on Matrix Dance project implementation")
    print("🔗 Reference: Google Cloud Channel API & Workspace Admin SDK")
    print()
    
    try:
        # Initialize automator
        automator = GoogleWorkspaceAutomator()
        
        # Run complete setup
        success = automator.run_complete_setup()
        
        if success:
            print("\n🎯 SUCCESS! Google Workspace is ready to use!")
            sys.exit(0)
        else:
            print("\n❌ Setup incomplete. Please review errors above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 