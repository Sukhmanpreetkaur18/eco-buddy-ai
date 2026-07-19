import os

# Base line and sensitivity for total footprint (if not using categories)
ECO_SCORE_BASELINE = float(os.environ.get("SCORING_BASELINE", 4000.0))
ECO_SCORE_SENSITIVITY = float(os.environ.get("SCORING_SENSITIVITY", 1000.0))

# Category weights for the eco score calculation
CATEGORY_WEIGHTS = {
    "Transport": float(os.environ.get("WEIGHT_TRANSPORT", 0.3)),
    "Electricity": float(os.environ.get("WEIGHT_ELECTRICITY", 0.3)),
    "Diet": float(os.environ.get("WEIGHT_DIET", 0.25)),
    "Flights": float(os.environ.get("WEIGHT_FLIGHTS", 0.15)),
}
