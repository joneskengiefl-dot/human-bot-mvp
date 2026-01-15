"""
Event Logger - Capture and log events
"""

import json
import os
from typing import Optional, Dict, Any
from datetime import datetime


class EventLogger:
    """
    Event logger for capturing bot events
    
    This class handles:
    - Event logging to console
    - Event logging to file
    - Structured event format
    """
    
    def __init__(
        self,
        log_file: Optional[str] = None,
        log_format: str = "json",
        log_level: str = "INFO"
    ):
        """
        Initialize event logger
        
        Args:
            log_file: Optional log file path
            log_format: Log format ("json" or "text")
            log_level: Log level ("DEBUG", "INFO", "WARNING", "ERROR")
        """
        self.log_format = log_format
        self.log_file = log_file
        self.log_level = log_level
        
        # Create logs directory if needed
        if log_file:
            log_path = os.path.dirname(log_file)
            if log_path and not os.path.exists(log_path):
                os.makedirs(log_path, exist_ok=True)
    
    def _should_log(self, level: str) -> bool:
        """Check if level should be logged"""
        levels = {
            "DEBUG": 0,
            "INFO": 1,
            "WARNING": 2,
            "ERROR": 3
        }
        return levels.get(level, 1) >= levels.get(self.log_level, 1)
    
    def _write_log(self, message: str) -> None:
        """Write log message"""
        # Console output
        print(message)
        
        # File output
        if self.log_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(message + '\n')
    
    def log_event(self, event_type: str, data: Dict[str, Any], level: str = "INFO") -> None:
        """
        Log an event
        
        Args:
            event_type: Event type
            data: Event data
            level: Log level
        """
        if not self._should_log(level):
            return
        
        event = {
            "type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
            "level": level
        }
        
        if self.log_format == "json":
            self._write_log(json.dumps(event))
        else:
            self._write_log(f"[{level}] {event_type}: {json.dumps(data)}")
    
    def log_session_start(
        self,
        session_id: str,
        device: str,
        target_url: str,
        proxy: Optional[str] = None
    ) -> None:
        """Log session start"""
        self.log_event("session_start", {
            "session_id": session_id,
            "device": device,
            "target_url": target_url,
            "proxy": proxy
        })
    
    def log_session_end(
        self,
        session_id: str,
        success: bool,
        duration: float
    ) -> None:
        """Log session end"""
        self.log_event("session_end", {
            "session_id": session_id,
            "success": success,
            "duration": duration
        })
    
    def log_click(self, session_id: str, url: str) -> None:
        """Log click event"""
        self.log_event("click", {
            "session_id": session_id,
            "url": url
        })
    
    def log_scroll(self, session_id: str, depth: int) -> None:
        """Log scroll event"""
        self.log_event("scroll", {
            "session_id": session_id,
            "depth": depth
        })
    
    def log_ip_rotation(self, old_ip: Optional[str], new_ip: str) -> None:
        """Log IP rotation"""
        self.log_event("ip_rotation", {
            "old_ip": old_ip,
            "new_ip": new_ip
        })
    
    def log_error(self, session_id: Optional[str], error: str) -> None:
        """Log error"""
        self.log_event("error", {
            "session_id": session_id,
            "error": error
        }, level="ERROR")
