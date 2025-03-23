def evaluate_crop_health(frame: dict, crop_zones: dict):
    """
    Evaluate crop health based on environmental sensor values.
    Returns a dictionary of crop -> (status, reasons)
    """
    crop_health = {}

    # Extract environment values from the frame
    rh = frame.get("RF_TigerPond_Temp_RH_FEB-2025__RH[%]", None)
    par = frame.get("LEO-W_SQ-110_PAR_umolm-2s-1_FEB-2025__LEO-W_10_2_5", None)
    temp = frame.get("RF_MountainTower_Temp_FEB-2025__Temp_13m[degC]", None)
    co2 = frame.get("Desert_CO2_FEB-2025__CO2_desert[ppm]", None)

    for _, crop in crop_zones.items():
        score = 100
        reasons = []

        # Evaluate RH (Humidity)
        if rh is not None:
            if rh < 30:
                score -= 40
                reasons.append("Low RH")
            elif rh > 80:
                score -= 10
                reasons.append("High RH")

        # Evaluate PAR (Light)
        if par is not None:
            if par < 150:
                score -= 30
                reasons.append("Low PAR")
            elif par > 1800:
                score -= 10
                reasons.append("High PAR")

        # Evaluate Temperature
        if temp is not None:
            if temp < 10:
                score -= 20
                reasons.append("Too Cold")
            elif temp > 35:
                score -= 20
                reasons.append("Too Hot")

        # Evaluate CO2
        if co2 is not None:
            if co2 > 1200:
                score -= 15
                reasons.append("High CO₂")
            elif co2 < 200:
                score -= 10
                reasons.append("Low CO₂")

        # Translate score into health status with emojis
        if score >= 80:
            status = "🌱 Healthy"
        elif score >= 50:
            status = "⚠️ Warning"
        else:
            status = "🥀 Critical"

        if reasons:
            status += " (" + ", ".join(reasons) + ")"

        crop_health[crop] = status

    return crop_health


def crop_color_for_health(health_str):
    """
    Converts emoji+label health string to a display color.
    """
    if "🌱" in health_str:
        return (34, 139, 34)  # Healthy - green
    elif "⚠️" in health_str:
        return (255, 215, 0)  # Warning - yellow
    elif "🥀" in health_str:
        return (139, 69, 19)  # Critical - brown
    else:
        return (180, 180, 180)  # Unknown/neutral - gray