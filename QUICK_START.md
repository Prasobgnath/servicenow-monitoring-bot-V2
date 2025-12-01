# 🚀 Quick Start Guide

Welcome to the refactored Ticket Monitoring Bot! This guide will get you running in 5 minutes.

## ⚡ Super Quick Start (For Experienced Users)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Edit config.py (update these lines):
#    - Line 8-12: File paths
#    - Line 17: Teams ID
#    - Line 24-26: Credentials

# 3. First-time profile setup (run once in non-headless mode):
#    Set headless = False in config.py
python main.py
#    Login to ServiceNow and Teams, then Ctrl+C to stop

# 4. Enable headless mode and run normally:
#    Set headless = True in config.py
python main.py
```

**To manually open Selenium Chrome profile:**
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\selenium_chrome_profile"
```

---

## 📋 Detailed Setup (First Time Users)

### Step 1: Check Prerequisites ✓

- [ ] Python 3.8+ installed
- [ ] Chrome browser installed  
- [ ] ChromeDriver downloaded (same version as Chrome)
- [ ] Access to ServiceNow (SNOW Instance 1 and SNOW Instance 2)
- [ ] Access to Microsoft Teams

### Step 1.5: Prepare Required Files ✓

You need these three files before running the bot:

#### **Inventory Excel File**
Contains your node/server lists for scope detection.

**Create it**:
1. Open Excel → New Workbook
2. Add columns: `DNS NODES`, `PROXY NODES`, `FW NODES`, `LB NODES` (or your scopes)
3. Fill in your nodes:
   ```
   DNS NODES    PROXY NODES    FW NODES    LB NODES
   dns1         proxy1-1       fw1-1       lb1
   dns2         proxy1-2       fw1-2       lb2
   dns3         proxy2-1       fw2-1       lb3
   ```
4. Save as: `all nodes list - data frame.xlsx`

#### **Log Excel File**
Records all tickets the bot processes.

**Create it**:
1. Open Excel → New Workbook
2. Rename Sheet1 to: `log`
3. Add these headers in row 1:
   ```
   Unique ID | Short Description | Affected User | Priority | Logged Time | Assignment Group | Type | Updated | Instance
   ```
4. Leave rows 2+ empty (bot fills them)
5. Save as: `Monitoring bot logs.xlsx`
6. **Important**: Close the file!

#### **Notification Sound File**
Plays when alerts are triggered.

**Options**:
- Use Windows default: `C:\Windows\Media\notify.wav`
- Download any `.wav` file
- Or use any sound file you have

Save the file somewhere accessible.

**Quick Files Checklist**:
- [ ] Inventory Excel created with node columns
- [ ] Log Excel created with "log" sheet and headers
- [ ] Notification sound (.wav) file ready
- [ ] Know the full paths to all three files

### Step 2: Install Dependencies ✓

Open PowerShell in the BOT folder:

```powershell
pip install -r requirements.txt
```

You should see:
```
Successfully installed openpyxl-3.1.2 pandas-2.1.4 ...
```

### Step 3: Configure Settings ✓

Open `config.py` in any text editor and update:

#### A. Feature Toggles (Lines 14-25) - NEW!
```python
# Enable/disable Teams messaging
ENABLE_TEAMS_MESSAGING = True  # Set to False to disable all Teams messages

# Enable/disable monitoring of specific ServiceNow instances
ENABLE_SNOW_INSTANCE_1_MONITORING = True  # Set to False to skip SNOW Instance 1
ENABLE_SNOW_INSTANCE_2_MONITORING = True   # Set to False to skip SNOW Instance 2

# Enable/disable monitoring of specific ticket types
ENABLE_INCIDENT_MONITORING = True   # Set to False to skip Incident monitoring
ENABLE_CHANGE_MONITORING = True     # Set to False to skip Change Request monitoring
ENABLE_CTASK_MONITORING = True      # Set to False to skip Change Task monitoring
```

**You can now selectively enable/disable what the bot monitors!**

#### B. File Paths (Lines 28-32)
```python
SOUND_FILE = r"C:\path\to\notify_me.wav"
CHROME_DRIVER_PATH = "chromedriver.exe"
INVENTORY_EXCEL = r"C:\path\to\inventory_nodes.xlsx"
LOG_EXCEL = r"C:\path\to\monitoring_logs.xlsx"
CHROME_USER_DATA = r"C:\selenium_chrome_profile"
```

**Replace with YOUR paths!**

