# Bot Engine - Python

Core simulation module for human-like web traffic.

## Structure

```
bot-engine/
├── core/              # Core simulation module
│   ├── simulator.py   # Main simulation engine
│   ├── behavior.py    # Human behavior patterns
│   └── device.py      # Device/browser profiles
├── ip_rotation/        # IP rotation system
│   ├── manager.py     # IP pool management
│   └── strategy.py    # Rotation strategies
├── event_logging/     # Event logging module
│   ├── logger.py      # Event logger
│   └── database.py    # Database storage
├── ai_ready/          # AI integration ready
│   ├── patterns.py    # Traffic pattern analysis
│   └── feedback.py    # Feedback loops
├── api/               # REST API server
│   └── server.py      # FastAPI server
├── tests/             # Unit tests
├── main.py            # Entry point
└── requirements.txt   # Dependencies
```

## Quick Setup

### Windows
```powershell
# Run automated setup
.\setup.bat

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run bot engine
python main.py --sessions 5
```

**Note:** If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### macOS/Linux
```bash
# Make setup script executable and run
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Run bot engine
python main.py --sessions 5
```

## Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows: .\venv\Scripts\Activate.ps1
# macOS/Linux: source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium

# Create directories
mkdir -p data logs

# Configure
cp config.example.yaml config.yaml
```

**Prerequisites:**
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)

## Usage

```bash
# Run bot engine (5 sessions)
python main.py --sessions 5

# Run with custom query
python main.py --sessions 10 --query "python programming"

# Run with config file
python main.py --config config.yaml --sessions 5

# Start API server
python -m api.server
# Or: uvicorn api.server:app --reload --port 8000

# Run tests
python -m pytest tests/ -v
```

## Quick Run Scripts

**Windows:**
```powershell
.\run.bat --sessions 5
.\run-api.bat
.\run-demo.bat  # Run 100 sessions demo
```

**macOS/Linux:**
```bash
chmod +x run.sh run-api.sh run-demo.sh
./run.sh --sessions 5
./run-api.sh
./run-demo.sh  # Run 100 sessions demo
```

## Configuration

1. Copy `config.example.yaml` to `config.yaml`
2. Edit `config.yaml` with your settings:
   - Add proxy URLs
   - Adjust behavior patterns
   - Configure logging

See `config.example.yaml` for all configuration options.

## Documentation

- **QUICKSTART.md** - Get started in 5 minutes
- **SETUP.md** - Detailed setup instructions
- **config.example.yaml** - Configuration reference

## 100 Sessions Demo

Run the demo script to generate 100 sessions with seeded randomness:

```bash
# Windows
python demo_100_sessions.py

# macOS/Linux
python3 demo_100_sessions.py
```

This will:
- Run 100 bot sessions
- Use seeded randomness for reproducibility
- Log all events to SQLite database (`data/human_bot.db`)
- Produce statistics at the end

## Querying Logs

All events are stored in SQLite database at `data/human_bot.db`. Example queries:

```sql
-- Get all sessions
SELECT * FROM sessions;

-- Get successful sessions
SELECT * FROM sessions WHERE success = 1;

-- Get sessions by date
SELECT * FROM sessions WHERE DATE(start_time) = DATE('now');

-- Get click events
SELECT * FROM events WHERE event_type = 'click';

-- Get session statistics
SELECT 
    COUNT(*) as total_sessions,
    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
    AVG(duration) as avg_duration
FROM sessions;

-- Get events for a specific session
SELECT * FROM events WHERE session_id = 'your-session-id';
```

## API Endpoints

**⚠️ LOCAL/DEV ONLY - No authentication or external access**

When running the API server (`python -m api.server`):

- **Health Check**: `GET http://localhost:8000/api/health`
- **Sessions**: `GET http://localhost:8000/api/sessions`
- **Run Sessions**: `POST http://localhost:8000/api/sessions/run`
- **Statistics**: `GET http://localhost:8000/api/stats`
- **IP Status**: `GET http://localhost:8000/api/ip/status`
- **WebSocket**: `WS ws://localhost:8000/ws`
- **API Docs**: `http://localhost:8000/docs`

**Note**: API is intentionally local-only for MVP. No authentication, no external partners, no production deployment yet.

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
- Event logging to SQLite
- Session tracking

**AI-Ready Scaffolding:**
- `ai_ready/` module structure (stub-only, no intelligence yet)
- Feedback loop hooks (not yet functional)
- Pattern analysis structure (not yet implemented)

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
- ❌ Scalability features
- ❌ Advanced monitoring

**Note**: The `ai_ready/` module exists as scaffolding only. It does NOT implement any intelligence layer behavior yet - it's intentionally stub-only for future expansion per the architecture PDF.

**MVP Statement**: This MVP validates human-like session simulation, IP rotation, and event logging only. All intelligence, optimisation, routing, BI, and monetisation features are intentionally out of scope.
