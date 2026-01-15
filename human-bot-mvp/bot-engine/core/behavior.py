"""
Behavior Patterns - Define realistic human behavior
"""

import random
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class BehaviorConfig:
    """Configuration for behavior patterns"""
    click_probability: float = 0.7
    scroll_probability: float = 0.5
    scroll_depth_min: int = 20
    scroll_depth_max: int = 80
    dwell_time_min: float = 2.0
    dwell_time_max: float = 10.0
    click_delay_min: float = 0.5
    click_delay_max: float = 2.0


class BehaviorPattern:
    """
    Generate human-like behavior patterns
    
    This class simulates realistic user interactions including:
    - Click decisions
    - Scroll behavior
    - Dwell times
    - Click delays
    """
    
    def __init__(
        self,
        config: Optional[BehaviorConfig] = None,
        search_queries: Optional[List[str]] = None
    ):
        """
        Initialize behavior pattern generator
        
        Args:
            config: Behavior configuration. If None, uses defaults.
            search_queries: List of search queries. If None, uses defaults.
        """
        self.config = config or BehaviorConfig()
        self.search_queries = search_queries or [
            "python programming",
            "web development",
            "data science",
            "machine learning",
            "software engineering",
            "artificial intelligence",
            "cloud computing",
            "cybersecurity"
        ]
    
    def should_click(self) -> bool:
        """
        Determine if user should click based on probability
        
        Returns:
            True if click should occur, False otherwise
        """
        return random.random() < self.config.click_probability
    
    def should_scroll(self) -> bool:
        """
        Determine if user should scroll
        
        Returns:
            True if scroll should occur, False otherwise
        """
        return random.random() < self.config.scroll_probability
    
    def get_scroll_depth(self) -> int:
        """
        Get random scroll depth as percentage
        
        Returns:
            Scroll depth percentage (0-100)
        """
        return random.randint(
            self.config.scroll_depth_min,
            self.config.scroll_depth_max
        )
    
    def get_dwell_time(self) -> float:
        """
        Get random dwell time in seconds
        
        Returns:
            Dwell time in seconds
        """
        return random.uniform(
            self.config.dwell_time_min,
            self.config.dwell_time_max
        )
    
    def get_click_delay(self) -> float:
        """
        Get random click delay in seconds
        
        Returns:
            Click delay in seconds
        """
        return random.uniform(
            self.config.click_delay_min,
            self.config.click_delay_max
        )
    
    def get_random_search_query(self) -> str:
        """
        Get a random search query
        
        Returns:
            Random search query string
        """
        return random.choice(self.search_queries)
    
    def get_search_queries(self) -> List[str]:
        """Get all search queries"""
        return self.search_queries.copy()
    
    def set_search_queries(self, queries: List[str]) -> None:
        """Set search queries"""
        self.search_queries = queries
