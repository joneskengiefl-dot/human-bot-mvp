"""
Rotation Strategy - IP rotation strategies
"""

from typing import Optional
from .manager import IPManager


class RotationStrategy:
    """
    IP rotation strategy implementation
    
    This class provides different rotation strategies for IP selection.
    """
    
    def __init__(self, ip_manager: IPManager, strategy: str = "round_robin"):
        """
        Initialize rotation strategy
        
        Args:
            ip_manager: IP manager instance
            strategy: Rotation strategy ("round_robin", "random", "least_used")
        """
        self.ip_manager = ip_manager
        self.strategy = strategy
        self.current_proxy: Optional[str] = None
    
    def get_next_proxy(self) -> Optional[str]:
        """
        Get next proxy based on strategy
        
        Returns:
            Proxy URL or None
        """
        self.current_proxy = self.ip_manager.get_proxy(self.strategy)
        return self.current_proxy
    
    def record_success(self, proxy_url: str) -> None:
        """
        Record successful proxy use
        
        Args:
            proxy_url: Proxy URL
        """
        self.ip_manager.record_use(proxy_url, success=True)
    
    def record_failure(self, proxy_url: str) -> None:
        """
        Record failed proxy use
        
        Args:
            proxy_url: Proxy URL
        """
        self.ip_manager.record_use(proxy_url, success=False)
    
    def set_strategy(self, strategy: str) -> None:
        """
        Change rotation strategy
        
        Args:
            strategy: New strategy ("round_robin", "random", "least_used")
        """
        self.strategy = strategy
