"""
Configuration file for Ticket Monitoring Bot
All paths, URLs, XPaths, and configuration values are centralized here for easy management

Developer: Prasob G Nath
GitHub: github.com/Prasobgnath
"""

# =====================================================================
# FILE PATHS
# =====================================================================
SOUND_FILE = "notify_me.wav"
CHROME_DRIVER_PATH = "chromedriver.exe"
INVENTORY_EXCEL = r"C:\path\to\inventory_nodes.xlsx"
LOG_EXCEL = r"C:\path\to\monitoring_logs.xlsx"

# Chrome Profile Configuration
# Using dedicated Selenium profile to avoid conflicts with regular Chrome usage
# FIRST TIME SETUP: Run bot in non-headless mode (set headless=False below), then login to ServiceNow/Teams
# To manually open this profile in Chrome, run below line in command prompt:
#   "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\selenium_chrome_profile"
CHROME_USER_DATA = r"C:\selenium_chrome_profile"

# =====================================================================
# FEATURE TOGGLES
# =====================================================================
# Enable/disable Teams messaging
ENABLE_TEAMS_MESSAGING = True  # Set to False to disable all Teams messages

# Enable/disable monitoring of specific ServiceNow instances
ENABLE_SNOW_INSTANCE_1_MONITORING = True  # Set to False to skip SNOW Instance 1
ENABLE_SNOW_INSTANCE_2_MONITORING = False   # Set to False to skip SNOW Instance 2

# Enable/disable monitoring of specific ticket types
ENABLE_INCIDENT_MONITORING = True   # Set to False to skip Incident monitoring
ENABLE_CHANGE_MONITORING = True     # Set to False to skip Change Request monitoring
ENABLE_CTASK_MONITORING = True      # Set to False to skip Change Task monitoring

# =====================================================================
# TEAMS CONFIGURATION
# =====================================================================
# Choose the teams sender/group name
TEAMS_SENT_ID = "'Monitoring Bot Channel'"
# TEAMS_SENT_ID = "'Your Channel Name'"  # Alternative sent id for testing

# =====================================================================
# CHROME OPTIONS
# =====================================================================
CHROME_OPTIONS = {
    "headless": False,  # Set to False for GUI Mode
    "window_size": "1920,1080",
    "incognito": False,
    "ignore_certificate_errors": True,
    "ignore_ssl_errors": True,
    "disable_images": True,
    "disable_gpu": True,
    "no_sandbox": True,
}

# =====================================================================
# COLUMN MAPPINGS FOR INCIDENT TABLE
# =====================================================================
INCIDENT_COLUMNS = {
    "inc_number": 2,
    "short_description": 4,
    "affected_user": 5,
    "priority": 7,
    "state": 8,
    "assignment_group": 11,
    "assigned_to": 12,
    "type": 10,
    "updated": 13,
}

# =====================================================================
# COLUMN MAPPINGS FOR CHANGE/CTASK TABLE
# =====================================================================
CHANGE_COLUMNS = {
    "chg_number": 2,
    "short_description": 3,
    "affected_user": 7,
    "priority": 4,
    "state": 6,
    "assignment_group": 10,
    "assigned_to": 11,
    "type": 5,
    "updated": 12,
}

# =====================================================================
# SERVICENOW URLS
# =====================================================================
# URL configurations for different ticket types and instances

INCIDENT_URLS_FIRST_SCAN = [
    "https://everest.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_query%3Dassignment_group%253D8e4ce63b879b11d0e70832a80cbb3511%255EORassignment_group%253D1d687f0087984e9cfd79db173cbb3596%255EORassignment_group%253D459f0c6e2bc51a5445e2f831ce91bfd7%255EORassignment_group%253Daf1282dc2b43d2d8828af1c3d891bf9e%255Estate!%253D7%255Estate!%253D8%255Eresolved_atONToday%40javascript%3Ags.beginningOfToday()%40javascript%3Ags.endOfToday()%26sysparm_first_row%3D1%26sysparm_view%3D",
    "https://everest.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_query%3Dassignment_group%253D8e4ce63b879b11d0e70832a80cbb3511%255EORassignment_group%253D1d687f0087984e9cfd79db173cbb3596%255EORassignment_group%253D459f0c6e2bc51a5445e2f831ce91bfd7%255EORassignment_group%253Daf1282dc2b43d2d8828af1c3d891bf9e%255Estate!%253D6%255Estate!%253D7%255Estate!%253D8%26sysparm_first_row%3D1%26sysparm_view%3D",
    "https://alaska.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_query%3Dassignment_group%253D8e4ce63b879b11d0e70832a80cbb3511%255EORassignment_group%253D1d687f0087984e9cfd79db173cbb3596%255EORassignment_group%253D459f0c6e2bc51a5445e2f831ce91bfd7%255EORassignment_group%253Daf1282dc2b43d2d8828af1c3d891bf9e%255Estate!%253D6%255Estate!%253D7%255Estate!%253D8%26sysparm_first_row%3D1%26sysparm_view%3D"
]

