def generate_recommendations(
    transport,
    electricity,
    diet,
    flights,
    contributors
):
    recommendations = []

    # Find the biggest contributor
    highest_category = max(contributors, key=contributors.get)

    insight = (
        f"Your biggest contributor is {highest_category} "
        f"({contributors[highest_category]:.0f} kg CO₂/year)."
    )

    # Transport suggestions
    if transport == "Car":
        recommendations.append(
            "🚗 Try using public transport or carpooling 1–2 days a week."
        )

    # Electricity suggestions
    if electricity > 250:
        recommendations.append(
            "💡 Reduce electricity use by switching to LED bulbs and turning off unused appliances."
        )

    # Diet suggestions
    if diet == "Non-Vegetarian":
        recommendations.append(
            "🥗 Consider adding 1–2 plant-based meals each week."
        )

    # Flight suggestions
    if flights >= 3:
        recommendations.append(
            "✈️ Reduce non-essential flights or consider carbon offset programs."
        )

    # Default suggestion
    if not recommendations:
        recommendations.append(
            "🌱 Great job! Keep maintaining your sustainable habits."
        )

    return insight, recommendations