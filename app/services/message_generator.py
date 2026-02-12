def generate_friendly_message(rain_prob: float, temp: float, wind: float) -> str:
    if rain_prob > 70:
        return f"Aïe ! Il y a {rain_prob:.1f}% de chances de pluie 🌧️. Prévoyez un parapluie !"
    elif rain_prob > 40:
        return f"Hmm, il y a {rain_prob:.1f}% de chances de pluie 🌤️. Un parapluie pourrait être utile."
    elif temp < 10:
        return f"Il fera frais ({temp:.1f}°C) ❄️. Habillez-vous chaudement !"
    elif temp > 30:
        return f"Il fera chaud ({temp:.1f}°C) 🔥. N'oubliez pas l'eau et la crème solaire !"
    elif wind > 30:
        return f"Attention, vent fort prévu ({wind:.1f} km/h) 💨 !"
    else:
        return f"Parfait ! Il fera probablement beau pour votre sortie ☀️ ({temp:.1f}°C, {rain_prob:.1f}% pluie)"
