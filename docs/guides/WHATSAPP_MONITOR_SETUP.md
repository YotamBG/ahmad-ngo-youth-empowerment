# 📱 WhatsApp Web Command Monitor Setup

**Automated command execution via WhatsApp messages from your phone**

## 🎯 Overview

This system allows you to send commands via WhatsApp messages from your phone (`052 339 6883` / `+972 52 339 6883`) and have them automatically executed on your computer. Perfect for remote monitoring and control!

## 🔧 Setup Instructions

### 1. Prerequisites Check
```bash
# Verify Python 3 is installed
python3 --version

# Verify required packages are installed  
pip3 list | grep selenium
```

### 2. Start the Monitor
```bash
# From the project root directory
python3 start_whatsapp_monitor.py
```

### 3. First-Time Authentication
1. **Chrome will open** automatically to WhatsApp Web
2. **QR Code will appear** - scan it with your phone's WhatsApp
3. **Wait for "Authentication successful!"** message
4. **Monitor will start** checking for messages

### 4. Session Persistence
- After first QR scan, sessions are saved in `whatsapp_profile/`
- **No need to scan QR again** on subsequent runs
- Session stays active until you manually log out

## 📱 Available Commands

Send these messages from your phone (`052 339 6883`) to execute commands:

### Testing Commands
- **`go`** - Run complete skeptical testing cycle
- **`cycle`** - Run testing cycle (same as 'go')

### Deployment Commands  
- **`deploy`** - Deploy website to Vercel production
- **`status`** - Get current system status

### Example Usage
1. Open WhatsApp on your phone
2. Send message: `go`
3. Bot automatically responds with test results
4. All commands are logged to terminal

## 🔍 System Features

### ✅ Smart Contact Detection
- Automatically finds your contact in chat list
- Flexible number matching:
  - `052 339 6883`
  - `+972 52 339 6883`  
  - `0523396883`
  - `+972523396883`

### ✅ Real-Time Monitoring
- Checks for new messages every 5 seconds
- Only processes incoming messages (not your own)
- Prevents duplicate command execution

### ✅ Command Execution
- Runs commands with timeouts to prevent hanging
- Captures output and sends results back
- Error handling with meaningful messages

### ✅ Session Management
- Persistent browser sessions
- No repeated QR scanning required
- Browser stays open for continuous monitoring

## 🚀 Quick Start

```bash
# 1. Install dependencies (if not already installed)
pip3 install selenium selenium-stealth webdriver-manager

# 2. Start monitoring
python3 start_whatsapp_monitor.py

# 3. Scan QR code when prompted

# 4. Send 'go' from your phone to test!
```

## 📊 Command Examples

### Testing Website
```
You: go
Bot: 🔥 TESTING CYCLE COMPLETE!
     📊 Success Rate: 96.8%
     ✅ Content: 10/10 (100%)
     ✅ Design: 8/8 (100%)
     ✅ Functionality: 7/7 (100%)
```

### Deploying Updates
```
You: deploy  
Bot: 🚀 Deployment successful! Website updated.
```

### Checking Status
```
You: status
Bot: ✅ WhatsApp Monitor Active
     📊 Website: 96.8% Success Rate
     🌐 Domain: arabyouthleaders.org needs nameserver fix
```

## 🛠️ Troubleshooting

### Chrome/Driver Issues
```bash
# Update Chrome driver
pip3 install --upgrade webdriver-manager

# Clear browser profile
rm -rf whatsapp_profile/
```

### Authentication Issues
```bash
# If QR code doesn't appear:
# 1. Close all Chrome windows
# 2. Clear profile: rm -rf whatsapp_profile/
# 3. Restart monitor: python3 start_whatsapp_monitor.py
```

### Contact Not Found
- Make sure you have an existing WhatsApp conversation
- Send a message first from your phone to create the chat
- Restart monitor if contact list doesn't update

### Commands Not Working
```bash
# Check terminal output for errors
# Verify scripts directory exists with test files
ls scripts/simplified_ahmad_test.py

# Test command manually
python3 scripts/simplified_ahmad_test.py
```

## 🔐 Security Notes

- **Only processes messages from your specific number**
- **Browser session is isolated** from your main Chrome profile
- **Commands have timeout limits** to prevent system hanging
- **No external API keys** or credentials exposed

## ⚙️ Configuration

Edit `scripts/whatsapp_monitor.py` to customize:

```python
# Change target number
self.target_number = "YOUR_NUMBER_HERE"

# Change check interval (seconds)
self.check_interval = 5

# Add new commands in execute_command() method
```

## 🔄 Monitoring Status

While running, the terminal shows:
- ✅ New messages detected
- 🔥 Commands being executed  
- 📤 Responses sent back
- ⏰ Timing information
- ❌ Any errors encountered

## 🎯 Best Practices

1. **Keep terminal open** to see monitoring status
2. **Don't close Chrome window** - it needs to stay open
3. **Send simple commands** - avoid very long messages
4. **Wait for responses** before sending next command
5. **Use Ctrl+C** to stop monitoring cleanly

## 📞 Emergency Stop

If you need to stop monitoring immediately:
- **Press `Ctrl+C`** in terminal
- **Close Chrome window** manually if needed
- **Restart with** `python3 start_whatsapp_monitor.py`

---

## 🎉 You're All Set!

Your WhatsApp Command Monitor is ready! Send **`go`** from your phone to run your first test cycle. 

The system will now continuously monitor for your messages and execute commands automatically. Perfect for remote website management! 🚀 