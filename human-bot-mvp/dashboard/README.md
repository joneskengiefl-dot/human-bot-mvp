# Dashboard - TypeScript

Real-time web dashboard for monitoring the Human B.O.T Engine.

## Features

- ✅ Real-time session monitoring
- ✅ Statistics dashboard
- ✅ IP health status
- ✅ Session activity charts
- ✅ WebSocket real-time updates
- ✅ Modular component architecture

## Quick Start

### Prerequisites
1. **Node.js** (v18 LTS or v20 LTS recommended) - [Download](https://nodejs.org/)
   - **Recommended:** Node.js 20.x LTS (e.g., 20.20 LTS, 20.21 LTS)
   - **Alternative:** Node.js 18.x LTS
   - **Any version in the 20.x series works!** (20.20 LTS is perfect)
2. **Bot Engine API** running on port 8000

### Step 1: Install Dependencies

```bash
cd dashboard
npm install
```

### Step 2: Start Bot Engine API (Required)

**In a separate terminal:**
```bash
cd bot-engine
.\venv\Scripts\Activate.ps1  # Windows
python -m api.server
```

### Step 3: Start Dashboard

```bash
npm run dev
```

Dashboard will be available at **http://localhost:3000**

### Complete Example

**Terminal 1 (Bot Engine):**
```powershell
cd human-bot-mvp\bot-engine
.\venv\Scripts\Activate.ps1
python -m api.server
```

**Terminal 2 (Dashboard):**
```powershell
cd human-bot-mvp\dashboard
npm install
npm run dev
```

Then open: **http://localhost:3000**

## Troubleshooting

### Issue: `npm` command not found
**Solution:** Install Node.js from https://nodejs.org/ (v18 LTS or v20 LTS recommended)

### Issue: Port 3000 already in use
**Solution:** Vite will automatically try the next available port. Check terminal output for the actual port.

### Issue: Cannot connect to API
**Solution:** 
1. Make sure bot engine is running on port 8000
2. Check `http://localhost:8000/api/health` in browser
3. Verify `.env` file has correct API URL (optional, defaults are fine)

### Issue: WebSocket connection failed
**Solution:**
1. Make sure bot engine API server is running
2. Check WebSocket URL in `.env` file (optional, defaults are fine)
3. Check browser console for errors

### Issue: Dashboard shows "Loading..." forever
**Solution:**
1. Check if bot engine API is running
2. Check browser console for errors
3. Verify API URL is correct

## Available Scripts

```bash
# Development server (with hot reload)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm test

# Lint code
npm run lint
```

## Structure

```
dashboard/
├── src/
│   ├── components/     # React components
│   │   ├── Dashboard.tsx
│   │   ├── StatsCards.tsx
│   │   ├── SessionList.tsx
│   │   ├── IPStatus.tsx
│   │   └── ActivityChart.tsx
│   ├── services/       # API & WebSocket services
│   │   ├── api.ts
│   │   └── websocket.ts
│   ├── types/          # TypeScript types
│   │   └── index.ts
│   └── App.tsx         # Main app
└── package.json
```

## Configuration

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
```

## MVP Scope

### ✅ What This MVP Includes

- Basic real-time dashboard
- Session monitoring and statistics
- IP health status display
- Activity charts
- WebSocket real-time updates
- Local development only

### ❌ What This MVP Intentionally Does NOT Include

**Production Features (Future):**
- ❌ Looker/Grafana integration (per architecture PDF)
- ❌ Advanced BI visualization
- ❌ Authentication/authorization
- ❌ Production deployment
- ❌ External API integrations

**Note**: This dashboard is intentionally "overbuilt" for MVP (includes some extras like charts) but is kept simple and local-only. Future expansion will integrate with Looker/Grafana per the architecture PDF.

**MVP Statement**: This MVP validates human-like session simulation, IP rotation, and event logging only. All intelligence, optimisation, routing, BI, and monetisation features are intentionally out of scope. The dashboard is MONITOR-ONLY and does not control execution.
