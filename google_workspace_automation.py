#!/usr/bin/env python3
"""
Google Workspace Registration Automation Script
This script automates the process of registering Google Workspace with an existing domain
using the Google Cloud Channel API.

Requirements:
1. Google Cloud Project with billing enabled
2. Cloud Channel API enabled
3. Service account with proper permissions
4. Your domain name
5. Location (e.g., Versailles, France)
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from google.cloud import channel
from google.oauth2 import service_account
from google.auth import default

class GoogleWorkspaceAutomator:
    def __init__(self, domain, location="Versailles", country="FR"):
        self.domain = domain
        self.location = location
        self.country = country
        self.project_id = None
        self.account_id = None
        self.service_account_key = None
        self.reseller_admin_user = None
        
    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        print("🔍 Checking prerequisites...")
        
        # Check gcloud installation
        try:
            result = subprocess.run(['gcloud', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception("gcloud CLI not installed")
            print("✅ gcloud CLI is installed")
        except Exception as e:
            print(f"❌ gcloud CLI check failed: {e}")
            return False
        
        # Check authentication
        try:
            result = subprocess.run(['gcloud', 'auth', 'list', '--format=json'], 
                                  capture_output=True, text=True)
            auth_data = json.loads(result.stdout)
            if not auth_data:
                print("❌ No authenticated accounts found")
                return False
            print("✅ gcloud is authenticated")
        except Exception as e:
            print(f"❌ Authentication check failed: {e}")
            return False
            
        return True
    
    def setup_project(self):
        """Set up or select Google Cloud Project"""
        print("\n🛠️ Setting up Google Cloud Project...")
        
        # Get current project
        try:
            result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                                  capture_output=True, text=True)
            current_project = result.stdout.strip()
            
            if current_project and current_project != "(unset)":
                print(f"📋 Current project: {current_project}")
                use_current = input("Use current project? (y/n): ").lower().strip()
                if use_current == 'y':
                    self.project_id = current_project
                    return True
            
            # Create new project or set existing one
            project_name = input("Enter project ID (or press Enter to create new): ").strip()
            
            if not project_name:
                project_name = f"workspace-{self.domain.replace('.', '-')}-{self.location.lower()}"
                print(f"Creating new project: {project_name}")
                
                cmd = [
                    'gcloud', 'projects', 'create', project_name,
                    '--name', f"Google Workspace for {self.domain}",
                    '--labels', f'domain={self.domain.replace(".", "-")},location={self.location.lower()}'
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"❌ Failed to create project: {result.stderr}")
                    return False
                    
                print(f"✅ Created project: {project_name}")
            
            # Set the project
            subprocess.run(['gcloud', 'config', 'set', 'project', project_name])
            self.project_id = project_name
            print(f"✅ Set active project: {project_name}")
            
        except Exception as e:
            print(f"❌ Project setup failed: {e}")
            return False
            
        return True
    
    def enable_apis(self):
        """Enable required APIs"""
        print("\n🔌 Enabling required APIs...")
        
        apis = [
            'cloudchannel.googleapis.com',
            'cloudresourcemanager.googleapis.com',
            'iam.googleapis.com',
            'admin.googleapis.com'
        ]
        
        for api in apis:
            print(f"Enabling {api}...")
            result = subprocess.run([
                'gcloud', 'services', 'enable', api, 
                '--project', self.project_id
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Enabled {api}")
            else:
                print(f"❌ Failed to enable {api}: {result.stderr}")
                return False
                
        return True
    
    def create_service_account(self):
        """Create service account for Channel API"""
        print("\n👤 Creating service account...")
        
        sa_name = "workspace-provisioner"
        sa_email = f"{sa_name}@{self.project_id}.iam.gserviceaccount.com"
        
        # Create service account
        cmd = [
            'gcloud', 'iam', 'service-accounts', 'create', sa_name,
            '--display-name', 'Google Workspace Provisioner',
            '--description', 'Service account for provisioning Google Workspace',
            '--project', self.project_id
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 and "already exists" not in result.stderr:
            print(f"❌ Failed to create service account: {result.stderr}")
            return False
        
        print(f"✅ Service account ready: {sa_email}")
        
        # Grant necessary roles
        roles = [
            'roles/cloudchannel.admin',
            'roles/iam.serviceAccountUser'
        ]
        
        for role in roles:
            cmd = [
                'gcloud', 'projects', 'add-iam-policy-binding', self.project_id,
                '--member', f'serviceAccount:{sa_email}',
                '--role', role
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Granted role: {role}")
            else:
                print(f"⚠️ Warning: Could not grant {role}: {result.stderr}")
        
        # Create and download key
        key_file = f"{sa_name}-key.json"
        cmd = [
            'gcloud', 'iam', 'service-accounts', 'keys', 'create', key_file,
            '--iam-account', sa_email,
            '--project', self.project_id
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            self.service_account_key = os.path.abspath(key_file)
            print(f"✅ Service account key saved: {key_file}")
            return True
        else:
            print(f"❌ Failed to create service account key: {result.stderr}")
            return False
    
    def setup_channel_partner(self):
        """Guide user through Channel Partner setup"""
        print("\n🤝 Setting up Channel Partner Account...")
        print("""
