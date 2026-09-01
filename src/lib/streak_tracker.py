"""
Streak Tracker for EcoBuddy AI
Tracks user streaks, milestones, and rewards for consistent challenge completion.
"""

from datetime import datetime, timedelta, date
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class StreakData:
    """Data class for streak information."""
    current_streak: int = 0
    best_streak: int = 0
    last_activity_date: Optional[date] = None
    streak_start_date: Optional[date] = None
    total_days_active: int = 0
    milestones_reached: List[int] = field(default_factory=list)
    rewards_earned: List[Dict[str, Any]] = field(default_factory=list)
    current_tier: str = "bronze"
    next_milestone: int = 7


class StreakTracker:
    """
    Tracks user streaks for eco-challenge completion.
    """

    MILESTONES = {
        7: {"name": "Week Warrior", "points": 50, "badge": "🔥"},
        14: {"name": "Two Week Champion", "points": 100, "badge": "⭐"},
        30: {"name": "Month Master", "points": 200, "badge": "🏆"},
        60: {"name": "Two Month Legend", "points": 400, "badge": "👑"},
        100: {"name": "Century Club", "points": 800, "badge": "💎"},
        200: {"name": "Sustainability Sage", "points": 1500, "badge": "🌟"},
        365: {"name": "Year of Green", "points": 3000, "badge": "🌿"}
    }

    TIERS = {
        "bronze": {"min_streak": 0, "icon": "🥉", "color": "#cd7f32"},
        "silver": {"min_streak": 7, "icon": "🥈", "color": "#c0c0c0"},
        "gold": {"min_streak": 30, "icon": "🥇", "color": "#ffd700"},
        "platinum": {"min_streak": 60, "icon": "💎", "color": "#e5e4e2"},
        "diamond": {"min_streak": 100, "icon": "💠", "color": "#b9f2ff"},
        "legendary": {"min_streak": 200, "icon": "👑", "color": "#ff6b6b"},
        "mythic": {"min_streak": 365, "icon": "🌟", "color": "#8b5cf6"}
    }

    def __init__(self, user_id: str = None):
        self.user_id = user_id
        self._streak_data: Dict[str, StreakData] = {}
        self._user_data: Dict[str, Any] = {}
        self._load_data()

    def _load_data(self):
        """Load streak data from storage."""
        # In production, this would load from database
        if self.user_id and self.user_id not in self._streak_data:
            self._streak_data[self.user_id] = StreakData()
            self._streak_data[self.user_id].next_milestone = 7

    def update_streak(self, completed_today: bool = True) -> Dict[str, Any]:
        """
        Update user streak based on daily activity.
        
        Args:
            completed_today: Whether the user completed a challenge today
        
        Returns:
            Dictionary with streak information
        """
        if not self.user_id:
            return {'error': 'No user ID provided'}

        self._ensure_user_data()
        streak = self._streak_data[self.user_id]
        today = date.today()

        if completed_today:
            # Check if already logged today
            if streak.last_activity_date == today:
                return self.get_streak_info()

            # Check if consecutive day
            if streak.last_activity_date == today - timedelta(days=1):
                streak.current_streak += 1
            else:
                # Reset streak if gap
                streak.current_streak = 1
                streak.streak_start_date = today

            streak.last_activity_date = today
            streak.total_days_active += 1

            # Update best streak
            if streak.current_streak > streak.best_streak:
                streak.best_streak = streak.current_streak

            # Check milestones
            milestone_reached = self._check_milestones(streak)

            # Update tier
            streak.current_tier = self._get_tier(streak.current_streak)

            # Update next milestone
            streak.next_milestone = self._get_next_milestone(streak.current_streak)

            self._save_data()

            return {
                'success': True,
                'streak': streak.current_streak,
                'best_streak': streak.best_streak,
                'tier': streak.current_tier,
                'milestone_reached': milestone_reached,
                'next_milestone': streak.next_milestone,
                'message': self._get_streak_message(streak.current_streak)
            }
        else:
            return {
                'success': False,
                'message': 'No challenge completed today',
                'streak': streak.current_streak
            }

    def _check_milestones(self, streak: StreakData) -> Optional[Dict[str, Any]]:
        """Check if a milestone is reached."""
        for milestone, reward in self.MILESTONES.items():
            if (streak.current_streak == milestone and 
                milestone not in streak.milestones_reached):
                streak.milestones_reached.append(milestone)
                streak.rewards_earned.append({
                    'milestone': milestone,
                    'reward': reward,
                    'date': date.today().isoformat()
                })
                return {
                    'milestone': milestone,
                    'name': reward['name'],
                    'points': reward['points'],
                    'badge': reward['badge']
                }
        return None

    def _get_tier(self, streak: int) -> str:
        """Get tier based on streak length."""
        if streak >= 365:
            return "mythic"
        elif streak >= 200:
            return "legendary"
        elif streak >= 100:
            return "diamond"
        elif streak >= 60:
            return "platinum"
        elif streak >= 30:
            return "gold"
        elif streak >= 7:
            return "silver"
        else:
            return "bronze"

    def _get_next_milestone(self, streak: int) -> int:
        """Get the next milestone based on current streak."""
        milestones = sorted(self.MILESTONES.keys())
        for milestone in milestones:
            if milestone > streak:
                return milestone
        return max(milestones) + 100

    def _get_streak_message(self, streak: int) -> str:
        """Get a motivational message based on streak."""
        if streak == 0:
            return "Start your eco-journey today! 🌱"
        elif streak < 3:
            return "Great start! Keep it going! 💪"
        elif streak < 7:
            return "You're building a habit! 🌟"
        elif streak < 14:
            return "Week streak achieved! 🔥"
        elif streak < 30:
            return "You're a sustainability warrior! 💚"
        elif streak < 60:
            return "Month master! Incredible dedication! 🏆"
        elif streak < 100:
            return "Two months of green living! Amazing! 🌿"
        elif streak < 200:
            return "Century club! You're an inspiration! ⭐"
        elif streak < 365:
            return "Legendary sustainability champion! 👑"
        else:
            return "Year of green! You're a true eco-legend! 🌟"

    def get_streak_info(self) -> Dict[str, Any]:
        """Get current streak information."""
        self._ensure_user_data()
        streak = self._streak_data[self.user_id]

        return {
            'current_streak': streak.current_streak,
            'best_streak': streak.best_streak,
            'tier': streak.current_tier,
            'tier_info': self.TIERS.get(streak.current_tier, {}),
            'next_milestone': streak.next_milestone,
            'next_milestone_info': self.MILESTONES.get(streak.next_milestone, {}),
            'milestones_reached': streak.milestones_reached,
            'total_days_active': streak.total_days_active,
            'rewards_earned': streak.rewards_earned,
            'streak_start_date': streak.streak_start_date.isoformat() if streak.streak_start_date else None,
            'last_activity_date': streak.last_activity_date.isoformat() if streak.last_activity_date else None
        }

    def get_milestones_progress(self) -> List[Dict[str, Any]]:
        """Get progress towards all milestones."""
        self._ensure_user_data()
        streak = self._streak_data[self.user_id]
        progress = []

        for milestone, info in sorted(self.MILESTONES.items()):
            achieved = milestone in streak.milestones_reached
            progress.append({
                'milestone': milestone,
                'name': info['name'],
                'points': info['points'],
                'badge': info['badge'],
                'achieved': achieved,
                'progress': min(100, (streak.current_streak / milestone) * 100) if not achieved else 100
            })

        return progress

    def get_tier_progress(self) -> Dict[str, Any]:
        """Get progress through current tier."""
        self._ensure_user_data()
        streak = self._streak_data[self.user_id]
        tier = streak.current_tier
        
        # Find next tier
        tier_order = ['bronze', 'silver', 'gold', 'platinum', 'diamond', 'legendary', 'mythic']
        current_index = tier_order.index(tier) if tier in tier_order else 0
        
        if current_index < len(tier_order) - 1:
            next_tier = tier_order[current_index + 1]
            next_threshold = self.TIERS[next_tier]['min_streak']
            current_threshold = self.TIERS[tier]['min_streak']
            
            progress = ((streak.current_streak - current_threshold) / 
                       (next_threshold - current_threshold)) * 100 if next_threshold > current_threshold else 100
            
            return {
                'current_tier': tier,
                'current_tier_info': self.TIERS[tier],
                'next_tier': next_tier,
                'next_tier_info': self.TIERS[next_tier],
                'progress': min(100, progress),
                'streaks_needed': next_threshold - streak.current_streak
            }
        else:
            return {
                'current_tier': tier,
                'current_tier_info': self.TIERS[tier],
                'next_tier': None,
                'progress': 100,
                'streaks_needed': 0
            }

    def reset_streak(self) -> Dict[str, Any]:
        """Reset the current streak."""
        self._ensure_user_data()
        streak = self._streak_data[self.user_id]
        
        # Save best streak before reset
        best = streak.best_streak
        
        streak.current_streak = 0
        streak.streak_start_date = None
        streak.current_tier = "bronze"
        streak.next_milestone = 7
        
        self._save_data()
        
        return {
            'success': True,
            'message': 'Streak reset',
            'previous_best': best,
            'new_streak': 0
        }

    def _ensure_user_data(self):
        """Ensure user data exists."""
        if self.user_id and self.user_id not in self._streak_data:
            self._streak_data[self.user_id] = StreakData()
            self._streak_data[self.user_id].next_milestone = 7

    def _save_data(self):
        """Save streak data to storage."""
        # In production, this would save to database
        pass