"""
Device Profiles - Simulate different devices and browsers
"""

from dataclasses import dataclass
from typing import List
import random


@dataclass
class DeviceProfile:
    """Device profile configuration"""
    name: str
    user_agent: str
    viewport_width: int
    viewport_height: int
    device_type: str  # "desktop", "mobile", "tablet"
    is_mobile: bool = False
    has_touch: bool = False

    def __post_init__(self):
        """Set mobile and touch based on device type"""
        self.is_mobile = self.device_type in ["mobile", "tablet"]
        self.has_touch = self.device_type != "desktop"


class DeviceManager:
    """Manage device profiles"""
    
    def __init__(self, profiles: List[DeviceProfile] = None):
        """
        Initialize device manager
        
        Args:
            profiles: Custom device profiles. If None, uses default profiles.
        """
        if profiles:
            self.profiles = profiles
        else:
            self.profiles = self._get_default_profiles()
    
    def _get_default_profiles(self) -> List[DeviceProfile]:
        """Get default device profiles"""
        return [
            DeviceProfile(
                name="Desktop Chrome",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport_width=1920,
                viewport_height=1080,
                device_type="desktop"
            ),
            DeviceProfile(
                name="Desktop Firefox",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
                viewport_width=1920,
                viewport_height=1080,
                device_type="desktop"
            ),
            DeviceProfile(
                name="Mobile Chrome",
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                viewport_width=375,
                viewport_height=667,
                device_type="mobile"
            ),
            DeviceProfile(
                name="Mobile Safari",
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                viewport_width=390,
                viewport_height=844,
                device_type="mobile"
            ),
            DeviceProfile(
                name="Tablet iPad",
                user_agent="Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                viewport_width=768,
                viewport_height=1024,
                device_type="tablet"
            )
        ]
    
    def get_random_device(self) -> DeviceProfile:
        """Get a random device profile"""
        return random.choice(self.profiles)
    
    def get_device_by_name(self, name: str) -> DeviceProfile:
        """Get device profile by name"""
        for profile in self.profiles:
            if profile.name == name:
                return profile
        raise ValueError(f"Device profile '{name}' not found")
    
    def get_all_devices(self) -> List[DeviceProfile]:
        """Get all device profiles"""
        return self.profiles.copy()
