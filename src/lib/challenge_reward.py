"""
Challenge Rewards for EcoBuddy AI
Manages rewards, badges, and achievements for completing challenges.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Reward:
    """Data class for a reward."""
    id: str
    name: str
    description: str
    icon: str
    points: int
    category: str  # challenge, streak, milestone, special
    rarity: str  # common, uncommon, rare, epic, legendary
    unlocked: bool = False
    unlocked_date: Optional[str] = None


class ChallengeRewards:
    """
    Manages rewards and badges for eco-challenges.
    """

    def __init__(self):
        self._rewards: Dict[str, Reward] = {}
        self._user_rewards: Dict[str, List[str]] = {}
        self._initialize_rewards()

    def _initialize_rewards(self):
        """Initialize all available rewards."""
        rewards = [
            # Challenge completion rewards
            Reward(
                id="first_challenge",
                name="First Challenge",
                description="Complete your first eco-challenge",
                icon="🎯",
                points=10,
                category="challenge",
                rarity="common"
            ),
            Reward(
                id="challenge_master_10",
                name="Challenge Master",
                description="Complete 10 eco-challenges",
                icon="🏅",
                points=50,
                category="challenge",
                rarity="uncommon"
            ),
            Reward(
                id="challenge_legend_50",
                name="Challenge Legend",
                description="Complete 50 eco-challenges",
                icon="🏆",
                points=200,
                category="challenge",
                rarity="rare"
            ),
            Reward(
                id="challenge_grandmaster_100",
                name="Challenge Grandmaster",
                description="Complete 100 eco-challenges",
                icon="👑",
                points=500,
                category="challenge",
                rarity="epic"
            ),
            
            # Streak rewards
            Reward(
                id="streak_7",
                name="Week Warrior",
                description="Maintain a 7-day streak",
                icon="🔥",
                points=50,
                category="streak",
                rarity="uncommon"
            ),
            Reward(
                id="streak_30",
                name="Month Master",
                description="Maintain a 30-day streak",
                icon="🌙",
                points=200,
                category="streak",
                rarity="rare"
            ),
            Reward(
                id="streak_100",
                name="Century Club",
                description="Maintain a 100-day streak",
                icon="💯",
                points=500,
                category="streak",
                rarity="epic"
            ),
            Reward(
                id="streak_365",
                name="Year of Green",
                description="Maintain a 365-day streak",
                icon="🌟",
                points=1000,
                category="streak",
                rarity="legendary"
            ),
            
            # Category rewards
            Reward(
                id="transport_champion",
                name="Transport Champion",
                description="Complete 25 transport challenges",
                icon="🚲",
                points=100,
                category="special",
                rarity="rare"
            ),
            Reward(
                id="energy_saver",
                name="Energy Saver",
                description="Complete 25 energy challenges",
                icon="⚡",
                points=100,
                category="special",
                rarity="rare"
            ),
            Reward(
                id="water_warrior",
                name="Water Warrior",
                description="Complete 25 water challenges",
                icon="💧",
                points=100,
                category="special",
                rarity="rare"
            ),
            Reward(
                id="waste_reducer",
                name="Waste Reducer",
                description="Complete 25 waste challenges",
                icon="♻️",
                points=100,
                category="special",
                rarity="rare"
            ),
            
            # Milestone rewards
            Reward(
                id="milestone_10",
                name="10 Days Green",
                description="Complete 10 days of challenges",
                icon="🎉",
                points=50,
                category="milestone",
                rarity="uncommon"
            ),
            Reward(
                id="milestone_50",
                name="50 Days Green",
                description="Complete 50 days of challenges",
                icon="🎊",
                points=150,
                category="milestone",
                rarity="rare"
            ),
            Reward(
                id="milestone_100",
                name="100 Days Green",
                description="Complete 100 days of challenges",
                icon="🌟",
                points=300,
                category="milestone",
                rarity="epic"
            ),
            
            # Special rewards
            Reward(
                id="all_category_master",
                name="All Category Master",
                description="Complete 10 challenges in every category",
                icon="🏆",
                points=500,
                category="special",
                rarity="epic"
            ),
            Reward(
                id="perfect_month",
                name="Perfect Month",
                description="Complete every challenge for a full month",
                icon="📅",
                points=300,
                category="special",
                rarity="rare"
            )
        ]

        for reward in rewards:
            self._rewards[reward.id] = reward

    def check_and_award_rewards(
        self,
        user_id: str,
        challenge_count: int,
        streak: int,
        category_counts: Dict[str, int],
        days_active: int
    ) -> List[Reward]:
        """
        Check and award rewards based on user activity.
        
        Args:
            user_id: User ID
            challenge_count: Total challenges completed
            streak: Current streak
            category_counts: Counts by category
            days_active: Total active days
        
        Returns:
            List of newly awarded rewards
        """
        if user_id not in self._user_rewards:
            self._user_rewards[user_id] = []

        awarded = []
        
        # Check challenge rewards
        if challenge_count >= 1 and self._can_award(user_id, "first_challenge"):
            awarded.append(self._award_reward(user_id, "first_challenge"))
        
        if challenge_count >= 10 and self._can_award(user_id, "challenge_master_10"):
            awarded.append(self._award_reward(user_id, "challenge_master_10"))
        
        if challenge_count >= 50 and self._can_award(user_id, "challenge_legend_50"):
            awarded.append(self._award_reward(user_id, "challenge_legend_50"))
        
        if challenge_count >= 100 and self._can_award(user_id, "challenge_grandmaster_100"):
            awarded.append(self._award_reward(user_id, "challenge_grandmaster_100"))
        
        # Check streak rewards
        if streak >= 7 and self._can_award(user_id, "streak_7"):
            awarded.append(self._award_reward(user_id, "streak_7"))
        
        if streak >= 30 and self._can_award(user_id, "streak_30"):
            awarded.append(self._award_reward(user_id, "streak_30"))
        
        if streak >= 100 and self._can_award(user_id, "streak_100"):
            awarded.append(self._award_reward(user_id, "streak_100"))
        
        if streak >= 365 and self._can_award(user_id, "streak_365"):
            awarded.append(self._award_reward(user_id, "streak_365"))
        
        # Check category rewards
        for category, count in category_counts.items():
            if count >= 25:
                reward_id = f"{category}_champion"
                if self._can_award(user_id, reward_id):
                    awarded.append(self._award_reward(user_id, reward_id))
        
        # Check milestone rewards
        if days_active >= 10 and self._can_award(user_id, "milestone_10"):
            awarded.append(self._award_reward(user_id, "milestone_10"))
        
        if days_active >= 50 and self._can_award(user_id, "milestone_50"):
            awarded.append(self._award_reward(user_id, "milestone_50"))
        
        if days_active >= 100 and self._can_award(user_id, "milestone_100"):
            awarded.append(self._award_reward(user_id, "milestone_100"))
        
        return awarded

    def _can_award(self, user_id: str, reward_id: str) -> bool:
        """Check if a reward can be awarded."""
        return reward_id not in self._user_rewards.get(user_id, [])

    def _award_reward(self, user_id: str, reward_id: str) -> Reward:
        """Award a reward to a user."""
        if user_id not in self._user_rewards:
            self._user_rewards[user_id] = []
        
        self._user_rewards[user_id].append(reward_id)
        reward = self._rewards[reward_id]
        reward.unlocked = True
        reward.unlocked_date = datetime.now().isoformat()
        
        return reward

    def get_user_rewards(self, user_id: str) -> List[Reward]:
        """Get all rewards for a user."""
        if user_id not in self._user_rewards:
            return []
        
        return [self._rewards[rid] for rid in self._user_rewards[user_id] if rid in self._rewards]

    def get_user_reward_stats(self, user_id: str) -> Dict[str, Any]:
        """Get reward statistics for a user."""
        rewards = self.get_user_rewards(user_id)
        
        stats = {
            'total_rewards': len(rewards),
            'by_category': {},
            'by_rarity': {},
            'total_points': 0
        }
        
        for reward in rewards:
            stats['by_category'][reward.category] = stats['by_category'].get(reward.category, 0) + 1
            stats['by_rarity'][reward.rarity] = stats['by_rarity'].get(reward.rarity, 0) + 1
            stats['total_points'] += reward.points
        
        return stats