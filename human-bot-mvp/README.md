# Human B.O.T. MVP

A modular bot engine and dashboard system for simulating human-like web traffic.

## Architecture

```
human-bot-mvp/
├── bot-engine/          # Python bot engine
│   ├── core/           # Core simulation module
│   ├── ip_rotation/    # IP rotation system
│   ├── event_logging/  # Event logging module
│   ├── ai_ready/       # AI integration ready (stub-only)
│   └── api/            # REST API server
│
└── dashboard/          # TypeScript dashboard
    ├── src/
    │   ├── components/ # React components
    │   ├── services/   # API & WebSocket services
    │   └── types/      # TypeScript types
```

## Quick Start

### Bot Engine (Python)

```bash
cd bot-engine
pip install -r requirements.txt
playwright install chromium
python -m pytest tests/
python main.py
```

### Dashboard (TypeScript)

```bash
cd dashboard
npm install
npm test
npm run dev
```

## Features

- ✅ Human-like behavior simulation
- ✅ IP rotation system
- ✅ Event logging with SQLite
- ✅ Real-time dashboard
- ✅ AI-ready architecture (stub-only)
- ✅ Modular design

## 100 Sessions Demo

Run the demo script to generate 100 sessions:

```bash
# Windows
cd bot-engine
.\run-demo.bat

# macOS/Linux
cd bot-engine
chmod +x run-demo.sh
./run-demo.sh
```

Or directly:
```bash
cd bot-engine
python demo_100_sessions.py
```

## MVP Scope

### ✅ What This MVP Includes

**Core Layer:**
- Human-like session simulation
- SERP interaction (clicks, scrolling, dwell time)
- Behavioral fingerprinting (device profiles, user agents)
- Basic event logging

**Execution Layer:**
- IP rotation and scoring
- Basic proxy management
- Event logging to SQLite (queryable)
- Session tracking

**AI-Ready Scaffolding:**
- `ai_ready/` module structure (stub-only, no intelligence yet)
- Feedback loop hooks (not yet functional)
- Pattern analysis structure (not yet implemented)

**Dashboard:**
- Basic real-time monitoring
- Session statistics
- IP health status
- Local development only

### ❌ What This MVP Intentionally Does NOT Include

**Intelligence Layer (Future):**
- ❌ BI integration (Looker/Grafana)
- ❌ AI routing decisions
- ❌ Trend monitoring and detection
- ❌ RL/autonomy
- ❌ ML model integration
- ❌ Adaptive routing

**Production Features (Future):**
- ❌ Authentication/authorization
- ❌ External API partners
- ❌ Production deployment
- ❌ Advanced monitoring

**Note**: The `ai_ready/` module exists as scaffolding only. It does NOT implement any intelligence layer behavior yet - it's intentionally stub-only for future expansion per the architecture PDF.

**MVP Statement**: This MVP validates human-like session simulation, IP rotation, and event logging only. All intelligence, optimisation, routing, BI, and monetisation features are intentionally out of scope.

## Querying Logs

All events are stored in SQLite database at `bot-engine/data/human_bot.db`. Example queries:

```sql
-- Get all sessions
SELECT * FROM sessions;

-- Get successful sessions
SELECT * FROM sessions WHERE success = 1;

-- Get click events
SELECT * FROM events WHERE event_type = 'click';

-- Get session statistics
SELECT 
    COUNT(*) as total_sessions,
    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
    AVG(duration) as avg_duration
FROM sessions;
```

## API (Local/Dev Only)

**⚠️ The API is intentionally local-only for MVP. No authentication, no external access, no production deployment yet.**

See `bot-engine/README.md` for API endpoints and usage.

## Running Both Services Together

To see data in the dashboard, you need **both** services running:

### Step 1: Start the Bot Engine API Server

**Open a new terminal/PowerShell window:**

```powershell
cd human-bot-mvp\bot-engine
.\run-api.bat
```

**Or manually:**
```powershell
cd human-bot-mvp\bot-engine
.\venv\Scripts\Activate.ps1
python -m api.server
```

You should see: `INFO: Uvicorn running on http://0.0.0.0:8000`

### Step 2: Start the Dashboard

**Open another terminal/PowerShell window:**

```powershell
cd human-bot-mvp\dashboard
npm run dev
```

Dashboard will be available at **http://localhost:3000**

### Step 3: Run Bot Sessions

**Option A: Use Demo Script (Recommended for MVP)**
```powershell
cd human-bot-mvp\bot-engine
.\venv\Scripts\Activate.ps1
python demo_100_sessions.py
```

**Option B: Use API Directly**
```powershell
curl -X POST http://localhost:8000/api/sessions/run -H "Content-Type: application/json" -d "{\"count\": 5}"
```

### Troubleshooting

- **Dashboard shows "API Disconnected"**: Check if API server is running on port 8000
- **Dashboard shows "No data available"**: Run bot sessions first (use demo script or API)
- **Port conflicts**: Vite will automatically try the next available port for dashboard

## Documentation

- **README.md** (this file) - Project overview and quick start
- **bot-engine/README.md** - Bot engine setup, usage, and API documentation
- **dashboard/README.md** - Dashboard setup and usage

See individual README files in each directory for detailed setup instructions.
