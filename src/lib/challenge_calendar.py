"""
Challenge Calendar for EcoBuddy AI
Manages the calendar view of eco-challenges with date-based tracking.
"""

import calendar
from datetime import datetime, timedelta, date
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class ChallengeDay:
    """Data class for a single day in the calendar."""
    date: date
    challenges: List[Dict[str, Any]] = field(default_factory=list)
    is_today: bool = False
    is_past: bool = False
    is_future: bool = False
    has_completed: bool = False
    completion_count: int = 0
    total_challenges: int = 0
    streak: int = 0
    points_earned: int = 0
    badges: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_completion_percentage(self) -> float:
        """Get completion percentage for the day."""
        if self.total_challenges == 0:
            return 0.0
        return (self.completion_count / self.total_challenges) * 100

    def is_completed(self) -> bool:
        """Check if all challenges for the day are completed."""
        return self.completion_count >= self.total_challenges and self.total_challenges > 0


@dataclass
class ChallengeMonth:
    """Data class for a month in the calendar."""
    year: int
    month: int
    days: List[ChallengeDay] = field(default_factory=list)
    total_challenges: int = 0
    completed_challenges: int = 0
    total_points: int = 0
    earned_points: int = 0
    badges_earned: List[str] = field(default_factory=list)
    streak: int = 0
    best_streak: int = 0

    def get_completion_rate(self) -> float:
        """Get completion rate for the month."""
        if self.total_challenges == 0:
            return 0.0
        return (self.completed_challenges / self.total_challenges) * 100


