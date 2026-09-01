"""
Challenge Generator for EcoBuddy AI
Generates daily, weekly, and monthly eco-challenges with varying difficulty.
"""

import random
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta, date


class ChallengeGenerator:
    """
    Generates eco-challenges with different types, difficulties, and categories.
    """

    def __init__(self):
        self.challenge_pool = self._initialize_challenge_pool()

    def _initialize_challenge_pool(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize the challenge pool with predefined challenges."""
        return {
            'daily': [
                {
                    'title': '🚶 Walk for 15 minutes',
                    'description': 'Take a 15-minute walk instead of driving',
                    'category': 'transport',
                    'points': 10,
                    'difficulty': 'easy',
                    'effort': 'low'
                },
                {
                    'title': '♻️ Recycle waste',
                    'description': 'Properly sort and recycle your household waste',
                    'category': 'waste',
                    'points': 15,
                    'difficulty': 'easy',
                    'effort': 'low'
                },
                {
                    'title': '💡 Turn off unused lights',
                    'description': 'Turn off lights in empty rooms all day',
                    'category': 'energy',
                    'points': 10,
                    'difficulty': 'easy',
                    'effort': 'low'
                },
                {
                    'title': '🚿 Shorten shower by 2 minutes',
                    'description': 'Reduce your shower time by 2 minutes',
                    'category': 'water',
                    'points': 15,
                    'difficulty': 'easy',
                    'effort': 'low'
                },
                {
                    'title': '🥗 Eat one plant-based meal',
                    'description': 'Replace one meal with plant-based food',
                    'category': 'diet',
                    'points': 20,
                    'difficulty': 'medium',
                    'effort': 'medium'
                },
                {
                    'title': '🛍️ Use reusable bag',
                    'description': 'Use reusable bags for all shopping today',
                    'category': 'waste',
                    'points': 10,
                    'difficulty': 'easy',
                    'effort': 'low'
                },
                {
                    'title': '📊 Track your footprint',
                    'description': 'Complete a carbon footprint assessment',
                    'category': 'tracking',
                    'points': 25,
                    'difficulty': 'medium',
                    'effort': 'medium'
                },
                {
                    'title': '🚲 Bike instead of drive',
                    'description': 'Use a bike for a short trip instead of car',
                    'category': 'transport',
                    'points': 30,
                    'difficulty': 'medium',
                    'effort': 'medium'
                }
            ],
            'weekly': [
                {
                    'title': '🌳 Plant a tree',
                    'description': 'Plant a tree in your garden or community',
                    'category': 'nature',
                    'points': 50,
                    'difficulty': 'medium',
                    'effort': 'high'
                },
                {
                    'title': '💧 Fix leaking taps',
                    'description': 'Fix all leaking taps in your home',
                    'category': 'water',
                    'points': 40,
                    'difficulty': 'medium',
                    'effort': 'medium'
                },
                {
                    'title': '♻️ Zero waste day',
                    'description': 'Produce zero waste for one day',
                    'category': 'waste',
                    'points': 60,
                    'difficulty': 'hard',
                    'effort': 'high'
                },
                {
                    'title': '📉 Reduce electricity by 20%',
                    'description': 'Reduce your electricity usage by 20% this week',
                    'category': 'energy',
                    'points': 55,
                    'difficulty': 'hard',
                    'effort': 'high'
                },
                {
                    'title': '🥕 Visit a farmers market',
                    'description': 'Buy local produce from a farmers market',
                    'category': 'diet',
                    'points': 35,
                    'difficulty': 'medium',
                    'effort': 'medium'
                }
            ],
            'monthly': [
                {
                    'title': '🌍 Carbon reduction month',
                    'description': 'Reduce your carbon footprint by 15% this month',
                    'category': 'footprint',
                    'points': 200,
                    'difficulty': 'hard',
                    'effort': 'very_high'
                },
                {
                    'title': '📚 Sustainability challenge',
                    'description': 'Complete 20 daily challenges this month',
                    'category': 'tracking',
                    'points': 150,
                    'difficulty': 'hard',
                    'effort': 'high'
                },
                {
                    'title': '🌱 Start a compost',
                    'description': 'Start composting your organic waste',
                    'category': 'waste',
                    'points': 100,
                    'difficulty': 'medium',
                    'effort': 'high'
                }
            ]
        }

    def generate_daily_challenges(self, count: int = 3) -> List[Dict[str, Any]]:
        """Generate daily challenges."""
        daily_pool = self.challenge_pool['daily']
        selected = random.sample(daily_pool, min(count, len(daily_pool)))
        
        for challenge in selected:
            challenge['type'] = 'daily'
            challenge['date'] = date.today().isoformat()
        
        return selected

    def generate_weekly_challenges(self, count: int = 2) -> List[Dict[str, Any]]:
        """Generate weekly challenges."""
        weekly_pool = self.challenge_pool['weekly']
        selected = random.sample(weekly_pool, min(count, len(weekly_pool)))
        
        for challenge in selected:
            challenge['type'] = 'weekly'
            challenge['date'] = date.today().isoformat()
        
        return selected

    def generate_monthly_challenges(self, count: int = 1) -> List[Dict[str, Any]]:
        """Generate monthly challenges."""
        monthly_pool = self.challenge_pool['monthly']
        selected = random.sample(monthly_pool, min(count, len(monthly_pool)))
        
        for challenge in selected:
            challenge['type'] = 'monthly'
            challenge['date'] = date.today().isoformat()
        
        return selected

    def generate_all_challenges(self) -> List[Dict[str, Any]]:
        """Generate all challenges for the day."""
        challenges = []
        challenges.extend(self.generate_daily_challenges(3))
        challenges.extend(self.generate_weekly_challenges(2))
        challenges.extend(self.generate_monthly_challenges(1))
        return challenges

    def get_challenge_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """Get challenges by difficulty level."""
        all_challenges = []
        for pool in self.challenge_pool.values():
            for challenge in pool:
                if challenge.get('difficulty') == difficulty:
                    all_challenges.append(challenge)
        return all_challenges

    def get_challenge_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get challenges by category."""
        all_challenges = []
        for pool in self.challenge_pool.values():
            for challenge in pool:
                if challenge.get('category') == category:
                    all_challenges.append(challenge)
        return all_challenges

    def get_random_challenge(self) -> Dict[str, Any]:
        """Get a random challenge."""
        all_challenges = []
        for pool in self.challenge_pool.values():
            all_challenges.extend(pool)
        return random.choice(all_challenges)

    def get_challenge_stats(self) -> Dict[str, Any]:
        """Get challenge statistics."""
        total = 0
        by_type = {}
        by_difficulty = {}
        by_category = {}
        
        for challenge_type, challenges in self.challenge_pool.items():
            by_type[challenge_type] = len(challenges)
            total += len(challenges)
            
            for challenge in challenges:
                difficulty = challenge.get('difficulty', 'unknown')
                by_difficulty[difficulty] = by_difficulty.get(difficulty, 0) + 1
                
                category = challenge.get('category', 'unknown')
                by_category[category] = by_category.get(category, 0) + 1
        
        return {
            'total_challenges': total,
            'by_type': by_type,
            'by_difficulty': by_difficulty,
            'by_category': by_category
        }