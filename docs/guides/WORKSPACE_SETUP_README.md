# 🚀 Google Workspace Automation Setup

**Complete automation script for creating and connecting Google Workspace with custom domains**

This script automates the entire process of setting up Google Workspace, connecting your custom domain, configuring DNS records, and activating Gmail - just like we did for the Matrix Dance project.

## 🎯 What This Script Does

- ✅ **Creates Google Cloud Project** with required APIs
- ✅ **Sets up Service Accounts** for authentication
- ✅ **Verifies Domain Ownership** automatically
- ✅ **Configures DNS Records** (MX, TXT) via API
- ✅ **Creates Google Workspace Account** using Channel API
- ✅ **Activates Gmail Service** for your domain
- ✅ **Creates Admin Users** automatically
- ✅ **Provides Complete Setup Report**

## 📋 Prerequisites

### 1. Domain Requirements
- ✅ Own a domain (e.g., `arabyouthleaders.org`)
- ✅ Access to domain DNS management
- ✅ Domain registrar that supports API access (recommended: Cloudflare)

### 2. Google Account Requirements
- ✅ Google account with billing enabled
- ✅ Access to Google Cloud Console
- ✅ Ability to create Google Cloud projects

### 3. System Requirements
- ✅ Linux/macOS/WSL (Windows Subsystem for Linux)
- ✅ Python 3.8 or higher
- ✅ Internet connection

## 🛠️ Quick Start

### Step 1: Clone and Setup
```bash
# If not already in the project directory
cd ahmad-ngo

# Run the setup script
./setup_workspace.sh
```

### Step 2: Configure Your Settings
Edit the generated `workspace_config.json`:

```json
{
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
```

### Step 3: Set Environment Variables
```bash
# For Cloudflare DNS management
export CLOUDFLARE_API_TOKEN="your-cloudflare-api-token"

# For other DNS providers, set appropriate tokens
export DNS_API_KEY="your-dns-provider-api-key"
```

### Step 4: Run the Automation
```bash
# Activate virtual environment
source venv/bin/activate

# Run the automation script
python3 google_workspace_automation.py
```

## 🔧 Detailed Configuration Guide

### DNS Provider Setup

#### Option 1: Cloudflare (Recommended)
1. **Get API Token:**
   - Go to [Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens)
   - Create token with `Zone:Edit` permissions
   - Set `CLOUDFLARE_API_TOKEN` environment variable

2. **Domain Setup:**
   - Add your domain to Cloudflare
   - Update nameservers at your registrar
   - Verify DNS is active

#### Option 2: Other Providers
- The script supports manual DNS setup
- You'll be prompted to add records manually
- Follow the on-screen instructions

### Google Cloud Setup

#### Project Creation
```bash
# Create new project (optional - script can do this)
gcloud projects create ahmad-ngo-workspace --name="Ahmad NGO Workspace"

# Set billing account (required)
gcloud billing projects link ahmad-ngo-workspace --billing-account=YOUR-BILLING-ACCOUNT-ID
```

#### Enable Required APIs (automatic)
The script automatically enables:
- Cloud Channel API
- Admin SDK API
- Cloud DNS API
- IAM API

## 📊 What Happens During Setup

### Phase 1: Prerequisites Validation ✅
- Checks Python, gcloud CLI installation
- Validates configuration file
- Verifies environment variables

### Phase 2: Google Cloud Setup ☁️
- Creates/configures Google Cloud project
- Enables required APIs
- Sets up billing (if needed)

### Phase 3: Service Account Creation 🔑
- Creates automation service account
- Assigns necessary IAM roles
- Downloads service account key

### Phase 4: Domain Verification 🌐
- Gets domain verification token
- Adds DNS TXT record automatically
- Verifies domain ownership

### Phase 5: DNS Configuration 📧
- Adds Google MX records
- Configures SPF records
- Sets up DMARC (optional)

