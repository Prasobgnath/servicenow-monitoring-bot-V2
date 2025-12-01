# Dynamic Scope Configuration - Visual Guide

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER CONFIGURATION                       │
│                          (config.py)                             │
│                                                                  │
│  SCOPE_COLUMNS = ['DNS NODES', 'PROXY NODES', 'FIREWALL NODES'] │
│  INVENTORY_EXCEL = "path/to/inventory.xlsx"                     │
│  FUZZY_MATCH_THRESHOLD = 90                                     │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          │ Configuration loaded at startup
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INVENTORY LOADING                             │
│                 (load_inventory_data)                            │
│                                                                  │
│  Reads Excel file and loads columns:                            │
│  • DNS NODES → scope_data['DNS']                                │
│  • PROXY NODES → scope_data['PROXY']                            │
│  • FIREWALL NODES → scope_data['FIREWALL']                      │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          │ Dictionary of scope data
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SCOPE DETECTOR                                │
│                  (ScopeDetector class)                           │
│                                                                  │
│  scope_data = {                                                 │
│    'DNS': [dns01, dns02, dns03, ...],                           │
│    'PROXY': [proxy01, proxy02, ...],                            │
│    'FIREWALL': [fw01, fw02, ...]                                │
│  }                                                              │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          │ For each ticket
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TICKET PROCESSING                             │
│                                                                  │
│  Ticket: "Issue with dns02 server"                              │
│                                                                  │
│  Fuzzy Matching Against All Scopes:                             │
│  ┌──────────────┬──────────┐                                    │
│  │ Scope        │ Score    │                                    │
│  ├──────────────┼──────────┤                                    │
│  │ DNS          │ 95%  ✓   │ ← Best match!                      │
│  │ PROXY        │ 20%      │                                    │
│  │ FIREWALL     │ 15%      │                                    │
│  └──────────────┴──────────┘                                    │
│                                                                  │
│  Result: "DNS SCOPE"                                            │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          │ Scope assigned
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TICKET DISPLAY                                │
│                                                                  │
│  INC0001234 : 2 - High : DNS SCOPE : Team Queue : Issue with... │
└─────────────────────────────────────────────────────────────────┘
```

## Before vs After Comparison

### BEFORE (Hardcoded - Version 2.0)
```
┌────────────────┐
│   config.py    │ (No scope configuration)
└────────────────┘
        │
        ▼
┌────────────────┐
│   utils.py     │ Hardcoded:
│                │ • Load only DNS NODES
│ ScopeDetector  │ • Load only PROXY NODES
│  dns_nodes ────┼─► Check DNS first
│  proxy_nodes ──┼─► Check Proxy second
└────────────────┘
        │
        ▼
    Result: "DNS SCOPE", "PROXY SCOPE", or "Unknown SCOPE"

❌ Other teams must modify code
❌ Limited to 2 scopes only
❌ Adding new scope requires code changes
```

### AFTER (Dynamic - Version 2.1)
```
┌────────────────┐
│   config.py    │ SCOPE_COLUMNS = [...]
└────────┬───────┘
         │ User-defined scopes
         ▼
┌────────────────┐
│   utils.py     │ Dynamic:
│                │ • Load any columns from config
│ ScopeDetector  │ • Store in dictionary
│  scope_data ───┼─► Check ALL scopes
│  {'DNS': [...],│   Find BEST match
│   'PROXY': [...]│
│   ...}         │
└────────────────┘
        │
        ▼
    Result: Any configured scope (e.g., "DNS SCOPE", "FIREWALL SCOPE")

✅ Other teams just update config
✅ Unlimited number of scopes
✅ No code changes needed
```

## Data Flow Example

### Example 1: DNS Team Configuration
```
config.py
┌─────────────────────────────┐
│ SCOPE_COLUMNS = [           │
│   'DNS NODES'               │
│ ]                           │
└──────────────┬──────────────┘
               │
               ▼
inventory.xlsx
┌─────────────────────────────┐
│ DNS NODES                   │
│ ─────────                   │
│ dns-prod-01                 │
│ dns-prod-02                 │
│ dns-dev-01                  │
└──────────────┬──────────────┘
               │
               ▼
Scope Data Dictionary
┌─────────────────────────────┐
│ {                           │
│   'DNS': [                  │
│     'dns-prod-01',          │
│     'dns-prod-02',          │
│     'dns-dev-01'            │
│   ]                         │
│ }                           │
└──────────────┬──────────────┘
               │
               ▼
