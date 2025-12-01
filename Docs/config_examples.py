"""
Example Scope Configurations for Different Teams
Copy the relevant example to config.py based on your team's needs
"""

# =====================================================================
# EXAMPLE 1: DNS TEAM ONLY
# =====================================================================
# For teams that only handle DNS tickets
SCOPE_COLUMNS_DNS_ONLY = [
    'DNS NODES'
]

# Inventory Excel structure for DNS team:
# | DNS NODES |
# |-----------|
# | dns01     |
# | dns02     |
# | dns03     |


# =====================================================================
# EXAMPLE 2: PROXY TEAM ONLY
# =====================================================================
# For teams that only handle Proxy tickets
SCOPE_COLUMNS_PROXY_ONLY = [
    'PROXY NODES'
]

# Inventory Excel structure for Proxy team:
# | PROXY NODES |
# |-------------|
# | proxy01     |
# | proxy02     |
# | proxy03     |


# =====================================================================
# EXAMPLE 3: DNS AND PROXY TEAM (DEFAULT)
# =====================================================================
# For teams handling both DNS and Proxy (current configuration)
SCOPE_COLUMNS_DNS_AND_PROXY = [
    'DNS NODES',
    'PROXY NODES'
]

# Inventory Excel structure:
# | DNS NODES | PROXY NODES |
# |-----------|-------------|
# | dns01     | proxy01     |
# | dns02     | proxy02     |
# | dns03     | proxy03     |


# =====================================================================
# EXAMPLE 4: FIREWALL TEAM
# =====================================================================
# For teams managing firewalls
SCOPE_COLUMNS_FIREWALL = [
    'FIREWALL NODES'
]

# Inventory Excel structure for Firewall team:
# | FIREWALL NODES |
# |----------------|
# | fw-prod-01     |
# | fw-prod-02     |
# | fw-dev-01      |


# =====================================================================
# EXAMPLE 5: LOAD BALANCER TEAM
# =====================================================================
# For teams managing load balancers
SCOPE_COLUMNS_LOAD_BALANCER = [
    'LOAD BALANCER NODES',
    'APPLICATION DELIVERY CONTROLLER NODES'
]

# Inventory Excel structure:
# | LOAD BALANCER NODES | APPLICATION DELIVERY CONTROLLER NODES |
# |---------------------|---------------------------------------|
# | lb-prod-01          | adc-prod-01                           |
# | lb-prod-02          | adc-prod-02                           |


# =====================================================================
# EXAMPLE 6: NETWORK TEAM (MULTI-SCOPE)
# =====================================================================
# For comprehensive network teams handling multiple infrastructure types
SCOPE_COLUMNS_NETWORK_TEAM = [
    'DNS NODES',
    'PROXY NODES',
    'FIREWALL NODES',
    'LOAD BALANCER NODES'
]

# Inventory Excel structure:
# | DNS NODES | PROXY NODES | FIREWALL NODES | LOAD BALANCER NODES |
# |-----------|-------------|----------------|---------------------|
# | dns01     | proxy01     | fw01           | lb01                |
# | dns02     | proxy02     | fw02           | lb02                |
# | dns03     | proxy03     | fw03           | lb03                |


# =====================================================================
# EXAMPLE 7: SMTP AND EMAIL TEAM
# =====================================================================
# For teams handling SMTP relays and email infrastructure
SCOPE_COLUMNS_SMTP_EMAIL = [
    'SMTP RELAY NODES',
    'EMAIL GATEWAY NODES'
]

# Inventory Excel structure:
# | SMTP RELAY NODES | EMAIL GATEWAY NODES |
# |------------------|---------------------|
# | smtp-relay-01    | gateway-01          |
# | smtp-relay-02    | gateway-02          |


# =====================================================================
# EXAMPLE 8: SECURITY TEAM
# =====================================================================
# For security teams managing various security appliances
SCOPE_COLUMNS_SECURITY = [
    'FIREWALL NODES',
    'IPS NODES',
    'WAF NODES',
    'VPN NODES'
]

# Inventory Excel structure:
# | FIREWALL NODES | IPS NODES | WAF NODES | VPN NODES |
# |----------------|-----------|-----------|-----------|
# | fw01           | ips01     | waf01     | vpn01     |
# | fw02           | ips02     | waf02     | vpn02     |


# =====================================================================
# EXAMPLE 9: CUSTOM NAMING CONVENTION
# =====================================================================
# You can use any column name ending with " NODES"
# The scope name will be extracted from the column name
SCOPE_COLUMNS_CUSTOM = [
    'WEB PROXY NODES',           # → WEB PROXY SCOPE
    'FORWARD PROXY NODES',       # → FORWARD PROXY SCOPE
    'REVERSE PROXY NODES',       # → REVERSE PROXY SCOPE
    'RECURSIVE DNS NODES',       # → RECURSIVE DNS SCOPE
    'AUTHORITATIVE DNS NODES'    # → AUTHORITATIVE DNS SCOPE
]


# =====================================================================
# USAGE INSTRUCTIONS
# =====================================================================
"""
To use any of these examples:

1. Choose the example that matches your team's responsibility
2. Copy the corresponding SCOPE_COLUMNS list
3. In config.py, replace the SCOPE_COLUMNS value with your chosen example:

   # In config.py, under SCOPE CONFIGURATION section:
   SCOPE_COLUMNS = [
       'YOUR COLUMN 1',
       'YOUR COLUMN 2',
       # ... add more as needed
   ]

4. Ensure your inventory Excel file has columns matching the names in SCOPE_COLUMNS

5. Update the INVENTORY_EXCEL path in config.py to point to your inventory file:
   
   INVENTORY_EXCEL = r"path\\to\\your\\inventory_file.xlsx"

6. Run the bot:
   
   python main.py

The bot will automatically:
- Load all specified scope columns from your Excel file
- Detect which scope each ticket belongs to using fuzzy matching
- Tag tickets with the appropriate scope (e.g., "DNS SCOPE", "FIREWALL SCOPE")
"""


# =====================================================================
# ADVANCED: MIXING DIFFERENT INFRASTRUCTURE TYPES
# =====================================================================
"""
You can combine any infrastructure types in SCOPE_COLUMNS:

SCOPE_COLUMNS = [
    'DNS NODES',
    'PROXY NODES',
    'FIREWALL NODES',
    'LOAD BALANCER NODES',
    'SMTP RELAY NODES',
    'VPN NODES',
    'WAF NODES',
    'IPS NODES',
    'ROUTER NODES',
    'SWITCH NODES'
]

Just ensure:
1. Each column name ends with " NODES"
2. The columns exist in your inventory Excel file
3. Each column contains a list of hostnames/device names
"""
