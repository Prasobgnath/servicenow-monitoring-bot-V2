# Project Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         main.py                                 │
│                    (Orchestration Layer)                        │
│                                                                 │
│  • Initializes all components                                  │
│  • Coordinates monitoring workflow                             │
│  • Manages main execution loop                                 │
└────────┬─────────────┬─────────────┬──────────────┬───────────┘
         │             │             │              │
         │             │             │              │
┌────────▼─────┐ ┌─────▼──────┐ ┌───▼─────────┐ ┌─▼────────────┐
│ browser_     │ │ ticket_    │ │ teams_      │ │ utils.py     │
│ manager.py   │ │ monitor.py │ │ messenger.py│ │              │
│              │ │            │ │             │ │              │
│ • Browser    │ │ • Monitor  │ │ • Send      │ │ • LogManager │
│   setup      │ │   tickets  │ │   alerts    │ │ • Scope      │
│ • Login      │ │ • Paginate │ │ • Reminders │ │   Detector   │
│   handling   │ │ • Collect  │ │ • Format    │ │ • Sound      │
│              │ │   data     │ │   messages  │ │   Notifier   │
└───────┬──────┘ └──────┬─────┘ └──────┬──────┘ └──────┬───────┘
        │               │               │                │
        │               │               │                │
        └───────────────┴───────────────┴────────────────┘
                                │
                                │ (All import from)
                                │
                     ┌──────────▼───────────┐
                     │     config.py        │
                     │  (Configuration)     │
                     │                      │
                     │ • URLs               │
                     │ • XPaths             │
                     │ • File paths         │
                     │ • Credentials        │
                     │ • Timeouts           │
                     │ • Column mappings    │
                     │ • Message templates  │
                     └──────────────────────┘
```

## Data Flow

```
┌──────────┐
│ START    │
└────┬─────┘
     │
     ▼
┌─────────────────────┐
│ Initialize Browser  │ ◄──── browser_manager.py
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Login to Alaska     │ ◄──── browser_manager.py
│ (if needed)         │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────────────────────────────────┐
│         Main Monitoring Loop (repeats)          │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │ 1. Monitor Incidents                   │    │
│  │    └─► Read ServiceNow table           │◄───┼─ ticket_monitor.py
│  │    └─► Extract ticket data             │    │
│  │    └─► Log to Excel                    │◄───┼─ utils.py
│  │    └─► Detect scope (DNS/Proxy)        │◄───┼─ utils.py
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │ 2. Monitor Change Requests             │    │
│  │    └─► (same process as incidents)     │◄───┼─ ticket_monitor.py
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │ 3. Monitor Change Tasks (CTASKs)       │    │
│  │    └─► (same process as incidents)     │◄───┼─ ticket_monitor.py
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │ 4. Send Teams Notifications            │    │
│  │    └─► If new tickets: send alert      │◄───┼─ teams_messenger.py
│  │    └─► If same tickets: send reminder  │◄───┼─ teams_messenger.py
│  │    └─► Play sound notification         │◄───┼─ utils.py
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │ 5. Sleep (200 seconds)                 │    │
│  └────────────────────────────────────────┘    │
│                                                  │
└──────────────────┬──────────────────────────────┘
                   │
                   │ (Loop continues)
                   │
                   └─► Back to step 1
```

## Module Dependencies

```
main.py
├── browser_manager
│   ├── BrowserManager
│   │   ├── config (paths, options, timeouts)
│   │   └── selenium
│   └── AlaskaLogin
│       ├── config (credentials, XPaths)
│       └── selenium
│
├── ticket_monitor
│   ├── TicketMonitor
│   │   ├── config (URLs, XPaths, column mappings)
│   │   ├── LogManager (from utils)
│   │   ├── ScopeDetector (from utils)
│   │   └── selenium
│   └── monitor functions
│
├── teams_messenger
│   ├── TeamsMessenger
│   │   ├── config (XPaths, templates)
│   │   ├── SoundNotifier (from utils)
│   │   └── selenium
│   └── messaging functions
│
└── utils
    ├── LogManager
    │   ├── config (paths)
    │   ├── pandas
    │   └── openpyxl
    ├── ScopeDetector
    │   ├── config (threshold)
    │   └── fuzzywuzzy
    ├── SoundNotifier
    │   ├── config (sound file)
    │   └── winsound
    └── helper functions
```

## Configuration Flow

```
┌──────────────────┐
│   config.py      │
│                  │
│ • FILE_PATHS     │──┐
│ • URLS           │  │
│ • XPATHS         │  │
│ • CREDENTIALS    │  │
│ • TIMEOUTS       │  │
│ • COLUMNS        │  │
│ • TEMPLATES      │  │
└──────────────────┘  │
                      │
         ┌────────────┴────────────┬──────────────┬──────────────┐
         │                         │              │              │
         ▼                         ▼              ▼              ▼
┌─────────────────┐    ┌──────────────────┐  ┌────────┐  ┌────────┐
│ browser_manager │    │ ticket_monitor   │  │ teams_ │  │ utils  │
│ imports config  │    │ imports config   │  │ imports│  │ imports│
└─────────────────┘    └──────────────────┘  └────────┘  └────────┘

Result: Change config.py once, all modules use updated values!
```

## Error Handling Strategy

```
┌──────────────────────────────────────────────────┐
│              Error Handling Layers               │
├──────────────────────────────────────────────────┤
│                                                  │
│  Layer 1: Network Errors                        │
│  └─► Retry logic in browser_manager             │
│      • Retry navigation (3 attempts)            │
│      • Refresh on JavaScript errors             │
│                                                  │
│  Layer 2: Element Not Found                     │
│  └─► Timeout handling in ticket_monitor         │
│      • WebDriverWait with configured timeout    │
│      • Skip element if not critical             │
│                                                  │
│  Layer 3: Stale Elements                        │
│  └─► Re-query in pagination logic               │
│      • Catch StaleElementReference              │
│      • Refresh and continue                     │
│                                                  │
│  Layer 4: Teams Messaging                       │
│  └─► Fallback mechanisms in teams_messenger     │
│      • Keyboard shortcuts if buttons fail       │
│      • Page refresh on click interception       │
│                                                  │
│  Layer 5: Data Processing                       │
│  └─► Skip and continue in utils                 │
│      • Log errors but continue processing       │
│      • Handle missing data gracefully           │
│                                                  │
└──────────────────────────────────────────────────┘
```

## Session Management

```
Browser Session Lifecycle:

┌────────────┐
│ Initialize │
└─────┬──────┘
      │
      ▼
┌─────────────────┐     Login Required?
│ Kill Chrome     │────►│ Yes: Login to Alaska
└─────┬───────────┘     │ No: Continue
      │                 │
      ▼                 ▼
┌─────────────────┐   ┌──────────────┐
│ Start Chrome    │   │ Navigate to  │
│ with Profile    │   │ ServiceNow   │
└─────┬───────────┘   └──────┬───────┘
      │                      │
      │◄─────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│    Monitoring Sessions          │
│                                 │
│  ServiceNow ──► Teams ──► Repeat│
│     │            │              │
│     └────────────┘              │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────┐
│ On Exit/Error:  │
│ Close Browser   │
└─────────────────┘
```

---

This architecture provides:
- **Separation of Concerns**: Each module has a specific purpose
- **Loose Coupling**: Modules communicate through well-defined interfaces
- **High Cohesion**: Related functionality grouped together
- **Easy Testing**: Each component can be tested independently
- **Maintainability**: Changes in one area don't break others