### Phase 6: Workspace Account Creation 🏢
- Uses Cloud Channel API
- Creates customer record
- Provisions cloud identity
- Sets up workspace entitlement

### Phase 7: Gmail Activation 📬
- Activates Gmail service
- Validates email routing
- Tests email delivery

### Phase 8: User Management 👥
- Creates admin users
- Sets temporary passwords
- Configures roles and permissions

## 🚨 Troubleshooting Guide

### Common Issues

#### 1. "Domain not verified"
```bash
# Check DNS propagation
dig TXT your-domain.com

# Wait for propagation (up to 48 hours)
# Re-run verification step
```

#### 2. "API not enabled"
```bash
# Manually enable APIs
gcloud services enable cloudchannel.googleapis.com
gcloud services enable admin.googleapis.com
```

#### 3. "Permission denied"
```bash
# Check service account permissions
gcloud projects get-iam-policy ahmad-ngo-workspace

# Re-run service account setup
```

#### 4. "MX records not working"
```bash
# Check MX records
dig MX your-domain.com

# Verify with Google
# https://toolbox.googleapps.com/apps/dig/
```

### Debug Mode
Run with debug logging:
```bash
export DEBUG=1
python3 google_workspace_automation.py
```

## 🔒 Security Best Practices

### 1. Service Account Security
- ✅ Store service account keys securely
- ✅ Use least-privilege IAM roles
- ✅ Rotate keys regularly
- ✅ Delete unused service accounts

### 2. API Token Security
- ✅ Use environment variables (not hardcoded)
- ✅ Limit token scope and permissions
- ✅ Set token expiration
- ✅ Monitor token usage

### 3. Workspace Security
- ✅ Enable 2-factor authentication
- ✅ Set strong password policies
- ✅ Configure mobile device management
- ✅ Enable security monitoring

## 📈 Post-Setup Recommendations

### 1. Test Email Functionality
```bash
# Test email sending
echo "Test email" | mail -s "Test" admin@your-domain.com

# Check email delivery
# Login to Gmail and verify
```

### 2. Configure Additional Security
- Set up SSO if needed
- Configure DLP policies
- Enable audit logging
- Set up backup policies

### 3. User Management
- Create additional users as needed
- Set up organizational units
- Configure group policies
- Enable mobile management

## 🆘 Support and References

### Documentation Links
- [Google Workspace Admin Help](https://support.google.com/a)
- [Cloud Channel API Documentation](https://cloud.google.com/channel/docs)
- [Admin SDK Directory API](https://developers.google.com/admin-sdk/directory)

### Matrix Dance Reference
This automation is based on the successful implementation for the Matrix Dance project where we:
- Connected `matrix-dance.com` to Google Workspace
- Automated DNS configuration via Cloudflare
- Set up Gmail with custom domain
- Created admin and user accounts

### Getting Help
1. **Check the logs** - script provides detailed logging
2. **Review troubleshooting section** above
3. **Check Google Cloud Console** for API errors
4. **Verify DNS settings** using online tools
5. **Contact support** if business-critical

## 🎉 Success Indicators

When setup is complete, you should have:
- ✅ Working Gmail at your domain
- ✅ Admin console access
- ✅ User accounts created
- ✅ DNS properly configured
- ✅ All services activated

## 📝 File Structure

```
ahmad-ngo/
├── google_workspace_automation.py    # Main automation script
├── setup_workspace.sh               # Initial setup script
├── requirements.txt                 # Python dependencies
├── workspace_config.json           # Configuration file
├── service-account-key.json        # Generated service account key
├── venv/                           # Python virtual environment
└── WORKSPACE_SETUP_README.md      # This file
```

## 🚀 Ready to Launch!

Your Google Workspace automation is ready! This script will give you the same professional email setup that we achieved with the Matrix Dance project, but automated for efficiency and reliability.

**Questions?** Check the troubleshooting guide or review the Matrix Dance implementation for reference. 