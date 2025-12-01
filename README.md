# Ticket Monitoring Bot - Revised Version

A refactored and well-organized ServiceNow ticket monitoring bot with Microsoft Teams integration. Monitors Incidents, Change Requests, and Change Tasks across multiple instances.

## Project Structure

```
BOT/
├── config.py              # Centralized configuration (URLs, XPaths, settings)
├── requirements.txt       # Python dependencies
├── main.py               # Main entry point
├── browser_manager.py    # Browser initialization and management
├── ticket_monitor.py     # ServiceNow ticket monitoring logic
├── teams_messenger.py    # Microsoft Teams messaging functionality
├── utils.py              # Utility functions (logging, scope detection, etc.)
├── inc_bot.py           # Original script (kept for reference)
└── README.md            # This file
```

## Features

### Modular Architecture
- **config.py**: All configuration in one place (URLs, XPaths, credentials, timeouts)
- **browser_manager.py**: Chrome browser setup and ServiceNow login
- **ticket_monitor.py**: Monitors incidents, changes, and change tasks
- **teams_messenger.py**: Sends alerts and reminders to Microsoft Teams
- **utils.py**: Helper functions for logging, scope detection, and formatting

### Key Improvements
1. **Centralized Configuration**: All paths, URLs, and XPaths in `config.py`
2. **Dependency Management**: All requirements in `requirements.txt`
3. **Categorized Functions**: Organized by purpose (browser, monitoring, messaging, utilities)
4. **Easy Maintenance**: Change URLs/XPaths in one file instead of searching through code
5. **Better Error Handling**: Consistent error handling across modules
6. **Code Reusability**: Functions can be imported and reused

## Installation

### Prerequisites
- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver (same version as Chrome)
- Access to ServiceNow (SNOW Instance 1 and SNOW Instance 2)
- Access to Microsoft Teams

### Required Files

Before running the bot, you need to prepare these essential files:

#### 1. **Inventory Excel File** (`INVENTORY_EXCEL`)
**Purpose**: Contains the list of nodes/servers for scope detection

**Format**: Excel file (.xlsx) with columns for different scopes

**Example Structure**:
```
| DNS NODES  | PROXY NODES | FW NODES    | LB NODES    |
|------------|-------------|-------------|-------------|
| dns1       | proxy1-1    | fw1-1       | lb1         |
| dns2       | proxy1-2    | fw1-2       | lb2         |
| dns3       | proxy2-1    | fw2-1       | lb3         |
```

**What it does**:
- Bot uses fuzzy matching to detect which scope a ticket belongs to
- When a ticket mentions "dns1" or "dns2", it's tagged as "DNS SCOPE"
- When a ticket mentions "proxy1-1", it's tagged as "PROXY SCOPE"

**How to create**:
1. Create a new Excel file
2. Add column headers matching your `SCOPE_COLUMNS` in config.py
3. List all nodes under each column
4. Save as `.xlsx` format

**Location**: Set the full path in `config.py`:
```python
INVENTORY_EXCEL = r"D:\path\to\all nodes list - data frame.xlsx"
```

#### 2. **Log Excel File** (`LOG_EXCEL`)
**Purpose**: Records all tickets processed by the bot for tracking and auditing

**Format**: Excel file (.xlsx) with a sheet named "log"

**Auto-generated columns**:
- `Unique ID`: Ticket number (INC123456, CHG789012, etc.)
- `Short Description`: Ticket description
- `Affected User`: User impacted
- `Priority`: 1-Critical, 2-High, 3-Moderate, etc.
- `Logged Time`: When bot first saw this ticket
- `Assignment Group`: Which team it's assigned to
- `Type`: Incident, Change Request, or Change Task
- `Updated`: Last update timestamp from ServiceNow
- `Instance`: SNOW Instance 1 or SNOW Instance 2

**What it does**:
- Bot appends a new row for each new ticket it finds
- Used to avoid duplicate alerts (checks if ticket already logged)
- Provides audit trail of all tickets

**How to create**:
1. Create a new Excel file
2. Add a sheet named "log" (case-sensitive)
3. Add these column headers in row 1:
   ```
   Unique ID | Short Description | Affected User | Priority | Logged Time | Assignment Group | Type | Updated | Instance
   ```
4. Save as `.xlsx` format
5. Leave empty (bot will populate it)

