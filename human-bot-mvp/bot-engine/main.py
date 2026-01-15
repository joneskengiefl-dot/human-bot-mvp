"""
Main Entry Point - Bot Engine
"""

import asyncio
import argparse
import yaml
from pathlib import Path
from datetime import datetime

from core.simulator import Simulator
from core.behavior import BehaviorPattern, BehaviorConfig
from core.device import DeviceManager
from ip_rotation.manager import IPManager
from ip_rotation.strategy import RotationStrategy
from event_logging.logger import EventLogger
from event_logging.database import DatabaseLogger
# MVP: AI-ready modules are stub-only, not used in execution
# from ai_ready.patterns import TrafficPatternAnalyzer
# from ai_ready.feedback import FeedbackLoop


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file"""
    config_file = Path(config_path)
    if not config_file.exists():
        print(f"Config file {config_path} not found, using defaults")
        return {}
    
    with open(config_file, 'r') as f:
        return yaml.safe_load(f) or {}


async def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Human B.O.T Engine")
    parser.add_argument("--config", default="config.yaml", help="Config file path")
    parser.add_argument("--sessions", type=int, default=5, help="Number of sessions to run")
    parser.add_argument("--query", help="Search query")
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Initialize components
    event_logger = EventLogger(
        log_file=config.get("logging", {}).get("file", "logs/human_bot.log"),
        log_format=config.get("logging", {}).get("format", "json"),
        log_level=config.get("logging", {}).get("level", "INFO")
    )
    
    db_logger = DatabaseLogger(
        db_path=config.get("database", {}).get("url", "data/human_bot.db")
    )
    
    # Initialize IP manager
    # MVP: If no proxies configured, create mock IP pool for demonstration
    proxies = config.get("proxy", {}).get("proxies", [])
    ip_manager = IPManager(proxies=proxies, use_mock_ips=True)  # Creates mock IPs if no proxies provided
    rotation_strategy = RotationStrategy(
        ip_manager,
        strategy=config.get("proxy", {}).get("rotation_strategy", "round_robin")
    )
    
    # MVP: AI-ready modules are stub-only, not initialized
    # Future: pattern_analyzer = TrafficPatternAnalyzer()
    # Future: feedback_loop = FeedbackLoop()
    
    # Initialize behavior pattern
    behavior_config = config.get("behavior", {})
    behavior_pattern = BehaviorPattern(
        config=BehaviorConfig(
            click_probability=behavior_config.get("click_probability", 0.7),
            scroll_probability=behavior_config.get("scroll_probability", 0.5),
            scroll_depth_min=behavior_config.get("scroll_depth", {}).get("min", 20),
            scroll_depth_max=behavior_config.get("scroll_depth", {}).get("max", 80),
            dwell_time_min=behavior_config.get("dwell_time", {}).get("min", 2.0),
            dwell_time_max=behavior_config.get("dwell_time", {}).get("max", 10.0),
            click_delay_min=behavior_config.get("click_delay", {}).get("min", 0.5),
            click_delay_max=behavior_config.get("click_delay", {}).get("max", 2.0)
        ),
        search_queries=behavior_config.get("search_queries")
    )
    
    # Initialize device manager
    device_configs = config.get("devices", [])
    device_profiles = None  # Will use defaults if None
    if device_configs:
        from core.device import DeviceProfile
        device_profiles = [
            DeviceProfile(
                name=d.get("name"),
                user_agent=d.get("user_agent"),
                viewport_width=d.get("viewport_width"),
                viewport_height=d.get("viewport_height"),
                device_type=d.get("device_type")
            )
            for d in device_configs
        ]
    device_manager = DeviceManager(profiles=device_profiles)
    
    # Event callback
    def event_callback(event):
        event_logger.log_event(event["type"], event["data"])
        if event["type"] in ["session_start", "session_end", "click", "error"]:
            db_logger.save_event(
                event["data"].get("session_id", ""),
                event["type"],
                event["data"],
                event.get("timestamp")
            )
    
    # Initialize simulator
    simulator = Simulator(
        behavior_pattern=behavior_pattern,
        device_manager=device_manager,
        event_callback=event_callback
    )
    
    await simulator.initialize()
    
    print(f"Starting {args.sessions} session(s)...")
    
    # Run sessions
    for i in range(args.sessions):
        # Get proxy if available (None if no proxies configured)
        proxy = rotation_strategy.get_next_proxy() if rotation_strategy else None
        
        try:
            session = await simulator.simulate_search_session(
                search_query=args.query,
                proxy=proxy
            )
            
            # Save session to database
            # Calculate duration from session_end event if available, otherwise calculate it
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
            
            if proxy:
                rotation_strategy.record_success(proxy)
            
            print(f"Session {i+1}/{args.sessions} completed")
        except Exception as e:
            if proxy:
                rotation_strategy.record_failure(proxy)
            event_logger.log_error(None, str(e))
            print(f"Session {i+1}/{args.sessions} failed: {e}")
    
    # Get statistics
    stats = db_logger.get_statistics()
    print(f"\nStatistics:")
    print(f"Total sessions: {stats['total_sessions']}")
    print(f"Successful: {stats['successful_sessions']}")
    print(f"Failed: {stats['failed_sessions']}")
    print(f"Success rate: {stats['success_rate']:.2%}")
    
    await simulator.close()


if __name__ == "__main__":
    asyncio.run(main())