Ticket: "dns-prod-01 not responding"
               │
               ▼
Result: "DNS SCOPE"
```

### Example 2: Multi-Team Configuration
```
config.py
┌─────────────────────────────┐
│ SCOPE_COLUMNS = [           │
│   'DNS NODES',              │
│   'PROXY NODES',            │
│   'FIREWALL NODES'          │
│ ]                           │
└──────────────┬──────────────┘
               │
               ▼
inventory.xlsx
┌─────────────────────────────┐
│ DNS NODES │ PROXY │ FIREWALL│
│ ──────────┼───────┼─────────│
│ dns-01    │ prx-01│ fw-01   │
│ dns-02    │ prx-02│ fw-02   │
└──────────────┬──────────────┘
               │
               ▼
Scope Data Dictionary
┌─────────────────────────────┐
│ {                           │
│   'DNS': [dns-01, dns-02],  │
│   'PROXY': [prx-01, prx-02],│
│   'FIREWALL': [fw-01, fw-02]│
│ }                           │
└──────────────┬──────────────┘
               │
               ▼
Ticket: "fw-01 blocking traffic"
               │
               ▼
Fuzzy Match:
  DNS: 10% (too low)
  PROXY: 15% (too low)
  FIREWALL: 92% ✓ (above threshold)
               │
               ▼
Result: "FIREWALL SCOPE"
```

## Scope Detection Algorithm

```
┌─────────────────────────────────────────┐
│  INPUT: Ticket Description              │
│  "Issue with dns-prod-01 server"        │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Initialize Variables:                  │
│  • best_match_score = 0                 │
│  • best_scope = "Unknown SCOPE"         │
└─────────────────┬───────────────────────┘
                  │
                  ▼
         ┌────────────────┐
         │ For each scope │
         │ in scope_data  │
         └────┬───────────┘
              │
              ▼
    ┌──────────────────────────────┐
    │ Fuzzy match Short Description│
    │ against all nodes            │
    │ this scope              │
    └─────┬───────────────────┘
          │
          ▼
    ┌──────────────────┐     YES    ┌──────────────────┐
    │ Score > current  │────────────►│ Update:          │
    │ best_match_score?│             │ • best_scope     │
    └────┬─────────────┘             │ • best_match_score│
         │ NO                         └──────────────────┘
         │                                     │
         └─────────────────────────────────────┘
                          │
                          ▼
                 ┌────────────────┐
                 │ More scopes?   │
                 └────┬───────┬───┘
                  YES │       │ NO
                      │       │
    ┌─────────────────┘       └──────────────┐
    │                                         │
    │ Loop back                               ▼
    │                              ┌──────────────────┐
    │                              │ Return best_scope│
    │                              └──────────────────┘
    └──────────────────────────────────────────────────┘
```

## Configuration Flexibility Matrix

```
┌──────────────────┬─────────┬─────────┬─────────┬─────────┐
│ Team Type        │ v2.0    │ v2.1    │ Effort  │ Code    │
│                  │ Support │ Support │ Required│ Changes │
├──────────────────┼─────────┼─────────┼─────────┼─────────┤
│ DNS Only         │ ✅      │ ✅      │ 30 sec  │ ❌      │
│ Proxy Only       │ ✅      │ ✅      │ 30 sec  │ ❌      │
│ DNS + Proxy      │ ✅      │ ✅      │ None    │ ❌      │
│ Firewall         │ ❌      │ ✅      │ 30 sec  │ ❌      │
│ Load Balancer    │ ❌      │ ✅      │ 30 sec  │ ❌      │
│ Multi-Scope (4+) │ ❌      │ ✅      │ 1 min   │ ❌      │
│ Custom Scopes    │ ❌      │ ✅      │ 1 min   │ ❌      │
└──────────────────┴─────────┴─────────┴─────────┴─────────┘
```

## Summary of Changes

```
File Modified: 3 core files
Files Added: 5 documentation files
Lines Changed: ~100 lines
Breaking Changes: None (backward compatible)
Configuration Required: Yes (simple list update)

Impact:
┌────────────────────────────────────────┐
│ Developers: Minimal (just config)     │
│ End Users: Maximum (any scope works)  │
│ Maintenance: Reduced (no code edits)  │
│ Scalability: Unlimited scopes         │
└────────────────────────────────────────┘
```

---

**Visual Guide Version**: 1.0  
**Created**: November 26, 2025  
**For**: Ticket Monitoring Bot v2.1  
**Last Updated**: December 2025