To provision Google Workspace, you need to:

1. Go to: https://partnerdash.google.com/
2. Apply to become a Google Cloud Partner
3. Complete the Channel Partner application
4. Get approved (this can take a few days)
5. Access your Partner Sales Console
6. Find your Account ID in Settings

Note: This is a business requirement and cannot be automated.
""")
        
        account_id = input("Enter your Channel Partner Account ID (C######): ").strip()
        if not account_id.startswith('C'):
            print("❌ Account ID should start with 'C'")
            return False
            
        self.account_id = account_id
        
        admin_email = input("Enter your reseller admin email: ").strip()
        if '@' not in admin_email:
            print("❌ Invalid email address")
            return False
            
        self.reseller_admin_user = admin_email
        print(f"✅ Channel Partner setup configured")
        return True
    
    def create_workspace_customer(self):
        """Create Google Workspace customer using Channel API"""
        print(f"\n🏢 Creating Google Workspace customer for {self.domain}...")
        
        if not all([self.service_account_key, self.account_id, self.reseller_admin_user]):
            print("❌ Missing required configuration")
            return False
        
        try:
            # Set up credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_key, 
                scopes=["https://www.googleapis.com/auth/apps.order"]
            )
            credentials_delegated = credentials.with_subject(self.reseller_admin_user)
            
            # Create the API client
            client = channel.CloudChannelServiceClient(credentials=credentials_delegated)
            account_name = f"accounts/{self.account_id}"
            
            # Check if domain already has cloud identity
            print("Checking if domain already has cloud identity...")
            request = channel.CheckCloudIdentityAccountsExistRequest(
                parent=account_name, 
                domain=self.domain
            )
            
            response = client.check_cloud_identity_accounts_exist(request)
            
            if response.cloud_identity_accounts:
                print("❌ Domain already has a cloud identity. Customer must be transferred.")
                print("This is beyond the scope of this automation script.")
                return False
            
            print("✅ Domain is available for new customer creation")
            
            # Create customer
            print("Creating customer...")
            customer_request = channel.CreateCustomerRequest(
                parent=account_name,
                customer={
                    "org_display_name": f"Organization for {self.domain}",
                    "domain": self.domain,
                    "org_postal_address": {
                        "address_lines": [self.location],
                        "postal_code": "78000",  # Versailles postal code
                        "region_code": self.country
                    },
                    "correlation_id": f"AUTO-{self.domain}"
                }
            )
            
            customer = client.create_customer(customer_request)
            print(f"✅ Created customer: {customer.name}")
            
            # Provision cloud identity
            print("Provisioning cloud identity...")
            
            alternate_email = input("Enter alternate email (different domain): ").strip()
            admin_first_name = input("Enter admin first name: ").strip()
            admin_last_name = input("Enter admin last name: ").strip()
            
            cloud_identity_info = channel.CloudIdentityInfo(
                alternate_email=alternate_email, 
                language_code="en-US"
            )
            
            admin_user = channel.AdminUser(
                given_name=admin_first_name, 
                family_name=admin_last_name, 
                email=f"admin@{self.domain}"
            )
            
            cloud_identity_request = channel.ProvisionCloudIdentityRequest(
                customer=customer.name,
                cloud_identity_info=cloud_identity_info,
                user=admin_user
            )
            
            # This is a long-running operation
            operation = client.provision_cloud_identity(cloud_identity_request)
            print("Waiting for cloud identity provisioning...")
            customer = operation.result()
            
            print("✅ Cloud identity provisioned successfully!")
            print(f"Customer ID: {customer.cloud_identity_id}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to create workspace customer: {e}")
            return False
    
    def run_automation(self):
        """Run the complete automation process"""
        print(f"🚀 Starting Google Workspace registration for {self.domain}")
        print(f"📍 Location: {self.location}, {self.country}")
        print("=" * 60)
        
        steps = [
            ("Check Prerequisites", self.check_prerequisites),
            ("Setup Project", self.setup_project),
            ("Enable APIs", self.enable_apis),
            ("Create Service Account", self.create_service_account),
            ("Setup Channel Partner", self.setup_channel_partner),
            ("Create Workspace Customer", self.create_workspace_customer)
        ]
        
        for step_name, step_func in steps:
            print(f"\n{'='*20} {step_name} {'='*20}")
            
            if not step_func():
                print(f"❌ Failed at step: {step_name}")
                return False
        
        print("\n" + "="*60)
        print("🎉 Google Workspace registration automation completed!")
        print("\nNext steps:")
        print("1. The super admin will receive an email to accept Terms of Service")
        print("2. Domain verification may be required")
        print("3. Create additional users through Google Admin Console")
        print("4. Configure domain DNS settings if needed")
        
        return True

def main():
    parser = argparse.ArgumentParser(description='Automate Google Workspace registration')
    parser.add_argument('domain', help='Your domain name (e.g., example.com)')
    parser.add_argument('--location', default='Versailles', help='Location (default: Versailles)')
    parser.add_argument('--country', default='FR', help='Country code (default: FR)')
    
    args = parser.parse_args()
    
    automator = GoogleWorkspaceAutomator(args.domain, args.location, args.country)
    
    try:
        success = automator.run_automation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Automation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 