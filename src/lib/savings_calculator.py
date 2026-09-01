"""
Impact Calculator for EcoBuddy AI
Calculates environmental impact of sustainable choices and investments.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta


class ImpactCalculator:
    """
    Calculates environmental impact metrics for various sustainable actions.
    """

    # Environmental impact factors
    FACTORS = {
        'co2_per_kwh': 0.4,  # kg CO2 per kWh (US average)
        'co2_per_liter_water': 0.002,  # kg CO2 per liter of water
        'co2_per_kg_waste': 0.5,  # kg CO2 per kg of waste
        'co2_per_km_driving': 0.2,  # kg CO2 per km driven
        'co2_per_km_flying': 0.25,  # kg CO2 per km flown
        'co2_per_kg_meat': 15,  # kg CO2 per kg of meat
        'co2_per_kg_dairy': 3,  # kg CO2 per kg of dairy
        'co2_per_kg_vegetables': 0.5,  # kg CO2 per kg of vegetables
        'trees_per_co2': 1/22,  # 1 tree absorbs ~22kg CO2 per year
        'water_per_kwh': 0.5,  # liters of water per kWh
        'land_per_meat': 20,  # square meters per kg of meat
    }

    def __init__(self):
        pass

    def calculate_co2_impact(self, action_type: str, amount: float) -> Dict[str, float]:
        """
        Calculate CO2 impact of an action.
        
        Args:
            action_type: Type of action (energy, driving, flying, meat, dairy, waste, water)
            amount: Amount of the action
        
        Returns:
            Impact metrics
        """
        factors = {
            'energy': self.FACTORS['co2_per_kwh'],
            'driving': self.FACTORS['co2_per_km_driving'],
            'flying': self.FACTORS['co2_per_km_flying'],
            'meat': self.FACTORS['co2_per_kg_meat'],
            'dairy': self.FACTORS['co2_per_kg_dairy'],
            'waste': self.FACTORS['co2_per_kg_waste'],
            'water': self.FACTORS['co2_per_liter_water']
        }

        co2_factor = factors.get(action_type, 0)
        co2_saved = amount * co2_factor
        trees_equivalent = co2_saved * self.FACTORS['trees_per_co2']

        return {
            'co2_saved_kg': co2_saved,
            'trees_equivalent': trees_equivalent,
            'action_type': action_type,
            'amount': amount
        }

    def calculate_lifetime_impact(self, investment_amount: float, annual_co2_reduction: float, years: int = 10) -> Dict[str, float]:
        """
        Calculate lifetime impact of an investment.
        
        Args:
            investment_amount: Total investment amount
            annual_co2_reduction: Annual CO2 reduction in kg
            years: Number of years
        
        Returns:
            Lifetime impact metrics
        """
        lifetime_co2 = annual_co2_reduction * years
        lifetime_trees = lifetime_co2 * self.FACTORS['trees_per_co2']

        return {
            'lifetime_co2_kg': lifetime_co2,
            'lifetime_trees': lifetime_trees,
            'annual_co2_kg': annual_co2_reduction,
            'investment_amount': investment_amount,
            'co2_per_dollar': annual_co2_reduction / investment_amount if investment_amount > 0 else 0
        }

    def calculate_water_impact(self, water_saved_liters: float) -> Dict[str, float]:
        """
        Calculate water conservation impact.
        
        Args:
            water_saved_liters: Liters of water saved
        
        Returns:
            Water impact metrics
        """
        energy_saved = water_saved_liters * 0.05  # kWh per liter heated
        co2_saved = energy_saved * self.FACTORS['co2_per_kwh']

        return {
            'water_saved_liters': water_saved_liters,
            'energy_saved_kwh': energy_saved,
            'co2_saved_kg': co2_saved,
            'trees_equivalent': co2_saved * self.FACTORS['trees_per_co2'],
            'people_supported': water_saved_liters / 365 / 50  # 50 liters per person per day
        }

    def calculate_diet_impact(self, meals_replaced: int, meal_type: str = 'meat') -> Dict[str, float]:
        """
        Calculate impact of dietary changes.
        
        Args:
            meals_replaced: Number of meals replaced
            meal_type: Type of meal being replaced (meat, dairy)
        
        Returns:
            Diet impact metrics
        """
        if meal_type == 'meat':
            co2_per_meal = 5  # kg CO2 per meat meal
        elif meal_type == 'dairy':
            co2_per_meal = 2  # kg CO2 per dairy meal
        else:
            co2_per_meal = 0

        co2_saved = meals_replaced * co2_per_meal
        trees_equivalent = co2_saved * self.FACTORS['trees_per_co2']

        return {
            'meals_replaced': meals_replaced,
            'co2_saved_kg': co2_saved,
            'trees_equivalent': trees_equivalent,
            'water_saved_liters': meals_replaced * 1000,  # Approximate water saved
            'land_saved_sq_meters': meals_replaced * 20  # Approximate land saved
        }

    def calculate_transport_impact(self, km_replaced: float, transport_type: str = 'car') -> Dict[str, float]:
        """
        Calculate impact of sustainable transport.
        
        Args:
            km_replaced: Kilometers replaced
            transport_type: Type of transport being replaced (car, flight)
        
        Returns:
            Transport impact metrics
        """
        if transport_type == 'car':
            co2_per_km = 0.2
        elif transport_type == 'flight':
            co2_per_km = 0.25
        else:
            co2_per_km = 0

        co2_saved = km_replaced * co2_per_km
        trees_equivalent = co2_saved * self.FACTORS['trees_per_co2']

        return {
            'km_replaced': km_replaced,
            'transport_type': transport_type,
            'co2_saved_kg': co2_saved,
            'trees_equivalent': trees_equivalent,
            'calories_burned': km_replaced * 50 if transport_type == 'car' else 0  # Walking/cycling
        }

    def calculate_combined_impact(self, actions: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate combined impact of multiple actions.
        
        Args:
            actions: List of action dictionaries
        
        Returns:
            Combined impact metrics
        """
        total_co2 = 0
        total_water = 0
        total_trees = 0
        total_energy = 0

        for action in actions:
            action_type = action.get('type', '')
            amount = action.get('amount', 0)

            if action_type == 'solar':
                impact = self.calculate_co2_impact('energy', amount * 1000)  # Convert to kWh
            elif action_type == 'ev':
                impact = self.calculate_co2_impact('driving', amount)
            elif action_type == 'water':
                impact = self.calculate_water_impact(amount)
            elif action_type == 'diet':
                impact = self.calculate_diet_impact(amount, action.get('meal_type', 'meat'))
            elif action_type == 'transport':
                impact = self.calculate_transport_impact(amount, action.get('transport_type', 'car'))
            else:
                impact = {}

            total_co2 += impact.get('co2_saved_kg', 0)
            total_water += impact.get('water_saved_liters', 0)
            total_trees += impact.get('trees_equivalent', 0)
            total_energy += impact.get('energy_saved_kwh', 0)

        return {
            'total_co2_saved_kg': total_co2,
            'total_water_saved_liters': total_water,
            'total_trees_equivalent': total_trees,
            'total_energy_saved_kwh': total_energy,
            'actions_count': len(actions)
        }

    def get_impact_equivalent(self, co2_kg: float) -> Dict[str, Any]:
        """
        Get equivalent impact metrics for a given CO2 amount.
        
        Args:
            co2_kg: CO2 amount in kg
        
        Returns:
            Equivalent impact metrics
        """
        return {
            'co2_kg': co2_kg,
            'trees': co2_kg / 22,
            'car_km': co2_kg / 0.2,
            'kwh': co2_kg / 0.4,
            'meals': co2_kg / 5,
            'water_liters': co2_kg / 0.002,
            'flight_km': co2_kg / 0.25
        }