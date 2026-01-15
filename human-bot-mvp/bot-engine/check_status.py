#!/usr/bin/env python3
"""
Quick diagnostic script to check API server and database status
"""

import sqlite3
from pathlib import Path

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False
    print("⚠️  httpx not available, API check will be skipped")

def check_database():
    """Check if database exists and has data"""
    db_path = Path("data/human_bot.db")
    
    print("=" * 60)
    print("DATABASE CHECK")
    print("=" * 60)
    
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        print(f"   Expected location: {db_path.absolute()}")
        return False
    
    print(f"✅ Database exists: {db_path.absolute()}")
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check sessions count
        cursor.execute("SELECT COUNT(*) FROM sessions")
        session_count = cursor.fetchone()[0]
        
        # Check events count
        cursor.execute("SELECT COUNT(*) FROM events")
        event_count = cursor.fetchone()[0]
        
        # Get recent sessions
        cursor.execute("SELECT id, device, start_time FROM sessions ORDER BY start_time DESC LIMIT 5")
        recent_sessions = cursor.fetchall()
        
        conn.close()
        
        print(f"   Sessions in database: {session_count}")
        print(f"   Events in database: {event_count}")
        
        if session_count > 0:
            print(f"\n   Recent sessions:")
            for sid, device, start_time in recent_sessions:
                print(f"     - {sid[:8]}... | {device} | {start_time}")
        else:
            print(f"\n   ⚠️  No sessions in database!")
            print(f"   You need to run sessions first:")
            print(f"     python demo_100_sessions.py")
            print(f"     or")
            print(f"     python main.py --sessions 10")
        
        return session_count > 0
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")
        return False


def check_api_server():
    """Check if API server is running and responding"""
    print("\n" + "=" * 60)
    print("API SERVER CHECK")
    print("=" * 60)
    
    if not HAS_HTTPX:
        print("⚠️  Cannot check API server (httpx not available)")
        return False
    
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get("http://localhost:8000/api/health")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ API server is running")
                print(f"   Status: {data.get('status')}")
                print(f"   Active sessions: {data.get('active_sessions', 0)}")
                print(f"   Total sessions in DB: {data.get('total_sessions_in_db', 0)}")
                print(f"   Database path: {data.get('database_path', 'unknown')}")
                
                # Check stats endpoint
                try:
                    stats_response = client.get("http://localhost:8000/api/stats", timeout=5.0)
                    if stats_response.status_code == 200:
                        stats = stats_response.json()
                        print(f"\n   Statistics:")
                        print(f"     Total sessions: {stats.get('total_sessions', 0)}")
                        print(f"     Successful: {stats.get('successful_sessions', 0)}")
                        print(f"     Failed: {stats.get('failed_sessions', 0)}")
                        print(f"     Total clicks: {stats.get('total_clicks', 0)}")
                except Exception as e:
                    print(f"   ⚠️  Could not get stats: {e}")
                
                return True
            else:
                print(f"❌ API server returned status {response.status_code}")
                return False
                
    except httpx.ConnectError:
        print("❌ API server is not running!")
        print("   Start it with: python -m api.server")
        print("   Or: .\\run-api.bat")
        return False
    except Exception as e:
        print(f"❌ Error checking API server: {e}")
        return False


def main():
    print("\n🔍 Human B.O.T MVP - Diagnostic Check\n")
    
    db_ok = check_database()
    api_ok = check_api_server()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if not api_ok:
        print("❌ API server is not running")
        print("   Fix: Start API server first")
    elif not db_ok:
        print("⚠️  API server is running but database is empty")
        print("   Fix: Run sessions to generate data")
        print("   Command: python demo_100_sessions.py")
    else:
        print("✅ Everything looks good!")
        print("   If dashboard still shows no data, try:")
        print("   1. Refresh the browser")
        print("   2. Check browser console (F12) for errors")
        print("   3. Verify dashboard is connecting to http://localhost:8000")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
