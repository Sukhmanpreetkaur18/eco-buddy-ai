"""
Investment Tracker for EcoBuddy AI
Tracks green investments, calculates returns, and manages investment portfolios.
"""

from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import json
import logging
import uuid
import math

logger = logging.getLogger(__name__)


@dataclass
class Investment:
    """Data class for a single investment."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    category: str = ""  # solar, ev, energy_efficiency, water, waste, sustainable_agriculture, green_building, etc.
    amount: float = 0.0
    invested_date: str = ""
    expected_roi: float = 0.0  # Expected annual return percentage
    actual_roi: float = 0.0
    annual_savings: float = 0.0  # Annual savings in currency
    co2_saved: float = 0.0  # Annual CO2 saved in kg
    energy_saved: float = 0.0  # Annual energy saved in kWh
    water_saved: float = 0.0  # Annual water saved in liters
    trees_equivalent: float = 0.0
    status: str = "active"  # active, completed, pending
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class InvestmentPortfolio:
    """Data class for an investment portfolio."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "My Green Portfolio"
    investments: List[Investment] = field(default_factory=list)
    total_invested: float = 0.0
    total_savings: float = 0.0
    total_co2_saved: float = 0.0
    total_energy_saved: float = 0.0
    total_water_saved: float = 0.0
    total_trees: float = 0.0
    overall_roi: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class InvestmentGoal:
    """Data class for an investment goal."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    target_amount: float = 0.0
    current_amount: float = 0.0
    deadline: str = ""
    category: str = "general"
    priority: str = "medium"  # low, medium, high
    status: str = "active"  # active, completed, failed
    progress: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class InvestmentTracker:
    """
    Manages green investments, portfolios, and investment goals.
    """

    INVESTMENT_CATEGORIES = {
        'solar': {
            'name': 'Solar Energy',
            'icon': '☀️',
            'co2_factor': 0.5,  # kg CO2 saved per $ invested
            'energy_factor': 2.0,  # kWh saved per $ invested
            'water_factor': 0.1,  # liters saved per $ invested
            'avg_roi': 0.12,  # Average ROI
            'description': 'Solar panel installation and solar energy systems'
        },
        'ev': {
            'name': 'Electric Vehicle',
            'icon': '🚗',
            'co2_factor': 0.8,
            'energy_factor': 1.5,
            'water_factor': 0.05,
            'avg_roi': 0.10,
            'description': 'Electric vehicles and charging infrastructure'
        },
        'energy_efficiency': {
            'name': 'Energy Efficiency',
            'icon': '💡',
            'co2_factor': 0.3,
            'energy_factor': 3.0,
            'water_factor': 0.0,
            'avg_roi': 0.15,
            'description': 'LED lighting, smart thermostats, efficient appliances'
        },
        'water': {
            'name': 'Water Conservation',
            'icon': '💧',
            'co2_factor': 0.1,
            'energy_factor': 0.2,
            'water_factor': 5.0,
            'avg_roi': 0.08,
            'description': 'Water-efficient fixtures, rainwater harvesting'
        },
        'waste': {
            'name': 'Waste Management',
            'icon': '♻️',
            'co2_factor': 0.4,
            'energy_factor': 0.5,
            'water_factor': 0.0,
            'avg_roi': 0.10,
            'description': 'Recycling, composting, waste reduction systems'
        },
        'green_building': {
            'name': 'Green Building',
            'icon': '🏗️',
            'co2_factor': 1.0,
            'energy_factor': 1.0,
            'water_factor': 0.5,
            'avg_roi': 0.07,
            'description': 'Sustainable construction, green materials'
        },
        'sustainable_agriculture': {
            'name': 'Sustainable Agriculture',
            'icon': '🌾',
            'co2_factor': 0.6,
            'energy_factor': 0.3,
            'water_factor': 3.0,
            'avg_roi': 0.09,
            'description': 'Organic farming, permaculture, regenerative agriculture'
        },
        'reforestation': {
            'name': 'Reforestation',
            'icon': '🌳',
            'co2_factor': 2.0,
            'energy_factor': 0.0,
            'water_factor': 0.2,
            'avg_roi': 0.05,
            'description': 'Tree planting, forest restoration projects'
        }
    }

    def __init__(self, user_id: str = None):
        self.user_id = user_id
        self._investments: List[Investment] = []
        self._goals: List[InvestmentGoal] = []
        self._portfolio: Optional[InvestmentPortfolio] = None
        self._load_data()

    def _load_data(self):
        """Load investment data from storage."""
        # In production, this would load from database
        pass

    def add_investment(self, investment: Investment) -> Dict[str, Any]:
        """
        Add a new investment.
        
        Args:
            investment: Investment object
        
        Returns:
            Result dictionary
        """
        try:
            self._investments.append(investment)
            self._update_portfolio()
            return {
                'success': True,
                'message': f'Investment "{investment.name}" added successfully! 🌱',
                'investment_id': investment.id
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_investment(self, investment_id: str) -> Optional[Investment]:
        """Get an investment by ID."""
        for inv in self._investments:
            if inv.id == investment_id:
                return inv
        return None

    def get_all_investments(self) -> List[Investment]:
        """Get all investments."""
        return self._investments

    def get_investments_by_category(self, category: str) -> List[Investment]:
        """Get investments by category."""
        return [inv for inv in self._investments if inv.category == category]

    def get_investments_by_status(self, status: str) -> List[Investment]:
        """Get investments by status."""
        return [inv for inv in self._investments if inv.status == status]

    def update_investment(self, investment_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an investment."""
        for inv in self._investments:
            if inv.id == investment_id:
                for key, value in updates.items():
                    if hasattr(inv, key):
                        setattr(inv, key, value)
                inv.updated_at = datetime.now().isoformat()
                self._update_portfolio()
                return {
                    'success': True,
                    'message': f'Investment "{inv.name}" updated successfully!'
                }
        return {'success': False, 'error': 'Investment not found'}

    def delete_investment(self, investment_id: str) -> Dict[str, Any]:
        """Delete an investment."""
        for i, inv in enumerate(self._investments):
            if inv.id == investment_id:
                del self._investments[i]
                self._update_portfolio()
                return {
                    'success': True,
                    'message': f'Investment "{inv.name}" deleted successfully!'
                }
        return {'success': False, 'error': 'Investment not found'}

    def _update_portfolio(self):
        """Update portfolio totals."""
        if not self._portfolio:
            self._portfolio = InvestmentPortfolio()

        total_invested = sum(inv.amount for inv in self._investments)
        total_savings = sum(inv.annual_savings for inv in self._investments)
        total_co2 = sum(inv.co2_saved for inv in self._investments)
        total_energy = sum(inv.energy_saved for inv in self._investments)
        total_water = sum(inv.water_saved for inv in self._investments)
        total_trees = sum(inv.trees_equivalent for inv in self._investments)

        self._portfolio.total_invested = total_invested
        self._portfolio.total_savings = total_savings
        self._portfolio.total_co2_saved = total_co2
        self._portfolio.total_energy_saved = total_energy
        self._portfolio.total_water_saved = total_water
        self._portfolio.total_trees = total_trees

        if total_invested > 0:
            self._portfolio.overall_roi = (total_savings / total_invested) * 100
        else:
            self._portfolio.overall_roi = 0

        self._portfolio.updated_at = datetime.now().isoformat()

    def get_portfolio(self) -> InvestmentPortfolio:
        """Get the investment portfolio."""
        if not self._portfolio:
            self._portfolio = InvestmentPortfolio()
        return self._portfolio

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get portfolio summary statistics."""
        portfolio = self.get_portfolio()
        
        return {
            'total_investments': len(self._investments),
            'total_invested': portfolio.total_invested,
            'total_savings': portfolio.total_savings,
            'total_co2_saved': portfolio.total_co2_saved,
            'total_energy_saved': portfolio.total_energy_saved,
            'total_water_saved': portfolio.total_water_saved,
            'total_trees': portfolio.total_trees,
            'overall_roi': portfolio.overall_roi,
            'by_category': self._get_category_breakdown(),
            'by_status': self._get_status_breakdown()
        }

    def _get_category_breakdown(self) -> Dict[str, Dict[str, Any]]:
        """Get breakdown by category."""
        breakdown = {}
        for category in self.INVESTMENT_CATEGORIES:
            investments = self.get_investments_by_category(category)
            if investments:
                total = sum(inv.amount for inv in investments)
                breakdown[category] = {
                    'name': self.INVESTMENT_CATEGORIES[category]['name'],
                    'icon': self.INVESTMENT_CATEGORIES[category]['icon'],
                    'count': len(investments),
                    'total_invested': total,
                    'total_savings': sum(inv.annual_savings for inv in investments),
                    'total_co2': sum(inv.co2_saved for inv in investments)
                }
        return breakdown

    def _get_status_breakdown(self) -> Dict[str, int]:
        """Get breakdown by status."""
        breakdown = {}
        for inv in self._investments:
            breakdown[inv.status] = breakdown.get(inv.status, 0) + 1
        return breakdown

    def calculate_impact(self, investment: Investment) -> Dict[str, float]:
        """
        Calculate environmental impact of an investment.
        
        Args:
            investment: Investment object
        
        Returns:
            Impact metrics dictionary
        """
        category_data = self.INVESTMENT_CATEGORIES.get(investment.category, {})
        
        co2_saved = investment.amount * category_data.get('co2_factor', 0.5)
        energy_saved = investment.amount * category_data.get('energy_factor', 1.0)
        water_saved = investment.amount * category_data.get('water_factor', 0.1)
        
        # Trees equivalent (1 tree absorbs ~22kg CO2 per year)
        trees_equivalent = co2_saved / 22
        
        return {
            'co2_saved': co2_saved,
            'energy_saved': energy_saved,
            'water_saved': water_saved,
            'trees_equivalent': trees_equivalent
        }

    def calculate_roi(self, investment: Investment, years: int = 5) -> Dict[str, float]:
        """
        Calculate ROI for an investment.
        
        Args:
            investment: Investment object
            years: Number of years to calculate
        
        Returns:
            ROI metrics dictionary
        """
        total_savings = investment.annual_savings * years
        net_profit = total_savings - investment.amount
        
        if investment.amount > 0:
            roi_percentage = (net_profit / investment.amount) * 100
            annual_roi = roi_percentage / years
        else:
            roi_percentage = 0
            annual_roi = 0
        
        payback_period = investment.amount / investment.annual_savings if investment.annual_savings > 0 else float('inf')
        
        return {
            'total_savings': total_savings,
            'net_profit': net_profit,
            'roi_percentage': roi_percentage,
            'annual_roi': annual_roi,
            'payback_period': payback_period
        }

    def add_goal(self, goal: InvestmentGoal) -> Dict[str, Any]:
        """Add an investment goal."""
        try:
            self._goals.append(goal)
            return {
                'success': True,
                'message': f'Goal "{goal.name}" added successfully! 🎯'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_goals(self) -> List[InvestmentGoal]:
        """Get all investment goals."""
        return self._goals

    def update_goal_progress(self, goal_id: str, amount: float) -> Dict[str, Any]:
        """Update goal progress."""
        for goal in self._goals:
            if goal.id == goal_id:
                goal.current_amount += amount
                goal.progress = (goal.current_amount / goal.target_amount) * 100 if goal.target_amount > 0 else 0
                if goal.progress >= 100:
                    goal.status = 'completed'
                return {
                    'success': True,
                    'message': f'Goal "{goal.name}" progress updated!',
                    'progress': goal.progress
                }
        return {'success': False, 'error': 'Goal not found'}

    def get_goal_progress(self) -> Dict[str, Any]:
        """Get overall goal progress."""
        if not self._goals:
            return {'total_goals': 0, 'completed': 0, 'progress': 0}

        total = len(self._goals)
        completed = sum(1 for g in self._goals if g.status == 'completed')
        avg_progress = sum(g.progress for g in self._goals) / total

        return {
            'total_goals': total,
            'completed': completed,
            'in_progress': total - completed,
            'avg_progress': avg_progress,
            'goals': self._goals
        }

    def get_investment_categories(self) -> Dict[str, Dict[str, Any]]:
        """Get all investment categories."""
        return self.INVESTMENT_CATEGORIES

    def get_recommendations(self) -> List[Dict[str, Any]]:
        """Get investment recommendations."""
        recommendations = []
        
        # Check current portfolio
        portfolio = self.get_portfolio()
        
        # Recommend solar if not present
        if not self.get_investments_by_category('solar'):
            recommendations.append({
                'category': 'solar',
                'name': 'Solar Energy',
                'reason': 'Great ROI with significant environmental impact',
                'estimated_cost': 5000,
                'estimated_savings': 600,
                'estimated_co2_saved': 2500
            })
        
        # Recommend EV if not present
        if not self.get_investments_by_category('ev'):
            recommendations.append({
                'category': 'ev',
                'name': 'Electric Vehicle',
                'reason': 'Reduce transportation emissions significantly',
                'estimated_cost': 30000,
                'estimated_savings': 3000,
                'estimated_co2_saved': 4000
            })
        
        # Recommend energy efficiency
        if len(self.get_investments_by_category('energy_efficiency')) < 2:
            recommendations.append({
                'category': 'energy_efficiency',
                'name': 'Energy Efficiency Upgrades',
                'reason': 'Quick payback period with immediate savings',
                'estimated_cost': 2000,
                'estimated_savings': 300,
                'estimated_co2_saved': 1500
            })
        
        # Recommend water conservation
        if not self.get_investments_by_category('water'):
            recommendations.append({
                'category': 'water',
                'name': 'Water Conservation',
                'reason': 'Save water and reduce utility bills',
                'estimated_cost': 1500,
                'estimated_savings': 150,
                'estimated_co2_saved': 500
            })
        
        return recommendations