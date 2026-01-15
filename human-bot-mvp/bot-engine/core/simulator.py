"""
Core Simulator - Main simulation engine using Playwright
"""

import asyncio
import random
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, Callable
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

from .behavior import BehaviorPattern
from .device import DeviceManager, DeviceProfile


class Simulator:
    """
    Main simulation engine for human-like web traffic
    
    This class orchestrates browser sessions, simulates user behavior,
    and manages device profiles.
    """
    
    def __init__(
        self,
        behavior_pattern: Optional[BehaviorPattern] = None,
        device_manager: Optional[DeviceManager] = None,
        event_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ):
        """
        Initialize simulator
        
        Args:
            behavior_pattern: Behavior pattern generator
            device_manager: Device profile manager
            event_callback: Callback function for events
        """
        self.behavior = behavior_pattern or BehaviorPattern()
        self.devices = device_manager or DeviceManager()
        self.event_callback = event_callback
        
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
    
    async def initialize(self) -> None:
        """Initialize Playwright browser"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )
    
    async def close(self) -> None:
        """Close browser and cleanup"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    def _emit_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Emit event to callback"""
        if self.event_callback:
            event = {
                "type": event_type,
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }
            self.event_callback(event)
    
    async def _inject_stealth(self, page: Page) -> None:
        """Inject stealth scripts to avoid detection"""
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) =>
                parameters.name === 'notifications'
                    ? Promise.resolve({ state: Notification.permission })
                    : originalQuery(parameters);
        """)
    
    async def create_session(
        self,
        session_id: Optional[str] = None,
        target_url: str = None,
        proxy: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new browser session
        
        Args:
            session_id: Optional session ID. If None, generates UUID.
            target_url: Target URL to navigate to
            proxy: Optional proxy server URL
            
        Returns:
            Session information dictionary
        """
        if not session_id:
            session_id = str(uuid.uuid4())
        
        device = self.devices.get_random_device()
        
        context_options = {
            "user_agent": device.user_agent,
            "viewport": {
                "width": device.viewport_width,
                "height": device.viewport_height
            },
            "device_scale_factor": 1 if device.device_type == "desktop" else 2,
            "is_mobile": device.is_mobile,
            "has_touch": device.has_touch
        }
        
        # MVP: Only use proxy if it's a real proxy URL (not a mock IP identifier)
        # Mock IPs are used for rotation/scoring demonstration but don't affect browser context
        if proxy and proxy.startswith("http"):
            context_options["proxy"] = {"server": proxy}
        
        context: BrowserContext = await self.browser.new_context(**context_options)
        page: Page = await context.new_page()
        
        # Inject stealth scripts
        await self._inject_stealth(page)
        
        session_info = {
            "session_id": session_id,
            "device": device.name,
            "context": context,
            "page": page,
            "start_time": datetime.utcnow(),
            "target_url": target_url,
            "proxy": proxy,
            "events": []
        }
        
        self.active_sessions[session_id] = session_info
        
        self._emit_event("session_start", {
            "session_id": session_id,
            "device": device.name,
            "target_url": target_url,
            "proxy": proxy
        })
        
        return session_info
    
    async def simulate_search_session(
        self,
        session_id: Optional[str] = None,
        search_query: Optional[str] = None,
        proxy: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Simulate a search session
        
        Args:
            session_id: Optional session ID
            search_query: Optional search query. If None, uses random query.
            proxy: Optional proxy server URL
            
        Returns:
            Session information dictionary
        """
        if not search_query:
            search_query = self.behavior.get_random_search_query()
        
        target_url = f"https://www.google.com/search?q={search_query}"
        session = await self.create_session(session_id, target_url, proxy)
        page = session["page"]
        
        try:
            # Navigate to search page
            await page.goto(target_url, wait_until="networkidle")
            
            # Simulate dwell time
            dwell_time = self.behavior.get_dwell_time()
            await asyncio.sleep(dwell_time)
            
            # Simulate scrolling
            if self.behavior.should_scroll():
                scroll_depth = self.behavior.get_scroll_depth()
                await page.evaluate(
                    f"window.scrollTo(0, document.body.scrollHeight * {scroll_depth} / 100)"
                )
                await asyncio.sleep(0.5 + random.random())
            
            # Simulate click on search result
            if self.behavior.should_click():
                click_delay = self.behavior.get_click_delay()
                await asyncio.sleep(click_delay)
                
                # Find search result links
                links = await page.query_selector_all('a[href^="http"]')
                result_links = []
                
                for link in links:
                    href = await link.get_attribute('href')
                    if href and 'google.com' not in href:
                        result_links.append({"element": link, "href": href})
                
                if result_links:
                    link_to_click = result_links[random.randint(0, min(4, len(result_links) - 1))]
                    
                    if link_to_click["href"]:
                        await link_to_click["element"].click()
                        await page.wait_for_load_state("networkidle")
                        
                        self._emit_event("click", {
                            "session_id": session["session_id"],
                            "url": link_to_click["href"]
                        })
                        
                        # Dwell on clicked page
                        await asyncio.sleep(self.behavior.get_dwell_time())
            
            session["events"].append({
                "type": "session_end",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {"success": True}
            })
            
        except Exception as e:
            session["events"].append({
                "type": "error",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {"error": str(e)}
            })
            self._emit_event("error", {
                "session_id": session["session_id"],
                "error": str(e)
            })
        finally:
            await session["context"].close()
            if session["session_id"] in self.active_sessions:
                del self.active_sessions[session["session_id"]]
            
            duration = (datetime.utcnow() - session["start_time"]).total_seconds()
            self._emit_event("session_end", {
                "session_id": session["session_id"],
                "success": session["events"][-1]["data"].get("success", True) if session["events"] else True,
                "duration": duration
            })
        
        return session
    
    async def close_session(self, session_id: str) -> None:
        """Close a specific session"""
        session = self.active_sessions.get(session_id)
        if session:
            await session["context"].close()
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
    
    def get_active_sessions(self) -> Dict[str, Any]:
        """Get all active sessions"""
        return {
            sid: {
                "device": info["device"],
                "start_time": info["start_time"].isoformat(),
                "target_url": info["target_url"]
            }
            for sid, info in self.active_sessions.items()
        }
