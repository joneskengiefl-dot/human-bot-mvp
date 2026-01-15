"""
FastAPI Server - REST API and WebSocket for dashboard
"""

import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.simulator import Simulator
from core.behavior import BehaviorPattern, BehaviorConfig
from core.device import DeviceManager
from ip_rotation.manager import IPManager
from ip_rotation.strategy import RotationStrategy
from event_logging.logger import EventLogger
from event_logging.database import DatabaseLogger
# MVP: AI-ready modules are stub-only, no execution paths
# from ai_ready.patterns import TrafficPatternAnalyzer
# from ai_ready.feedback import FeedbackLoop


# Pydantic models
class RunSessionRequest(BaseModel):
    count: int = 1
    search_query: Optional[str] = None
    proxy: Optional[str] = None


class SessionResponse(BaseModel):
    session_id: str
    device: str
    start_time: str
    target_url: str
    proxy: Optional[str] = None


class StatsResponse(BaseModel):
    total_sessions: int
    active_sessions: int
    successful_sessions: int
    failed_sessions: int
    total_clicks: int
    average_duration: float
    success_rate: float
    proxy_stats: List[Dict[str, Any]]
    ip_health: Dict[str, int]


# Initialize FastAPI app
app = FastAPI(title="Human B.O.T Engine API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
simulator: Optional[Simulator] = None
ip_manager: Optional[IPManager] = None
rotation_strategy: Optional[RotationStrategy] = None
event_logger: Optional[EventLogger] = None
db_logger: Optional[DatabaseLogger] = None
# MVP: AI-ready modules are stub-only, not used
# pattern_analyzer: Optional[TrafficPatternAnalyzer] = None
# feedback_loop: Optional[FeedbackLoop] = None
websocket_connections: List[WebSocket] = []


def event_callback(event: Dict[str, Any]) -> None:
    """Event callback for simulator"""
    # Log event
    if event_logger:
        event_logger.log_event(
            event["type"],
            event["data"],
            level=event.get("level", "INFO")
        )
    
    # Save to database
    if db_logger and event["type"] in ["session_start", "session_end", "click", "error"]:
        db_logger.save_event(
            event["data"].get("session_id", ""),
            event["type"],
            event["data"],
            event.get("timestamp")
        )
    
    # Broadcast to WebSocket clients
    asyncio.create_task(broadcast_event(event))


async def broadcast_event(event: Dict[str, Any]) -> None:
    """Broadcast event to all WebSocket connections"""
    message = {
        "type": "event",
        "data": event
    }
    disconnected = []
    for ws in websocket_connections:
        try:
            await ws.send_json(message)
        except Exception:
            disconnected.append(ws)
    
    for ws in disconnected:
        if ws in websocket_connections:
            websocket_connections.remove(ws)


@app.on_event("startup")
async def startup():
    """Initialize bot engine on startup"""
    global simulator, ip_manager, rotation_strategy, event_logger, db_logger
    # MVP: AI-ready modules are stub-only, not initialized
    # global pattern_analyzer, feedback_loop
    
    # Initialize components
    event_logger = EventLogger(
        log_file="logs/human_bot.log",
        log_format="json",
        log_level="INFO"
    )
    
    db_logger = DatabaseLogger(db_path="data/human_bot.db")
    
    # Initialize IP manager (will be configured from config.yaml)
    # MVP: If no proxies configured, create mock IP pool for demonstration
    # This allows IP rotation and scoring logic to be demonstrated without real proxies
    ip_manager = IPManager(proxies=[], use_mock_ips=True)  # Creates mock IPs if no proxies provided
    # TODO: Load proxies from config.yaml if needed
    
    rotation_strategy = RotationStrategy(ip_manager, strategy="round_robin")
    
    # MVP: AI-ready modules are stub-only, not initialized
    # Future: pattern_analyzer = TrafficPatternAnalyzer()
    # Future: feedback_loop = FeedbackLoop()
    
    # Initialize simulator
    behavior_pattern = BehaviorPattern()
    device_manager = DeviceManager()
    
    simulator = Simulator(
        behavior_pattern=behavior_pattern,
        device_manager=device_manager,
        event_callback=event_callback
    )
    
    await simulator.initialize()
    
    event_logger.log_event("system_start", {"message": "Bot engine started"})


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown"""
    global simulator
    if simulator:
        await simulator.close()


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    db_stats = {}
    if db_logger:
        try:
            stats = db_logger.get_statistics()
            db_stats = {
                "total_sessions_in_db": stats.get("total_sessions", 0),
                "database_path": str(db_logger.db_path)
            }
        except Exception:
            db_stats = {"database_path": str(db_logger.db_path) if db_logger else "not_initialized"}
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "active_sessions": len(simulator.active_sessions) if simulator else 0,
        **db_stats
    }


@app.get("/api/sessions", response_model=List[SessionResponse])
async def get_sessions():
    """
    Get all sessions (active + recent historical from database)
    
    Returns both:
    - Active sessions (currently running)
    - Recent historical sessions from database (last 50)
    """
    sessions_list = []
    
    # Get active sessions from simulator
    if simulator:
        active_sessions = simulator.get_active_sessions()
        for sid, info in active_sessions.items():
            sessions_list.append(SessionResponse(
                session_id=sid,
                device=info["device"],
                start_time=info["start_time"],
                target_url=info["target_url"],
                proxy=info.get("proxy")
            ))
    
    # Get recent historical sessions from database
    if db_logger:
        try:
            historical_sessions = db_logger.get_sessions(limit=50)
            for session in historical_sessions:
                # Skip if already in active sessions
                if not any(s.session_id == session["id"] for s in sessions_list):
                    sessions_list.append(SessionResponse(
                        session_id=session["id"],
                        device=session["device"],
                        start_time=session["start_time"],
                        target_url=session["target_url"],
                        proxy=session.get("proxy")
                    ))
        except Exception as e:
            # If database query fails, log but don't break
            if event_logger:
                event_logger.log_event("error", {"message": f"Failed to get historical sessions: {e}"}, level="WARNING")
    
    # Sort by start_time descending (most recent first)
    sessions_list.sort(key=lambda x: x.start_time, reverse=True)
    
    return sessions_list


@app.post("/api/sessions/run")
async def run_sessions(request: RunSessionRequest, background_tasks: BackgroundTasks):
    """
    Local MVP Demo Trigger (Temporary) - Run sessions in background
    
    ⚠️ MVP NOTE: This endpoint exists ONLY for local MVP demonstration.
    The dashboard is MONITOR-ONLY and does NOT call this endpoint.
    
    This trigger exists only for local MVP demonstration and is not part of the final architecture.
    It will be removed in future phases when proper execution control is implemented.
    
    For MVP, use: python demo_100_sessions.py or python main.py --sessions N
    """
    if not simulator:
        raise HTTPException(status_code=500, detail="Simulator not initialized")
    
    session_ids = []
    
    async def run_session_task():
        for _ in range(request.count):
            session_id = None
            
            # Get proxy if available
            proxy = request.proxy
            if not proxy and rotation_strategy:
                proxy = rotation_strategy.get_next_proxy()
            
            # Run session
            try:
                session = await simulator.simulate_search_session(
                    session_id=session_id,
                    search_query=request.search_query,
                    proxy=proxy
                )
                session_ids.append(session["session_id"])
                
                # Save session to database
                duration = 0
                success = True
                end_time = datetime.utcnow()
                
                # Try to get duration from session_end event
                for event in reversed(session.get("events", [])):
                    if event.get("type") == "session_end":
                        duration = event.get("data", {}).get("duration", 0)
                        success = event.get("data", {}).get("success", True)
                        break
                
                # If no duration in events, calculate it
                if duration == 0 and isinstance(session["start_time"], datetime):
                    duration = (end_time - session["start_time"]).total_seconds()
                
                if db_logger:
                    db_logger.save_session({
                        "id": session["session_id"],
                        "device": session["device"],
                        "target_url": session["target_url"],
                        "proxy": proxy,
                        "start_time": session["start_time"].isoformat() if isinstance(session["start_time"], datetime) else str(session["start_time"]),
                        "end_time": end_time.isoformat(),
                        "duration": duration,
                        "success": success,
                        "events": session.get("events", [])
                    })
                
                # MVP: No feedback loop - events are logged only
                # Future: Feedback loop will be implemented in intelligence layer
                
                if proxy and rotation_strategy:
                    rotation_strategy.record_success(proxy)
            except Exception as e:
                if proxy and rotation_strategy:
                    rotation_strategy.record_failure(proxy)
                event_logger.log_error(None, str(e))
    
    background_tasks.add_task(run_session_task)
    
    return {
        "message": f"Started {request.count} session(s)",
        "session_ids": session_ids
    }


@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """Get statistics"""
    if not simulator or not db_logger:
        raise HTTPException(status_code=500, detail="Components not initialized")
    
    # Get statistics from database
    stats = db_logger.get_statistics()
    
    # Get active sessions
    active_sessions = len(simulator.active_sessions) if simulator else 0
    
    # Get proxy stats
    proxy_stats = []
    ip_health = {"healthy": 0, "flagged": 0, "blacklisted": 0}
    
    if ip_manager:
        proxy_stats = ip_manager.get_proxy_stats()
        ip_health = {
            "healthy": ip_manager.get_healthy_count(),
            "flagged": ip_manager.get_flagged_count(),
            "blacklisted": ip_manager.get_blacklisted_count()
        }
    
    return StatsResponse(
        total_sessions=stats.get("total_sessions", 0),
        active_sessions=active_sessions,
        successful_sessions=stats.get("successful_sessions", 0),
        failed_sessions=stats.get("failed_sessions", 0),
        total_clicks=stats.get("total_clicks", 0),
        average_duration=stats.get("average_duration", 0.0),
        success_rate=stats.get("success_rate", 0.0),
        proxy_stats=proxy_stats,
        ip_health=ip_health
    )


@app.get("/api/events")
async def get_events(limit: int = 200, event_type: Optional[str] = None):
    """
    Get events from database
    
    Args:
        limit: Maximum number of events to return (default: 200)
        event_type: Optional event type filter (e.g., "click", "session_start")
    
    Returns:
        List of events
    """
    if not db_logger:
        return []
    
    try:
        events = db_logger.get_events(event_type=event_type, limit=limit)
        return [
            {
                "type": event["event_type"],
                "timestamp": event["timestamp"],
                "data": event["data"]
            }
            for event in events
        ]
    except Exception as e:
        if event_logger:
            event_logger.log_event("error", {"message": f"Failed to get events: {e}"}, level="WARNING")
        return []


@app.get("/api/ip/status")
async def get_ip_status():
    """
    Get IP status
    
    Returns proxy statistics and health counts.
    For MVP: Proxies start as healthy and may be flagged/blacklisted based on failures.
    """
    if not ip_manager:
        return {
            "proxies": [],
            "health": {
                "healthy": 0,
                "flagged": 0,
                "blacklisted": 0
            }
        }
    
    proxy_stats = ip_manager.get_proxy_stats()
    healthy_count = ip_manager.get_healthy_count()
    flagged_count = ip_manager.get_flagged_count()
    blacklisted_count = ip_manager.get_blacklisted_count()
    
    return {
        "proxies": proxy_stats,
        "health": {
            "healthy": healthy_count,
            "flagged": flagged_count,
            "blacklisted": blacklisted_count
        }
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    websocket_connections.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"type": "pong", "data": data})
    except WebSocketDisconnect:
        websocket_connections.remove(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
