"""
Database Logger - Store events in SQLite database
"""

import sqlite3
import json
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime


class DatabaseLogger:
    """
    Database logger for storing events in SQLite
    
    This class handles:
    - Event storage in SQLite
    - Session tracking
    - Query capabilities
    """
    
    def __init__(self, db_path: str = "data/human_bot.db"):
        """
        Initialize database logger
        
        Args:
            db_path: Database file path
        """
        # Create data directory if needed
        db_dir = Path(db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                device TEXT,
                target_url TEXT,
                proxy TEXT,
                start_time TEXT,
                end_time TEXT,
                duration REAL,
                success INTEGER,
                events TEXT
            )
        """)
        
        # Events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                event_type TEXT,
                timestamp TEXT,
                data TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        """)
        
        # IP usage table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ip_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proxy_url TEXT,
                session_id TEXT,
                timestamp TEXT,
                success INTEGER,
                duration REAL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_session(self, session_data: Dict[str, Any]) -> None:
        """
        Save session to database
        
        Args:
            session_data: Session data dictionary
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO sessions
            (id, device, target_url, proxy, start_time, end_time, duration, success, events)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_data.get("id"),
            session_data.get("device"),
            session_data.get("target_url"),
            session_data.get("proxy"),
            session_data.get("start_time"),
            session_data.get("end_time"),
            session_data.get("duration"),
            1 if session_data.get("success") else 0,
            json.dumps(session_data.get("events", []))
        ))
        
        conn.commit()
        conn.close()
    
    def save_event(
        self,
        session_id: str,
        event_type: str,
        data: Dict[str, Any],
        timestamp: Optional[str] = None
    ) -> None:
        """
        Save event to database
        
        Args:
            session_id: Session ID
            event_type: Event type
            data: Event data
            timestamp: Optional timestamp (defaults to now)
        """
        if not timestamp:
            timestamp = datetime.utcnow().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO events (session_id, event_type, timestamp, data)
            VALUES (?, ?, ?, ?)
        """, (session_id, event_type, timestamp, json.dumps(data)))
        
        conn.commit()
        conn.close()
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session by ID
        
        Args:
            session_id: Session ID
            
        Returns:
            Session data or None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if not row:
            return None
        
        return {
            "id": row[0],
            "device": row[1],
            "target_url": row[2],
            "proxy": row[3],
            "start_time": row[4],
            "end_time": row[5],
            "duration": row[6],
            "success": bool(row[7]),
            "events": json.loads(row[8]) if row[8] else []
        }
    
    def get_sessions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get recent sessions
        
        Args:
            limit: Maximum number of sessions to return
            
        Returns:
            List of session data dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM sessions
            ORDER BY start_time DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "device": row[1],
                "target_url": row[2],
                "proxy": row[3],
                "start_time": row[4],
                "end_time": row[5],
                "duration": row[6],
                "success": bool(row[7]),
                "events": json.loads(row[8]) if row[8] else []
            }
            for row in rows
        ]
    
    def get_events(
        self,
        session_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get events with optional filtering
        
        Args:
            session_id: Optional session ID filter
            event_type: Optional event type filter
            limit: Maximum number of events to return
            
        Returns:
            List of event data dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM events WHERE 1=1"
        params = []
        
        if session_id:
            query += " AND session_id = ?"
            params.append(session_id)
        
        if event_type:
            query += " AND event_type = ?"
            params.append(event_type)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "session_id": row[1],
                "event_type": row[2],
                "timestamp": row[3],
                "data": json.loads(row[4]) if row[4] else {}
            }
            for row in rows
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall statistics
        
        Returns:
            Statistics dictionary
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total sessions
        cursor.execute("SELECT COUNT(*) FROM sessions")
        total_sessions = cursor.fetchone()[0]
        
        # Successful sessions
        cursor.execute("SELECT COUNT(*) FROM sessions WHERE success = 1")
        successful_sessions = cursor.fetchone()[0]
        
        # Failed sessions
        cursor.execute("SELECT COUNT(*) FROM sessions WHERE success = 0")
        failed_sessions = cursor.fetchone()[0]
        
        # Total clicks
        cursor.execute("SELECT COUNT(*) FROM events WHERE event_type = 'click'")
        total_clicks = cursor.fetchone()[0]
        
        # Average duration
        cursor.execute("SELECT AVG(duration) FROM sessions WHERE duration IS NOT NULL")
        avg_duration = cursor.fetchone()[0] or 0.0
        
        conn.close()
        
        return {
            "total_sessions": total_sessions,
            "successful_sessions": successful_sessions,
            "failed_sessions": failed_sessions,
            "total_clicks": total_clicks,
            "average_duration": avg_duration,
            "success_rate": successful_sessions / total_sessions if total_sessions > 0 else 0.0
        }