#### C. Teams Configuration (Line 36)
```python
TEAMS_SENT_ID = "'BG Core Ticket Monitoring Bot'"  # Your Teams chat name
```

#### D. Login Credentials (Not Required)

The bot uses SSO (Single Sign-On) authentication via your Chrome profile. No manual credentials are needed - ensure your Chrome profile has saved credentials for your ServiceNow instances.

### Step 4: Chrome Profile Setup (Choose One Method) ✓

The bot uses a dedicated Chrome profile to avoid conflicts with your regular browser.

#### **Method A: Copy Existing Profile (Recommended - Includes SSO)**

This copies your Chrome profile with SSO extension and saved logins.

1. **Close all Chrome windows**

2. **Run this PowerShell command** (as Administrator):
   ```powershell
   # Copy your Chrome profile
   if (Test-Path "C:\selenium_chrome_profile") { 
       Remove-Item "C:\selenium_chrome_profile" -Recurse -Force 
   }
   Copy-Item "C:\Users\$env:USERNAME\AppData\Local\Google\Chrome\User Data\Default" "C:\selenium_chrome_profile\Default" -Recurse -Force
   Remove-Item "C:\selenium_chrome_profile\Default\*Lock*" -Force -ErrorAction SilentlyContinue
   Write-Host "Profile copied! SSO extension available." -ForegroundColor Green
   ```

3. **Verify browser_manager.py** has this line (around line 63):
   ```python
   opt.add_argument('--profile-directory=Default')
   ```

4. **Test in non-headless mode** (`config.py` line 48):
   ```python
   "headless": False,  # See the browser
   ```

5. **Run the bot**:
   ```bash
   python main.py
   ```
   - Chrome opens with SSO extension
   - SSO should authenticate automatically
   - Verify ServiceNow/Teams work

6. **Enable headless mode** once verified:
   ```python
   "headless": True,
   ```

#### **Method B: Fresh Profile (Manual Login)**

If Method A doesn't work or you prefer fresh setup:

1. **Set non-headless mode** in `config.py`:
   ```python
   "headless": False,
   ```

2. **Run the bot**:
   ```bash
   python main.py
   ```

3. **Login manually** when Chrome opens:
   - ServiceNow SSO login
   - Microsoft Teams login

4. **Stop bot** (Ctrl+C) after login

5. **Enable headless mode**:
   ```python
   "headless": True,
   ```

#### **Troubleshooting**

**SSO Extension Missing?**
- Use Method A to copy your profile

**Profile Locked?**
```powershell
Remove-Item "C:\selenium_chrome_profile\Default\*Lock*" -Force
```

