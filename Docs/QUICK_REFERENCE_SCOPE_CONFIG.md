# Quick Reference: Dynamic Scope Configuration

## 🎯 Quick Start for Other Teams

### 1. Update config.py (30 seconds)
```python
# Find this section in config.py:
SCOPE_COLUMNS = [
    'DNS NODES',        # ← Change these to match your Excel columns
    'PROXY NODES'       # ← Add or remove as needed
]

# Examples:
# For Firewall team:
SCOPE_COLUMNS = ['FIREWALL NODES']

# For Network team:
SCOPE_COLUMNS = ['DNS NODES', 'PROXY NODES', 'FIREWALL NODES', 'LOAD BALANCER NODES']
```

### 2. Update Your Inventory Path (10 seconds)
```python
# In config.py, update this path:
INVENTORY_EXCEL = r"D:\Your\Path\To\inventory.xlsx"
```

### 3. Test Configuration (10 seconds)
```powershell
python test_scope_config.py
```

### 4. Run the Bot
```powershell
python main.py
```

---

## 📋 Inventory Excel Format

Your Excel file should have columns matching `SCOPE_COLUMNS`:

**Example for DNS + Proxy team:**
| DNS NODES   | PROXY NODES |
|-------------|-------------|
| dns-01      | proxy-01    |
| dns-02      | proxy-02    |
| dns-03      | proxy-03    |

**Example for Firewall team:**
| FIREWALL NODES |
|----------------|
| fw-prod-01     |
| fw-prod-02     |
| fw-dev-01      |

---

## ⚙️ Common Configurations

### DNS Team Only
```python
SCOPE_COLUMNS = ['DNS NODES']
```

### Proxy Team Only
```python
SCOPE_COLUMNS = ['PROXY NODES']
```

### Firewall Team
```python
SCOPE_COLUMNS = ['FIREWALL NODES']
```

### Load Balancer Team
```python
SCOPE_COLUMNS = ['LOAD BALANCER NODES']
```

### Multi-Discipline Team
```python
SCOPE_COLUMNS = [
    'DNS NODES',
    'PROXY NODES',
    'FIREWALL NODES',
    'LOAD BALANCER NODES'
]
```

---

## ✅ Verification Checklist

- [ ] `SCOPE_COLUMNS` updated in config.py
- [ ] `INVENTORY_EXCEL` path points to your Excel file
- [ ] Excel file has columns matching `SCOPE_COLUMNS`
- [ ] Excel columns contain node/server names
- [ ] Ran `python test_scope_config.py` successfully
- [ ] Test shows your scopes are loaded

---

## 🔧 Troubleshooting

### "Column not found" error
✅ Check Excel column names match exactly (case-sensitive)  
✅ Column names should end with " NODES"

### "Unknown SCOPE" for all tickets
✅ Lower `FUZZY_MATCH_THRESHOLD` in config.py (try 85 instead of 90)  
✅ Verify node names in Excel match those in ticket Short Description field  
✅ Check for typos in node names

### "No scope data loaded"
✅ Verify `INVENTORY_EXCEL` path is correct  
✅ Ensure Excel file contains data in specified columns  
✅ Check file is not corrupted

---

## 📚 Documentation

- **Full Guide**: `SCOPE_CONFIGURATION_GUIDE.md`
- **Examples**: `config_examples.py`
- **Test Script**: `test_scope_config.py`
- **Main README**: `README.md`

---

## 💡 Key Points

1. **Column names must end with " NODES"**
   - Good: `DNS NODES`, `FIREWALL NODES`
   - Bad: `DNS`, `Firewall Servers`

2. **Scope name is derived from column name**
   - `DNS NODES` → **DNS SCOPE**
   - `FIREWALL NODES` → **FIREWALL SCOPE**

3. **No code changes needed**
   - Just update `SCOPE_COLUMNS` list in config.py

4. **Test before running**
   - Always run `python test_scope_config.py` first

---

## 🆘 Need Help?

1. Read `SCOPE_CONFIGURATION_GUIDE.md` for detailed instructions
2. Check `config_examples.py` for your team type
3. Run `python test_scope_config.py` to diagnose issues
4. Contact the development team

---

**Updated**: November 26, 2025  
**Version**: 2.1 (Dynamic Scope Configuration)