class ChallengeCalendar:
    """
    Manages the eco-challenge calendar with date-based tracking.
    """

    def __init__(self, user_id: str = None):
        self.user_id = user_id
        self._challenges: Dict[str, Dict[str, Any]] = {}
        self._user_progress: Dict[str, Dict[str, Any]] = {}
        self._streak_data: Dict[str, Any] = {}
        self._load_data()

    def _load_data(self):
        """Load challenge data from storage."""
        # In production, this would load from database
        pass

    def get_month(self, year: int, month: int) -> ChallengeMonth:
        """
        Get challenge data for a specific month.
        
        Args:
            year: Year
            month: Month (1-12)
        
        Returns:
            ChallengeMonth object
        """
        # Get calendar data
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(year, month)
        
        # Create challenge days
        challenge_days = []
        total_challenges = 0
        completed_challenges = 0
        total_points = 0
        earned_points = 0
        month_streak = 0
        best_streak = 0
        
        for week in month_days:
            for day in week:
                if day == 0:
                    continue
                
                current_date = date(year, month, day)
                day_challenges = self._get_challenges_for_date(current_date)
                day_data = self._get_user_day_data(current_date)
                
                challenge_day = ChallengeDay(
                    date=current_date,
                    challenges=day_challenges,
                    is_today=current_date == date.today(),
                    is_past=current_date < date.today(),
                    is_future=current_date > date.today(),
                    completion_count=day_data.get('completed', 0),
                    total_challenges=len(day_challenges),
                    streak=day_data.get('streak', 0),
                    points_earned=day_data.get('points', 0),
                    badges=day_data.get('badges', [])
                )
                
                challenge_days.append(challenge_day)
                
                total_challenges += len(day_challenges)
                if challenge_day.is_completed():
                    completed_challenges += 1
                total_points += sum(c.get('points', 0) for c in day_challenges)
                earned_points += day_data.get('points', 0)
                
                if challenge_day.streak > best_streak:
                    best_streak = challenge_day.streak
                month_streak = challenge_day.streak
        
        return ChallengeMonth(
            year=year,
            month=month,
            days=challenge_days,
            total_challenges=total_challenges,
            completed_challenges=completed_challenges,
            total_points=total_points,
            earned_points=earned_points,
            streak=month_streak,
            best_streak=best_streak
        )

    def _get_challenges_for_date(self, current_date: date) -> List[Dict[str, Any]]:
        """Get challenges for a specific date."""
        # In production, this would fetch from database
        # For now, return sample challenges
        challenges = []
        
        # Daily challenges
        if current_date.weekday() < 5:  # Weekdays
            challenges.extend([
                {
                    'id': f'daily_{current_date.isoformat()}',
                    'title': '🚶 Take a 15-minute walk',
                    'type': 'daily',
                    'points': 10,
                    'difficulty': 'easy',
                    'category': 'transport',
                    'description': 'Take a short walk instead of driving'
                },
                {
                    'id': f'daily_2_{current_date.isoformat()}',
                    'title': '♻️ Sort and recycle waste',
                    'type': 'daily',
                    'points': 15,
                    'difficulty': 'easy',
                    'category': 'waste',
                    'description': 'Properly sort your recyclables'
                }
            ])
        else:  # Weekend
            challenges.extend([
                {
                    'id': f'weekly_{current_date.isoformat()}',
                    'title': '🌳 Plant a tree or sapling',
                    'type': 'weekly',
                    'points': 50,
                    'difficulty': 'medium',
                    'category': 'nature',
                    'description': 'Plant a tree in your garden or community'
                }
            ])
        
        return challenges

    def _get_user_day_data(self, current_date: date) -> Dict[str, Any]:
        """Get user progress data for a specific day."""
        date_key = current_date.isoformat()
        if date_key not in self._user_progress:
            self._user_progress[date_key] = {
                'completed': 0,
                'points': 0,
                'badges': [],
                'streak': 0
            }
        return self._user_progress[date_key]

    def get_today(self) -> ChallengeDay:
        """Get today's challenge data."""
        today = date.today()
        challenges = self._get_challenges_for_date(today)
        day_data = self._get_user_day_data(today)
        
        return ChallengeDay(
            date=today,
            challenges=challenges,
            is_today=True,
            is_past=False,
            is_future=False,
            completion_count=day_data.get('completed', 0),
            total_challenges=len(challenges),
            streak=day_data.get('streak', 0),
            points_earned=day_data.get('points', 0),
            badges=day_data.get('badges', [])
        )

    def get_streak(self) -> int:
        """Get current streak."""
        today = date.today()
        streak = 0
        
        # Check consecutive days
        for i in range(30):  # Max 30 days
            check_date = today - timedelta(days=i)
            date_key = check_date.isoformat()
            
            if date_key in self._user_progress:
                day_data = self._user_progress[date_key]
                challenges = self._get_challenges_for_date(check_date)
                
                if day_data.get('completed', 0) >= len(challenges):
                    streak += 1
                else:
                    break
            else:
                break
        
        return streak

    def complete_challenge(self, challenge_id: str, date_key: str = None) -> Dict[str, Any]:
        """
        Mark a challenge as completed.
        
        Args:
            challenge_id: Challenge ID
            date_key: Date in YYYY-MM-DD format
        
        Returns:
            Result dictionary with status and rewards
        """
        if date_key is None:
            date_key = date.today().isoformat()
        
        if date_key not in self._user_progress:
            self._user_progress[date_key] = {
                'completed': 0,
                'points': 0,
                'badges': [],
                'streak': 0
            }
        
        self._user_progress[date_key]['completed'] += 1
        self._user_progress[date_key]['points'] += 10  # Default points
        
        # Check for streak
        streak = self.get_streak()
        
        return {
            'success': True,
            'message': 'Challenge completed! 🌟',
            'streak': streak,
            'points_earned': 10
        }

    def get_monthly_stats(self, year: int = None, month: int = None) -> Dict[str, Any]:
        """Get monthly statistics."""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        month_data = self.get_month(year, month)
        
        return {
            'total_challenges': month_data.total_challenges,
            'completed': month_data.completed_challenges,
            'completion_rate': month_data.get_completion_rate(),
            'points_earned': month_data.earned_points,
            'total_points': month_data.total_points,
            'streak': month_data.streak,
            'best_streak': month_data.best_streak,
            'badges': month_data.badges_earned
        }

    def get_challenge_by_id(self, challenge_id: str) -> Optional[Dict[str, Any]]:
        """Get a challenge by ID."""
        return self._challenges.get(challenge_id)

    def get_upcoming_challenges(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get upcoming challenges for the next N days."""
        upcoming = []
        today = date.today()
        
        for i in range(1, days + 1):
            future_date = today + timedelta(days=i)
            challenges = self._get_challenges_for_date(future_date)
            for challenge in challenges:
                challenge['date'] = future_date.isoformat()
                upcoming.append(challenge)
        
        return upcoming

    def get_recent_completed(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get recently completed challenges."""
        completed = []
        today = date.today()
        
        for i in range(days):
            check_date = today - timedelta(days=i)
            date_key = check_date.isoformat()
            
            if date_key in self._user_progress:
                day_data = self._user_progress[date_key]
                if day_data.get('completed', 0) > 0:
                    challenges = self._get_challenges_for_date(check_date)
                    for challenge in challenges[:day_data['completed']]:
                        challenge['completed_date'] = date_key
                        completed.append(challenge)
        
        return completed