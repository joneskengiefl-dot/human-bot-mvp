"""
IP Manager - Manage IP pool and rotation
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class IPStatus(Enum):
    """IP status enumeration"""
    HEALTHY = "healthy"
    FLAGGED = "flagged"
    BLACKLISTED = "blacklisted"


@dataclass
class IPInfo:
    """IP information and statistics"""
    url: str
    uses: int = 0
    successes: int = 0
    failures: int = 0
    last_used: Optional[str] = None
    status: IPStatus = IPStatus.HEALTHY
    enabled: bool = True


class IPManager:
    """
    Manage IP pool and rotation
    
    This class handles:
    - IP pool management
    - Usage tracking
    - Health monitoring
    - Status management
    """
    
    def __init__(self, proxies: Optional[List[str]] = None, use_mock_ips: bool = True):
        """
        Initialize IP manager
        
        Args:
            proxies: List of proxy URLs (format: http://host:port or http://user:pass@host:port)
            use_mock_ips: If True and no proxies provided, create mock IP pool for MVP demo
        """
        self.proxies: List[IPInfo] = []
        if proxies:
            for proxy_url in proxies:
                self.add_proxy(proxy_url)
        elif use_mock_ips:
            # MVP: Create mock IP pool for demonstration when no real proxies configured
            # This allows IP rotation and scoring logic to be demonstrated without real proxies
            mock_ips = [
                "mock-ip-001",
                "mock-ip-002", 
                "mock-ip-003",
                "mock-ip-004",
                "mock-ip-005"
            ]
            for mock_ip in mock_ips:
                self.add_proxy(mock_ip)
    
    def add_proxy(self, proxy_url: str) -> None:
        """
        Add a proxy to the pool
        
        Args:
            proxy_url: Proxy URL
        """
        proxy_info = IPInfo(url=proxy_url)
        self.proxies.append(proxy_info)
    
    def remove_proxy(self, proxy_url: str) -> None:
        """
        Remove a proxy from the pool
        
        Args:
            proxy_url: Proxy URL to remove
        """
        self.proxies = [p for p in self.proxies if p.url != proxy_url]
    
    def get_proxy(self, strategy: str = "round_robin") -> Optional[str]:
        """
        Get next proxy based on rotation strategy
        
        Args:
            strategy: Rotation strategy ("round_robin", "random", "least_used")
            
        Returns:
            Proxy URL/identifier or None if no enabled proxies
            Note: Returns mock IP identifiers (e.g., "mock-ip-001") for MVP demo when no real proxies
        """
        enabled_proxies = [p for p in self.proxies if p.enabled and p.status != IPStatus.BLACKLISTED]
        
        if not enabled_proxies:
            return None
        
        if strategy == "round_robin" or strategy == "least_used":
            proxy = min(enabled_proxies, key=lambda p: p.uses)
        elif strategy == "random":
            import random
            proxy = random.choice(enabled_proxies)
        else:
            proxy = enabled_proxies[0]
        
        return proxy.url
    
    def record_use(self, proxy_url: str, success: bool = True) -> None:
        """
        Record proxy usage
        
        Args:
            proxy_url: Proxy URL
            success: Whether the use was successful
        """
        proxy = next((p for p in self.proxies if p.url == proxy_url), None)
        if proxy:
            proxy.uses += 1
            if success:
                proxy.successes += 1
            else:
                proxy.failures += 1
                # Auto-flag after multiple failures
                if proxy.failures >= 3:
                    proxy.status = IPStatus.FLAGGED
                if proxy.failures >= 5:
                    proxy.status = IPStatus.BLACKLISTED
            proxy.last_used = datetime.utcnow().isoformat()
    
    def get_ip_status(self, proxy_url: str) -> IPStatus:
        """
        Get IP status
        
        Args:
            proxy_url: Proxy URL
            
        Returns:
            IP status
        """
        proxy = next((p for p in self.proxies if p.url == proxy_url), None)
        if proxy:
            return proxy.status
        return IPStatus.BLACKLISTED
    
    def set_ip_status(self, proxy_url: str, status: IPStatus) -> None:
        """
        Set IP status
        
        Args:
            proxy_url: Proxy URL
            status: New status
        """
        proxy = next((p for p in self.proxies if p.url == proxy_url), None)
        if proxy:
            proxy.status = status
    
    def disable_proxy(self, proxy_url: str) -> None:
        """Disable a proxy"""
        proxy = next((p for p in self.proxies if p.url == proxy_url), None)
        if proxy:
            proxy.enabled = False
    
    def enable_proxy(self, proxy_url: str) -> None:
        """Enable a proxy"""
        proxy = next((p for p in self.proxies if p.url == proxy_url), None)
        if proxy:
            proxy.enabled = True
    
    def get_proxy_stats(self) -> List[dict]:
        """
        Get statistics for all proxies
        
        Returns:
            List of proxy statistics dictionaries
        """
        stats = []
        for proxy in self.proxies:
            success_rate = proxy.successes / proxy.uses if proxy.uses > 0 else 0.0
            stats.append({
                "url": proxy.url,
                "uses": proxy.uses,
                "successes": proxy.successes,
                "failures": proxy.failures,
                "success_rate": success_rate,
                "status": proxy.status.value,
                "enabled": proxy.enabled,
                "last_used": proxy.last_used
            })
        return stats
    
    def get_healthy_count(self) -> int:
        """Get count of healthy proxies"""
        return len([p for p in self.proxies if p.status == IPStatus.HEALTHY and p.enabled])
    
    def get_flagged_count(self) -> int:
        """Get count of flagged proxies"""
        return len([p for p in self.proxies if p.status == IPStatus.FLAGGED])
    
    def get_blacklisted_count(self) -> int:
        """Get count of blacklisted proxies"""
        return len([p for p in self.proxies if p.status == IPStatus.BLACKLISTED])