INCIDENT_URLS_SUBSEQUENT = [
    "https://everest.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_query%3Dassignment_group%253D8e4ce63b879b11d0e70832a80cbb3511%255EORassignment_group%253D1d687f0087984e9cfd79db173cbb3596%255EORassignment_group%253D459f0c6e2bc51a5445e2f831ce91bfd7%255EORassignment_group%253Daf1282dc2b43d2d8828af1c3d891bf9e%255Estate%253D4%26sysparm_first_row%3D1%26sysparm_view%3D",
    "https://alaska.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_query%3Dassignment_group%253D8e4ce63b879b11d0e70832a80cbb3511%255EORassignment_group%253D1d687f0087984e9cfd79db173cbb3596%255EORassignment_group%253D459f0c6e2bc51a5445e2f831ce91bfd7%255EORassignment_group%253Daf1282dc2b43d2d8828af1c3d891bf9e%255Estate%253D4%26sysparm_first_row%3D1%26sysparm_view%3D"
]

CHANGE_URLS = [
    "https://everest.service-now.com/now/nav/ui/classic/params/target/change_request_list.do%3Fsysparm_query%3Dassignment_group%253D459f0c6e2bc51a5445e2f831ce91bfd7%255EORassignment_group%253D8e4ce63b879b11d0e70832a80cbb3511%255EORassignment_group%253D1d687f0087984e9cfd79db173cbb3596%255EORassignment_group%253Daf1282dc2b43d2d8828af1c3d891bf9e%255Estate!%253D3%255Estate!%253D4%26sysparm_first_row%3D1%26sysparm_view%3D",
    "https://alaska.service-now.com/now/nav/ui/classic/params/target/change_request_list.do%3Fsysparm_query%3Dassignment_group%253D459f0c6e2bc51a5445e2f831ce91bfd7%255EORassignment_group%253D8e4ce63b879b11d0e70832a80cbb3511%255EORassignment_group%253D1d687f0087984e9cfd79db173cbb3596%255EORassignment_group%253Daf1282dc2b43d2d8828af1c3d891bf9e%255Estate!%253D3%255Estate!%253D4%26sysparm_first_row%3D1%26sysparm_view%3D"
]

CTASK_URLS = [
    "https://everest.service-now.com/now/nav/ui/classic/params/target/change_task_list.do%3Fsysparm_query%3Dassignment_group%253D8e4ce63b879b11d0e70832a80cbb3511%255EORassignment_group%253D1d687f0087984e9cfd79db173cbb3596%255EORassignment_group%253D459f0c6e2bc51a5445e2f831ce91bfd7%255Estate!%253D4%255Estate!%253D3%255Eplanned_start_date%253Cjavascript%3Ags.beginningOfCurrentMinute()%26sysparm_first_row%3D1%26sysparm_view%3D",
    "https://alaska.service-now.com/now/nav/ui/classic/params/target/change_task_list.do%3Fsysparm_query%3Dassignment_group%253D8e4ce63b879b11d0e70832a80cbb3511%255EORassignment_group%253D1d687f0087984e9cfd79db173cbb3596%255EORassignment_group%253D459f0c6e2bc51a5445e2f831ce91bfd7%255Estate!%253D4%255Estate!%253D3%255Eplanned_start_date%253Cjavascript%3Ags.beginningOfCurrentMinute()%26sysparm_first_row%3D1%26sysparm_view%3D"
]

TEAMS_URL = "https://teams.microsoft.com/v2/"
ALASKA_LOGIN_URL = "https://alaska.service-now.com/login.do"  #Remove the login.do if alaska SSO works

