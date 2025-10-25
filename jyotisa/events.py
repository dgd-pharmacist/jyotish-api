"""
Event-house mapping logic for life area analysis
"""

# Event to house mapping based on classical Vedic astrology
EVENT_HOUSES = {
    "education": [2, 4, 5, 9],
    "career": [2, 6, 10, 11],
    "profession": [6, 10, 11],
    "marriage": [2, 7, 8],
    "relationships": [5, 7, 11],
    "health": [1, 6, 8, 12],
    "wealth": [2, 5, 9, 11],
    "property": [4, 11],
    "children": [5, 9],
    "spiritual": [1, 5, 9, 12],
    "foreign_travel": [3, 9, 12],
    "legal_matters": [6, 7, 9],
    "creativity": [3, 5],
    "communication": [2, 3],
    "family": [2, 4]
}


def get_relevant_houses(event_type):
    """Get house numbers relevant to a specific life event"""
    return EVENT_HOUSES.get(event_type.lower(), [])


def analyze_event_potential(event_type, chart, dasha_lord):
    """Analyze potential for a specific event based on houses and dasha lord"""
    relevant_houses = get_relevant_houses(event_type)
    
    if not relevant_houses:
        return {"error": f"Unknown event type: {event_type}"}
    
    # Check if dasha lord is in relevant houses
    asc_sign = int(chart["Ascendant"]["longitude"] / 30)
    
    if dasha_lord in chart:
        planet_sign = int(chart[dasha_lord]["longitude"] / 30)
        house_position = (planet_sign - asc_sign) % 12 + 1
        
        is_relevant = house_position in relevant_houses
        
        return {
            "event": event_type,
            "relevant_houses": relevant_houses,
            "dasha_lord": dasha_lord,
            "lord_house": house_position,
            "favorable": is_relevant,
            "note": f"{dasha_lord} is in house {house_position}, " + 
                    ("which is favorable for " if is_relevant else "which may not directly indicate ") + event_type
        }
    
    return {"error": f"Dasha lord {dasha_lord} not found in chart"}
