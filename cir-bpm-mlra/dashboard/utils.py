def get_recommendation(risk):
    if risk == "Normal":
        return "Maintain healthy diet, drink enough water, 30 min walking daily."
    elif risk == "Alert":
        return "Reduce salt intake, avoid junk food, daily exercise recommended."
    elif risk == "Warning":
        return "Monitor BP twice daily, avoid stress, consult doctor within 48 hours."
    elif risk == "Emergency":
        return "Immediate hospital visit, avoid physical exertion."
    else:
        return "No recommendation available"