**Manual Profile Access:**
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\selenium_chrome_profile" --profile-directory=Default
```

### Step 5: Go Headless (Production Mode) ✓

Once you've logged in successfully:

1. In `config.py`, line 48, set:
   ```python
   "headless": True,  # Run in background
   ```

2. Run again:
   ```powershell
   python main.py
   ```

Now it runs silently in the background!

---

## 🎯 What Happens When Running?

### Every ~3.5 Minutes (200 seconds):

1. **Monitors SNOW Instance 1 Incidents** → Looks for unassigned tickets
2. **Monitors SNOW Instance 2 Incidents** → Looks for unassigned tickets  
3. **Monitors SNOW Instance 1 Changes** → Looks for unassigned changes
4. **Monitors SNOW Instance 2 Changes** → Looks for unassigned changes
5. **Monitors SNOW Instance 1 CTASKs** → Looks for overdue tasks
6. **Monitors SNOW Instance 2 CTASKs** → Looks for overdue tasks
7. **Sends Teams Alert** → If unassigned tickets found
8. **Logs to Excel** → Records all activity
9. **Sleeps 200s** → Then repeats

### When Unassigned Tickets Found:

1. **Plays Sound** → notify_me.wav
2. **Opens Teams** → Navigates to your chat
3. **Sends Alert** → Lists all unassigned tickets
4. **Sends Reminders** → Up to 5 times if not resolved

---

## 🔧 Common Configurations

### Enable/Disable Monitoring Features (NEW!)

Edit `config.py` lines 14-25 to toggle features:

```python
# Example: Monitor only Incidents on SNOW Instance 1 (no Teams alerts)
ENABLE_TEAMS_MESSAGING = False
ENABLE_SNOW_INSTANCE_1_MONITORING = True
ENABLE_SNOW_INSTANCE_2_MONITORING = False
ENABLE_INCIDENT_MONITORING = True
ENABLE_CHANGE_MONITORING = False
ENABLE_CTASK_MONITORING = False
```

```python
# Example: Monitor everything on SNOW Instance 2 only
ENABLE_SNOW_INSTANCE_1_MONITORING = False
ENABLE_SNOW_INSTANCE_2_MONITORING = True
# All ticket types stay enabled
```

### Change How Often It Checks

Edit `config.py` around line 200:

```python
TIMEOUTS = {
    "sleep_between_scans": 200,  # seconds (200 = ~3.5 min)
}
```

Want every 5 minutes? Set to `300`  
Want every 10 minutes? Set to `600`

### Alaska Login (Optional - Only If SSO Fails)

**By default**, the bot uses SSO authentication via your Chrome profile. If SSO fails:

Edit `config.py` lines 44-46:

```python
# ALASKA LOGIN CREDENTIALS & OPTIONS
ENABLE_ALASKA_LOGIN = True  # Set to True only if Alaska login fails with SSO
ALASKA_USERNAME = "your.email@example.com"
ALASKA_PASSWORD = "your_password"
```

**When to enable:**
- SSO authentication isn't working
- Chrome profile doesn't have saved Alaska login
- You see "Alaska login skipped" message but Alaska tickets aren't loading

**When to disable (default):**
- SSO extension works in your Chrome profile
- You successfully logged in during initial setup
- You see Alaska tickets being monitored

### Change ServiceNow URLs

Edit `config.py` around lines 98-138:

```python
INCIDENT_URLS_FIRST_SCAN = [
    "https://your-new-url.service-now.com/...",
]
```

### Update XPaths (If UI Changed)

Edit `config.py` around lines 142-198:

```python
SNOW_XPATHS = {
    "tbody": "//new/xpath/here",
}
```

---

## 🐛 Troubleshooting

### "Module not found" Error

```bash
pip install -r requirements.txt
```

Make sure you're in the BOT folder when running this.

### "ChromeDriver not found" Error

1. Download ChromeDriver: https://chromedriver.chromium.org/
2. Must match your Chrome version
3. Put `chromedriver.exe` in BOT folder

### Teams Messages Not Sending

1. Check `TEAMS_SENT_ID` in config.py
2. Make sure it matches EXACTLY (case-sensitive)
3. Include the single quotes: `"'Chat Name'"`

### Not Finding ServiceNow Elements

1. Set `"headless": False` in config.py
2. Watch what the browser does
3. XPaths may have changed - update in config.py

### Excel Logging Errors

1. Close the Excel file if it's open
2. Check file path in config.py
3. Make sure you have write permissions

---

## 📁 File Structure Quick Reference

```
config.py           ← Edit this for all settings
main.py             ← Run this to start bot
requirements.txt    ← Install dependencies from here

browser_manager.py  ← Browser and login code
ticket_monitor.py   ← Monitoring logic
teams_messenger.py  ← Teams alerts
utils.py            ← Helper functions

README.md           ← Full documentation
CONFIGURATION_GUIDE.md  ← Settings reference
ARCHITECTURE.md     ← How it works
CHANGELOG.md        ← Version history
```

**You'll mostly only edit `config.py`!**

---

## 🎓 Learning More

- **Full Documentation**: See `README.md`
- **Configuration Details**: See `CONFIGURATION_GUIDE.md`
- **Architecture Overview**: See `ARCHITECTURE.md`
- **Version Changes**: See `CHANGELOG.md`

---

## ✅ Ready to Share?

To share with teammates:

1. **Copy these files**:
   - config.py (remove your password first!)
   - main.py
   - browser_manager.py
   - ticket_monitor.py
   - teams_messenger.py
   - utils.py
   - requirements.txt
   - README.md

2. **Tell them to**:
   - Run `pip install -r requirements.txt`
   - Update config.py with their paths
   - Run `python main.py`

---

## 🆘 Still Stuck?

1. Check if all file paths in config.py are correct
2. Make sure ChromeDriver version matches Chrome version
3. Try running with `"headless": False` to see what's happening
4. Check Excel file isn't open in another program
5. Verify Teams chat name is exact match

---

## 🎉 Success Checklist

- [ ] Dependencies installed
- [ ] config.py updated with your paths
- [ ] Tested in GUI mode (headless=False)
- [ ] Saw browser open and navigate
- [ ] Tickets detected correctly
- [ ] Teams message sent
- [ ] Excel log updated
- [ ] Switched to headless mode
- [ ] Running in background

**You're all set! 🚀**

---

**Last Updated**: December 2025