**Location**: Set the full path in `config.py`:
```python
LOG_EXCEL = r"D:\path\to\Monitoring bot logs.xlsx"
```

**Important**: Close this file before running the bot (Excel locks open files)

#### 3. **Notification Sound File** (`SOUND_FILE`)
**Purpose**: Plays an audible alert when unassigned tickets are found

**Format**: WAV audio file (.wav)

**What it does**:
- Plays sound at bot startup (confirms bot is running)
- Plays sound when new unassigned tickets are detected
- Helps get immediate attention for critical issues

**How to create/obtain**:
- Use any `.wav` file (Windows notification sounds work well)
- Download from free sound libraries
- Create your own with audio software
- Use Windows default: `C:\Windows\Media\notify.wav`

**Location**: Set the full path in `config.py`:
```python
SOUND_FILE = r"D:\path\to\notify_me.wav"
```

**Note**: Set to empty string `""` to disable sound notifications

#### Quick Setup Checklist
- [ ] Created inventory Excel with node lists
- [ ] Created log Excel with "log" sheet and headers
- [ ] Obtained a notification sound file (.wav)
- [ ] Updated all three file paths in `config.py`
- [ ] Verified files are accessible (not locked or read-only)

### Setup Steps

1. **Clone or download the project**
   ```bash
   git clone https://github.com/your-username/ticket-monitoring-bot.git
   cd ticket-monitoring-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure settings**
   - Edit `config.py` and update the following:
     - `SOUND_FILE`: Path to notification sound
     - `INVENTORY_EXCEL`: Path to nodes inventory file
     - `LOG_EXCEL`: Path to logging Excel file
     - `ALASKA_USERNAME` and `ALASKA_PASSWORD`: Your credentials
     - `TEAMS_SENT_ID`: Teams chat/channel name

4. **Ensure ChromeDriver is available**
   - Place `chromedriver.exe` in the same directory OR
   - Add it to your system PATH

5. **Chrome Profile Setup (IMPORTANT)**
   
   The bot uses a dedicated Selenium Chrome profile (`C:\selenium_chrome_profile`) to avoid conflicts with your regular Chrome browser.
   
   **Option A: Copy Your Existing Chrome Profile (Recommended - Includes SSO Extension)**
   
   This method copies your existing Chrome profile (with SSO extension and saved logins) to the Selenium profile.
   
   a. **Close all Chrome windows** (important to avoid file locks)
   
   b. **Run this PowerShell command** (open PowerShell as Administrator in the project folder):
      ```powershell
      # Copy Chrome profile with SSO extension
      if (Test-Path "C:\selenium_chrome_profile") { 
          Remove-Item "C:\selenium_chrome_profile" -Recurse -Force 
      }
      Copy-Item "C:\Users\$env:USERNAME\AppData\Local\Google\Chrome\User Data\Default" "C:\selenium_chrome_profile\Default" -Recurse -Force
      Remove-Item "C:\selenium_chrome_profile\Default\*Lock*" -Force -ErrorAction SilentlyContinue
      Write-Host "Profile copied successfully! SSO extension is now available." -ForegroundColor Green
      ```
   
   c. **Verify the browser_manager.py includes the profile directory**:
      ```python
      # In browser_manager.py, around line 62-63:
      opt.add_argument(f'--user-data-dir={config.CHROME_USER_DATA}')
      opt.add_argument('--profile-directory=Default')  # Use the copied Default profile
      ```
   
   d. **Run the bot in non-headless mode** to verify SSO works:
      ```python
      # In config.py, set:
      CHROME_OPTIONS = {
          "headless": False,  # Set to False to see the browser
          # ... other options
      }
      ```
   
   e. **Run the bot**:
      ```bash
      python main.py
      ```
      - Chrome should open with your SSO extension visible
      - SSO should authenticate automatically (or prompt once)
      - Verify you can access ServiceNow and Teams without manual login
   
   f. **Enable headless mode** for automated runs:
      ```python
      CHROME_OPTIONS = {
          "headless": True,  # Set back to True
          # ... other options
      }
      ```
   
   **Option B: Fresh Profile Setup (Manual Login Required)**
   
   If you prefer to start with a fresh profile or Option A doesn't work:
   
   a. **Set bot to non-headless mode** in `config.py`:
      ```python
      CHROME_OPTIONS = {
          "headless": False,  # Set to False for first run
          # ... other options
      }
      ```
   
   b. **Run the bot** for the first time:
      ```bash
      python main.py
      ```
   
   c. **Login manually** when Chrome opens:
      - Login to ServiceNow (Everest/Alaska) with SSO
      - Login to Microsoft Teams
      - Wait for pages to fully load
   
   d. **Stop the bot** (Ctrl+C) after logging in
   
   e. **Enable headless mode** in `config.py`:
      ```python
      CHROME_OPTIONS = {
          "headless": True,  # Set back to True for automated runs
          # ... other options
      }
      ```
   
   **Troubleshooting Chrome Profile Issues:**
   
   - **SSO Extension Not Working**: Use Option A to copy your Chrome profile
   - **Profile Locked Error**: Close all Chrome windows and delete lock files:
     ```powershell
     Remove-Item "C:\selenium_chrome_profile\Default\*Lock*" -Force
     ```
   - **Manual Profile Access**: To manually open and verify the profile:
     ```cmd
     "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\selenium_chrome_profile" --profile-directory=Default
     ```
   - **Re-copy Profile**: If profile gets corrupted, run the copy command from Option A again
   
   **Note**: The profile will remember your logins, extensions, and settings for future automated runs.

## Usage

### Run the Bot

```bash
python main.py
```

### What It Does

1. **Monitors ServiceNow Queues**:
   - Incidents (SNOW Instance 1 and SNOW Instance 2)
   - Change Requests
   - Change Tasks (CTASKs)

2. **Detects Unassigned Tickets**:
   - Categorizes by priority (Critical, High, Normal)
   - Detects scope dynamically (DNS, Proxy, or custom scopes) using fuzzy matching
   - Tracks in Excel log file

3. **Sends Teams Alerts**:
   - Sends new ticket notifications
   - Sends up to 5 reminder messages
   - Formats messages with bold for high-priority tickets

4. **Continuous Monitoring**:
   - Runs in a loop with configurable sleep time
   - Handles authentication and session management

## Configuration Guide

### Essential Settings in `config.py`

#### Feature Toggles (NEW - Selective Monitoring)
Control what the bot monitors:
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

**Use Cases:**
- Disable Teams to test monitoring without sending alerts
- Monitor only one instance (SNOW Instance 1 OR SNOW Instance 2)
- Monitor specific ticket types (e.g., only Incidents)
- Run in log-only mode for auditing

#### Scope Configuration (Dynamic Scopes)
Configure which scopes to monitor from your inventory Excel file:
```python
SCOPE_COLUMNS = [
    'DNS NODES',
    'PROXY NODES'
    # Add more scopes as needed (e.g., 'FIREWALL NODES', 'LOAD BALANCER NODES')
]
```

**📖 For detailed instructions on configuring scopes for different teams, see [SCOPE_CONFIGURATION_GUIDE.md](SCOPE_CONFIGURATION_GUIDE.md)**

#### File Paths
```python
SOUND_FILE = r"path\to\notify_me.wav"
INVENTORY_EXCEL = r"path\to\inventory.xlsx"
LOG_EXCEL = r"path\to\log.xlsx"
```

#### Chrome Settings
```python
CHROME_OPTIONS = {
    "headless": True,  # Set False to see browser GUI
    "window_size": "1920,1080",
    ...
}
```

#### ServiceNow URLs
- `INCIDENT_URLS_FIRST_SCAN`: Initial incident check
- `INCIDENT_URLS_SUBSEQUENT`: Follow-up incident checks
- `CHANGE_URLS`: Change request monitoring
- `CTASK_URLS`: Change task monitoring

#### Teams Configuration
```python
TEAMS_SENT_ID = "'Your Teams Chat Name'"
```

#### ServiceNow SSO Authentication
The bot uses SSO (Single Sign-On) authentication via your Chrome profile. Ensure your Chrome profile has saved credentials for your ServiceNow instance.

#### Timeouts
```python
TIMEOUTS = {
    "page_load": 10,
    "sleep_between_scans": 200,  # seconds between cycles
    ...
}
```

## Module Documentation

### browser_manager.py
**Classes**:
- `BrowserManager`: Handles Chrome browser lifecycle

**Key Methods**:
- `initialize_browser()`: Sets up Chrome with configured options
- `navigate_to_url(url)`: Navigates with retry logic
- `switch_to_snow_iframe()`: Switches to ServiceNow shadow DOM iframe

### ticket_monitor.py
**Classes**:
- `TicketMonitor`: Main monitoring logic

**Key Methods**:
- `monitor_tickets(url, column_config)`: Monitors ticket queue
- `read_table_rows()`: Extracts ticket data from table
- `paginate_and_collect()`: Handles pagination

**Functions**:
- `monitor_incident()`: Wrapper for incident monitoring
- `monitor_change()`: Wrapper for change/CTASK monitoring

### teams_messenger.py
**Classes**:
- `TeamsMessenger`: Handles all Teams interactions

**Key Methods**:
- `send_ticket_alert()`: Sends complete ticket notification
- `send_reminder()`: Sends reminder messages
- `should_send_message()`: Determines if message should be sent

### utils.py
**Classes**:
- `LogManager`: Excel logging functionality
- `ScopeDetector`: Dynamic fuzzy matching for configurable scopes (DNS, Proxy, Firewall, etc.)
- `SoundNotifier`: Plays notification sounds

**Functions**:
- `get_instance_name()`: Detects instance from URL
- `format_ticket_display()`: Formats ticket for display
- `load_inventory_data()`: Dynamically loads scope node lists from configured columns

## Customization

### Add New ServiceNow Instance
1. Add URL to appropriate list in `config.py`:
   ```python
   INCIDENT_URLS_FIRST_SCAN.append("https://newinstance.service-now.com/...")
   ```

### Change Column Mappings
Edit `INCIDENT_COLUMNS` or `CHANGE_COLUMNS` in `config.py`:
```python
INCIDENT_COLUMNS = {
    "inc_number": 2,        # Column index for incident number
    "priority": 7,          # Column index for priority
    ...
}
```

### Modify XPaths
Update `SNOW_XPATHS` or `TEAMS_XPATHS` in `config.py`:
```python
TEAMS_XPATHS = {
    "type_message": "//div[contains(@placeholder,'Type a message')]",
    ...
}
```

### Add New Message Templates
Add to `MESSAGE_TEMPLATES` in `config.py`:
```python
MESSAGE_TEMPLATES = {
    "custom_alert": "Custom message text here",
    ...
}
```

## Troubleshooting

### SSO Extension Not Found
If you encounter SSO extension issues:

1. Open Chrome with debugging port:
   ```bash
   cd "C:\Program Files\Google\Chrome\Application"
   chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\default"
   ```

2. Verify SSO extension appears in browser
3. Keep browser open and run the bot

### Bot Not Finding Elements
1. Check if XPaths in `config.py` are up to date
2. ServiceNow UI may have changed - inspect elements and update XPaths
3. Enable GUI mode: Set `"headless": False` in `config.py`

### Teams Messages Not Sending
1. Verify `TEAMS_SENT_ID` matches exactly (case-sensitive)
2. Check Teams XPaths in `config.py`
3. Increase Teams load timeout in `TIMEOUTS`

### Excel Logging Errors
1. Ensure log Excel file is not open in another program
2. Verify file path in `config.py` is correct
3. Check file permissions

## Sharing the Bot

To share this bot with colleagues:

1. **Share these files**:
   - `config.py`
   - `main.py`
   - `browser_manager.py`
   - `ticket_monitor.py`
   - `teams_messenger.py`
   - `utils.py`
   - `requirements.txt`
   - `README.md`

2. **Instruct them to**:
   - Install Python 3.8+
   - Run `pip install -r requirements.txt`
   - Update `config.py` with their paths and credentials
   - Place `chromedriver.exe` in the directory
   - See README.md for detailed setup instructions

3. **Security Note**:
   - Remove credentials from `config.py` before sharing
   - Consider using environment variables for sensitive data

## Maintenance

### Updating URLs
- Edit appropriate URL list in `config.py`
- No code changes needed

### Updating XPaths
- Edit `SNOW_XPATHS` or `TEAMS_XPATHS` in `config.py`
- Test with GUI mode enabled

### Adding New Features
- Add configuration to `config.py`
- Extend relevant class in appropriate module
- Import and use in `main.py`

## Developer

- **Name**: Prasob G Nath
- **GitHub**: [github.com/Prasobgnath](https://github.com/Prasobgnath)

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation and guides first

---

**Version**: 2.0 (Refactored)  
**Last Updated**: December 2025
