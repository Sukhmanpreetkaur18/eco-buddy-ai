"""
Investment Reports for EcoBuddy AI
Generates reports on investments, savings, and environmental impact.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import pandas as pd
from io import StringIO


class InvestmentReports:
    """
    Generates reports on investments, savings, and environmental impact.
    """

    def __init__(self):
        pass

    def generate_summary_report(self, investments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a summary report of all investments.
        
        Args:
            investments: List of investment dictionaries
        
        Returns:
            Summary report
        """
        total_invested = sum(inv.get('amount', 0) for inv in investments)
        total_savings = sum(inv.get('annual_savings', 0) for inv in investments)
        total_co2 = sum(inv.get('co2_saved', 0) for inv in investments)
        total_energy = sum(inv.get('energy_saved', 0) for inv in investments)
        total_water = sum(inv.get('water_saved', 0) for inv in investments)
        total_trees = sum(inv.get('trees_equivalent', 0) for inv in investments)

        return {
            'total_investments': len(investments),
            'total_invested': total_invested,
            'total_annual_savings': total_savings,
            'total_co2_saved': total_co2,
            'total_energy_saved': total_energy,
            'total_water_saved': total_water,
            'total_trees_equivalent': total_trees,
            'roi_percentage': (total_savings / total_invested * 100) if total_invested > 0 else 0,
            'by_category': self._group_by_category(investments),
            'by_status': self._group_by_status(investments),
            'generated_at': datetime.now().isoformat()
        }

    def _group_by_category(self, investments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Group investments by category."""
        categories = {}
        for inv in investments:
            category = inv.get('category', 'other')
            if category not in categories:
                categories[category] = {
                    'count': 0,
                    'total_invested': 0,
                    'total_savings': 0,
                    'total_co2': 0
                }
            categories[category]['count'] += 1
            categories[category]['total_invested'] += inv.get('amount', 0)
            categories[category]['total_savings'] += inv.get('annual_savings', 0)
            categories[category]['total_co2'] += inv.get('co2_saved', 0)
        return categories

    def _group_by_status(self, investments: List[Dict[str, Any]]) -> Dict[str, int]:
        """Group investments by status."""
        statuses = {}
        for inv in investments:
            status = inv.get('status', 'active')
            statuses[status] = statuses.get(status, 0) + 1
        return statuses

    def generate_impact_report(self, investments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate an environmental impact report.
        
        Args:
            investments: List of investment dictionaries
        
        Returns:
            Impact report
        """
        total_co2 = sum(inv.get('co2_saved', 0) for inv in investments)
        total_trees = sum(inv.get('trees_equivalent', 0) for inv in investments)
        total_energy = sum(inv.get('energy_saved', 0) for inv in investments)
        total_water = sum(inv.get('water_saved', 0) for inv in investments)

        return {
            'co2_saved_kg': total_co2,
            'co2_saved_tons': total_co2 / 1000,
            'trees_equivalent': total_trees,
            'energy_saved_kwh': total_energy,
            'water_saved_liters': total_water,
            'equivalent_metric': self._get_equivalent_metrics(total_co2),
            'generated_at': datetime.now().isoformat()
        }

    def _get_equivalent_metrics(self, co2_kg: float) -> Dict[str, float]:
        """Get equivalent metrics for CO2 savings."""
        return {
            'car_km': co2_kg / 0.2,
            'kwh': co2_kg / 0.4,
            'meals': co2_kg / 5,
            'flight_km': co2_kg / 0.25,
            'trees': co2_kg / 22
        }

    def generate_roi_report(self, investments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate an ROI report.
        
        Args:
            investments: List of investment dictionaries
        
        Returns:
            ROI report
        """
        total_invested = sum(inv.get('amount', 0) for inv in investments)
        total_savings = sum(inv.get('annual_savings', 0) for inv in investments)
        
        return {
            'total_invested': total_invested,
            'total_annual_savings': total_savings,
            'roi_percentage': (total_savings / total_invested * 100) if total_invested > 0 else 0,
            'payback_years': total_invested / total_savings if total_savings > 0 else float('inf'),
            'by_investment': [
                {
                    'name': inv.get('name', 'Unknown'),
                    'amount': inv.get('amount', 0),
                    'annual_savings': inv.get('annual_savings', 0),
                    'roi': (inv.get('annual_savings', 0) / inv.get('amount', 1)) * 100,
                    'payback_years': inv.get('amount', 1) / inv.get('annual_savings', 1) if inv.get('annual_savings', 0) > 0 else float('inf')
                }
                for inv in investments
            ],
            'generated_at': datetime.now().isoformat()
        }

    def generate_csv_report(self, investments: List[Dict[str, Any]]) -> str:
        """
        Generate a CSV report of investments.
        
        Args:
            investments: List of investment dictionaries
        
        Returns:
            CSV string
        """
        data = []
        for inv in investments:
            data.append({
                'Name': inv.get('name', ''),
                'Category': inv.get('category', ''),
                'Amount': inv.get('amount', 0),
                'Annual Savings': inv.get('annual_savings', 0),
                'CO2 Saved (kg)': inv.get('co2_saved', 0),
                'Energy Saved (kWh)': inv.get('energy_saved', 0),
                'Water Saved (L)': inv.get('water_saved', 0),
                'Trees Equivalent': inv.get('trees_equivalent', 0),
                'Status': inv.get('status', ''),
                'Invested Date': inv.get('invested_date', ''),
                'Expected ROI': inv.get('expected_roi', 0),
                'Actual ROI': inv.get('actual_roi', 0)
            })
        
        df = pd.DataFrame(data)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue()