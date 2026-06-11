from recommendations import generate_recommendations

contributors = {
    "Transport": 1533,
    "Electricity": 2460,
    "Diet": 1800,
    "Flights": 500
}

insight, recommendations = generate_recommendations(
    transport="Car",
    electricity=300,
    diet="Non-Vegetarian",
    flights=4,
    contributors=contributors
)

print(insight)

print("\nRecommendations:")
for rec in recommendations:
    print("-", rec)