# =====================================================================
# XPATHS FOR SERVICENOW ELEMENTS
# =====================================================================
SNOW_XPATHS = {
    # Shadow DOM selectors (use with execute_script)
    "shadow_root": "return document.querySelector('body>macroponent-f51912f4c700201072b211d4d8c26010').shadowRoot.querySelector('sn-canvas-appshell-root')",
    "iframe": "return document.querySelector('body > macroponent-f51912f4c700201072b211d4d8c26010').shadowRoot.querySelector('[id*=main]')",
    
    # Table elements
    "empty_list": "#incident > div.list2_empty-state-list",
    "tbody": "//tbody[contains(@class,'list2_body -sticky-group-headers')]",
    
    # Pagination elements
    "first_page": "(//button[contains(@id,'_first')])[2]",
    "next_page": "(//button[contains(@id,'next')])[2]",
    "last_page": "//button[contains(@class,'list_nav  btn btn-icon h_flip_content tab_')]",
}

# =====================================================================
# XPATHS FOR ALASKA LOGIN
# =====================================================================
ALASKA_LOGIN_XPATHS = {
    "username": "//input[@id='user_name']",
    "password": "//input[@id='user_password']",
    "login_button": "//button[@id='sysverb_login']",
    "biometric_button": "//button[contains(text(),'Biometric')]",
}

# =====================================================================
# XPATHS FOR TEAMS ELEMENTS
# =====================================================================
TEAMS_XPATHS = {
    "send_id": "// span[contains(text(),{} )]",  # Format with TEAMS_SENT_ID
    "delete_button": "//button[@title='Delete']//span[@role='img']//*[name()='svg']",
    "discard_button": "//span[normalize-space()='Discard']",
    "type_message": "//div[contains(@placeholder,'Type a message')]",
    "expand_compose": "//button[@name='expand-compose']//span[@role='img']//*[name()='svg']",
    "bold_button": "//button[@name='Bold']//div[@class='ui-toolbar__itemicon']",
    "bold_button_alt": "//button[@title='Bold ']//div[@class='ui-toolbar__itemicon']",
    "send_button": "//button[@title='Send (Ctrl+Enter)']//div[@class='ui-toolbar__itemicon']",
    "format_button": "//button[@title='Show Formatting options (Ctrl+Shift+X)']//div[@class='ui-toolbar__itemicon']",
    "auth_banner": "//button[contains(@data-tid,'banner-notification')]",
}

# =====================================================================
# CSS SELECTORS
# =====================================================================
CSS_SELECTORS = {
    "total_rows": "[id*='_total_rows']",
    "last_row": "[id*=_last_row]",
}

# =====================================================================
# TIMING SETTINGS
# =====================================================================
TIMEOUTS = {
    "page_load": 10,
    "element_wait": 10,
    "implicit_wait": 30,
    "sleep_between_scans": 200,  # seconds
    "teams_load": 20,
    "login_wait": 5,
}

# =====================================================================
# MONITORING SETTINGS
# =====================================================================
MAX_REMINDER_COUNT = 5
FUZZY_MATCH_THRESHOLD = 90

# =====================================================================
# SCOPE CONFIGURATION
# =====================================================================
# Define the scope columns to load from inventory Excel file
# Format: List of column names that represent different scopes
# Example: ['DNS NODES', 'PROXY NODES', 'FIREWALL NODES', 'LOAD BALANCER NODES']
SCOPE_COLUMNS = [
    'DNS NODES',
    'PROXY NODES',
    'FW NODES',
    'LB NODES'
]
# Note: Add or remove scope columns based on your inventory Excel structure
# The scope name will be derived from column name (e.g., 'DNS NODES' -> 'DNS SCOPE')

# =====================================================================
# MESSAGE TEMPLATES
# =====================================================================
MESSAGE_TEMPLATES = {
    "incident_instance1": "Hi Team, We Have Unassigned INC Tickets in SNOW Instance 1 Queue",
    "incident_instance2": "Hi Team, We Have Unassigned INC Tickets in SNOW Instance 2 Queue",
    "change_instance1": "Hi Team, We Have Unassigned Change Tickets in SNOW Instance 1 Queue",
    "change_instance2": "Hi Team, We Have Unassigned Change Tickets in SNOW Instance 2 Queue",
    "ctask_instance1": "Hi Team, We Have Unassigned CTASKs in SNOW Instance 1 Queue",
    "ctask_instance2": "Hi Team, We Have Unassigned CTASKs in SNOW Instance 2 Queue",
    "reminder": "Reminder {} to check the queue - Bot Msg",
    "final_reminder": "Final Reminder for present queue - Bot Msg",
}
