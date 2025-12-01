# Quick Configuration Guide

## For First-Time Setup

### Step 1: Configure Feature Toggles (NEW!)

```python
# Lines 14-25: Control what gets monitored

# Enable/disable Teams messaging
ENABLE_TEAMS_MESSAGING = True  # Set to False to disable all Teams messages

# Enable/disable monitoring of specific ServiceNow instances
ENABLE_EVEREST_MONITORING = True  # Set to False to skip Everest instance
ENABLE_ALASKA_MONITORING = True   # Set to False to skip Alaska instance

# Enable/disable monitoring of specific ticket types
ENABLE_INCIDENT_MONITORING = True   # Set to False to skip Incident monitoring
ENABLE_CHANGE_MONITORING = True     # Set to False to skip Change Request monitoring
ENABLE_CTASK_MONITORING = True      # Set to False to skip Change Task monitoring
```

**Common Scenarios:**
```python
# Scenario 1: Monitor only Incidents on Everest (no Teams)
ENABLE_TEAMS_MESSAGING = False
ENABLE_EVEREST_MONITORING = True
ENABLE_ALASKA_MONITORING = False
ENABLE_INCIDENT_MONITORING = True
ENABLE_CHANGE_MONITORING = False
ENABLE_CTASK_MONITORING = False

# Scenario 2: Monitor everything on Alaska only
ENABLE_EVEREST_MONITORING = False
ENABLE_ALASKA_MONITORING = True
ENABLE_INCIDENT_MONITORING = True
ENABLE_CHANGE_MONITORING = True
ENABLE_CTASK_MONITORING = True

# Scenario 3: Monitor only Changes and CTASKs (both instances)
ENABLE_INCIDENT_MONITORING = False
ENABLE_CHANGE_MONITORING = True
ENABLE_CTASK_MONITORING = True
```

### Step 2: Update File Paths in `config.py`

```python
# Line 8-12: Update these paths to match your system
SOUND_FILE = r"D:\your\path\to\notify_me.wav"
CHROME_DRIVER_PATH = "chromedriver.exe"  # or full path
INVENTORY_EXCEL = r"D:\your\path\to\inventory.xlsx"
LOG_EXCEL = r"D:\your\path\to\log.xlsx"
CHROME_USER_DATA = r"C:\Users\YOUR_USERNAME\AppData\Local\Google\Chrome\User Data\default"
```

**File Explanations**:

**SOUND_FILE** - Notification sound (WAV file)
- Plays when bot starts and when tickets are found
- Use `""` to disable sound
- Example: `r"C:\Windows\Media\notify.wav"`

**INVENTORY_EXCEL** - Your nodes/servers list
- Excel file with columns like "DNS NODES", "PROXY NODES", etc.
- Used for scope detection (fuzzy matching)
- Must match `SCOPE_COLUMNS` in config

**LOG_EXCEL** - Ticket tracking log
- Excel file with a sheet named "log"
- Bot appends each new ticket here
- Must have headers: Unique ID, Short Description, Affected User, Priority, Logged Time, Assignment Group, Type, Updated, Instance
- **Close this file before running the bot!**

**CHROME_USER_DATA** - Chrome profile directory
- Where your Chrome bookmarks/extensions are stored
- Needed for SSO authentication
- Find yours: Open Chrome → `chrome://version/` → look for "Profile Path"

### Step 3: Update Credentials in `config.py`

```python
# Lines 42-44: Update your credentials
ALASKA_USERNAME = "your.email@company.com"
ALASKA_PASSWORD = "YourPassword123"  # Consider using environment variables
```

### Step 4: Update Teams Configuration in `config.py`

```python
# Line 36: Update Teams chat/channel name
TEAMS_SENT_ID = "'Your Team Chat Name'"  # Keep the single quotes inside double quotes
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the Bot

```bash
python main.py
```

---

## Common Configuration Changes

### To Change Monitoring Frequency

Edit `config.py` line ~200:
```python
TIMEOUTS = {
    "sleep_between_scans": 200,  # Change this (in seconds)
}
```

### To Enable/Disable Headless Mode

Edit `config.py` line ~48:
```python
CHROME_OPTIONS = {
    "headless": False,  # False = see browser, True = hidden
}
```

### To Update ServiceNow URLs

Edit `config.py` lines ~98-138:
```python
INCIDENT_URLS_FIRST_SCAN = [
    "https://your-instance.service-now.com/...",
    # Add or modify URLs here
]
```

### To Change Column Numbers

If ServiceNow table columns change, update `config.py` lines ~82-96:
```python
INCIDENT_COLUMNS = {
    "inc_number": 2,           # Update column numbers
    "short_description": 4,
    # etc.
}
```

### To Update XPaths

If ServiceNow or Teams UI changes, update `config.py` lines ~142-198:
```python
SNOW_XPATHS = {
    "tbody": "//new/xpath/here",
    # Update XPaths as needed
}
```

---

## Important Notes

1. **Keep credentials secure**: Don't share `config.py` with passwords
2. **Test in GUI mode first**: Set `headless: False` to debug
3. **Backup your config**: Save a copy before making changes
4. **Check ChromeDriver version**: Must match your Chrome version

---

## File Purposes at a Glance

| File | Purpose | Edit Frequency |
|------|---------|----------------|
| `config.py` | ALL settings | Often |
| `main.py` | Run the bot | Rarely |
| `browser_manager.py` | Browser logic | Rarely |
| `ticket_monitor.py` | Monitoring logic | Rarely |
| `teams_messenger.py` | Teams alerts | Rarely |
| `utils.py` | Helper functions | Rarely |
| `requirements.txt` | Dependencies | Rarely |

**Bottom Line**: You'll mostly only need to edit `config.py`!

---

**Last Updated**: December 2025
