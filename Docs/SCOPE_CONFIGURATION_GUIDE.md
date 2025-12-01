# Scope Configuration Guide

## Overview
The Ticket Monitoring Bot now supports **dynamic scope detection**, allowing different team members to use the bot with their own inventory Excel files and scope types (DNS, Proxy, Firewall, Load Balancer, etc.).

## How to Configure for Your Team

### Step 1: Prepare Your Inventory Excel File

Your inventory Excel file should have columns with node names for each scope you want to monitor. For example:

| DNS NODES | PROXY NODES | FIREWALL NODES | LOAD BALANCER NODES |
|-----------|-------------|----------------|---------------------|
| dns01     | proxy01     | fw01           | lb01                |
| dns02     | proxy02     | fw02           | lb02                |
| dns03     | proxy03     | fw03           | lb03                |

**Important Notes:**
- Column names should end with " NODES" (e.g., "DNS NODES", "FIREWALL NODES")
- Each column contains the list of nodes/servers for that scope
- Empty cells are automatically ignored

### Step 2: Update Configuration File

Open `config.py` and locate the **SCOPE CONFIGURATION** section:

```python
# =====================================================================
# SCOPE CONFIGURATION
# =====================================================================
# Define the scope columns to load from inventory Excel file
SCOPE_COLUMNS = [
    'DNS NODES',
    'PROXY NODES'
]
```

**Modify the `SCOPE_COLUMNS` list** to match your inventory file columns:

#### Example 1: DNS Team Only
```python
SCOPE_COLUMNS = [
    'DNS NODES'
]
```

#### Example 2: Firewall and Load Balancer Team
```python
SCOPE_COLUMNS = [
    'FIREWALL NODES',
    'LOAD BALANCER NODES'
]
```

#### Example 3: Multi-Scope Team
```python
SCOPE_COLUMNS = [
    'DNS NODES',
    'PROXY NODES',
    'FIREWALL NODES',
    'LOAD BALANCER NODES',
    'SMTP RELAY NODES'
]
```

### Step 3: Update Inventory Excel Path

In the same `config.py` file, update the inventory Excel path:

```python
# =====================================================================
# FILE PATHS
# =====================================================================
INVENTORY_EXCEL = r"C:\Path\To\Your\inventory_file.xlsx"
```

### Step 4: Run the Bot

That's it! Run the bot as usual:

```powershell
python main.py
```

## How It Works

1. **Loading**: The bot reads all columns specified in `SCOPE_COLUMNS` from your inventory Excel file
2. **Scope Detection**: When processing tickets, the bot uses fuzzy matching on the **Short Description** field to identify which scope each ticket belongs to
3. **Display**: Tickets are tagged with their detected scope (e.g., "DNS SCOPE", "FIREWALL SCOPE", "Unknown SCOPE")

### Scope Name Convention

The scope name is automatically derived from the column name:
- `DNS NODES` → **DNS SCOPE**
- `PROXY NODES` → **PROXY SCOPE**
- `FIREWALL NODES` → **FIREWALL SCOPE**
- `LOAD BALANCER NODES` → **LOAD BALANCER SCOPE**

## Advanced Configuration

### Adjusting Fuzzy Match Threshold

The bot uses fuzzy matching to detect node names in the ticket's **Short Description** field. You can adjust the matching sensitivity:

```python
# In config.py
FUZZY_MATCH_THRESHOLD = 90  # Default is 90 (0-100)
```

- **Higher value (95-100)**: More strict matching, fewer false positives
- **Lower value (70-85)**: More lenient matching, catches more variations
- **Recommended**: 85-90 for most use cases

## Troubleshooting

### Problem: Scope shows as "Unknown SCOPE"
**Solutions:**
1. Verify the node name exists in your inventory Excel file
2. Check that the column name is listed in `SCOPE_COLUMNS`
3. Lower the `FUZZY_MATCH_THRESHOLD` value slightly
4. Ensure node names in Excel don't have extra spaces or special characters

### Problem: Column not found warning
**Error Message:** `Warning: Column 'XYZ NODES' not found in inventory file`

**Solutions:**
1. Open your inventory Excel file and verify the exact column name
2. Update `SCOPE_COLUMNS` to match the exact column name (case-sensitive)
3. Ensure you're using the correct Excel file path

### Problem: No scopes loaded
**Error Message:** `Warning: No scope columns were loaded from inventory`

**Solutions:**
1. Verify `SCOPE_COLUMNS` is not empty in `config.py`
2. Check that your inventory Excel file has data in the specified columns
3. Ensure the Excel file exists at the path specified in `INVENTORY_EXCEL`

## Example: Setting Up for Different Teams

### Firewall Team Configuration

**config.py:**
```python
INVENTORY_EXCEL = r"D:\Team\Firewall\firewall_inventory.xlsx"

SCOPE_COLUMNS = [
    'FIREWALL NODES',
    'VPN NODES'
]
```

**firewall_inventory.xlsx:**
| FIREWALL NODES | VPN NODES |
|----------------|-----------|
| fw-prod-01     | vpn-01    |
| fw-prod-02     | vpn-02    |
| fw-dev-01      | vpn-03    |

### Load Balancer Team Configuration

**config.py:**
```python
INVENTORY_EXCEL = r"D:\Team\LoadBalancer\lb_inventory.xlsx"

SCOPE_COLUMNS = [
    'LOAD BALANCER NODES',
    'APPLICATION DELIVERY CONTROLLER NODES'
]
```

**lb_inventory.xlsx:**
| LOAD BALANCER NODES | APPLICATION DELIVERY CONTROLLER NODES |
|---------------------|---------------------------------------|
| lb-prod-01          | adc-prod-01                           |
| lb-prod-02          | adc-prod-02                           |

## Benefits of Dynamic Scope Configuration

✅ **Reusable**: One bot for multiple teams  
✅ **Flexible**: Add/remove scopes without code changes  
✅ **Scalable**: Support unlimited number of scopes  
✅ **Team-Specific**: Each team maintains their own inventory file  
✅ **Easy Setup**: Just update one list in config.py  

## Support

If you need help configuring the bot for your team, please contact the bot maintainer or refer to the main README.md file.
