import pytest
from water import calculate_water_footprint, GLOBAL_WATER_AVERAGE_LITERS, DIET_VIRTUAL_WATER

def test_calculate_water_footprint_vegan():
    total, contributors = calculate_water_footprint(
        shower_mins_per_day=10,
        laundry_loads_per_week=2,
        dishwasher_runs_per_week=3,
        garden_mins_per_week=14,
        diet="Vegan"
    )
    
    assert total > 0
    assert contributors["Shower"] == 100
    assert contributors["Laundry"] == pytest.approx((2 * 50) / 7.0)
    assert contributors["Dishwasher"] == pytest.approx((3 * 15) / 7.0)
    assert contributors["Garden"] == pytest.approx((14 * 20) / 7.0)
    assert contributors["Diet"] == DIET_VIRTUAL_WATER["Vegan"]

def test_calculate_water_footprint_omnivore():
    total, contributors = calculate_water_footprint(
        shower_mins_per_day=5,
        laundry_loads_per_week=0,
        dishwasher_runs_per_week=0,
        garden_mins_per_week=0,
        diet="Omnivore"
    )
    
    assert contributors["Shower"] == 50
    assert contributors["Diet"] == DIET_VIRTUAL_WATER["Omnivore"]
    assert total == 50 + DIET_VIRTUAL_WATER["Omnivore"]
