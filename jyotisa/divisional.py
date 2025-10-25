"""
Divisional chart (Varga) calculations
"""


def get_divisional(longitude, D):
    """Calculate divisional chart position for a given longitude and division"""
    sign_names = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
                  "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
    sign_index = int(longitude / 30)
    part = 30.0 / D
    part_index = int((longitude % 30) / part)
    
    # Classical mapping rules
    if D == 1:  # Rasi (main chart)
        div_sign = sign_index
    elif D == 9:  # Navamsa
        div_sign = (sign_index * D + part_index) % 12
    elif D == 10:  # Dasamsa
        if sign_index % 2 == 0:
            div_sign = (sign_index + part_index) % 12
        else:
            div_sign = (sign_index + part_index + 8) % 12
    elif D == 12:  # Dwadasamsa
        div_sign = (sign_index + part_index) % 12
    elif D == 20:  # Vimsamsa
        if sign_index % 2 == 0:
            div_sign = (3 + part_index) % 12
        else:
            div_sign = (8 + part_index) % 12
    elif D == 24:  # Chaturvimsamsa
        if sign_index % 2 == 0:
            div_sign = (4 + part_index) % 12
        else:
            div_sign = (3 + part_index) % 12
    elif D == 30:  # Trimsamsa
        div_sign = (sign_index * D + part_index) % 12
    elif D == 60:  # Shashtiamsa
        div_sign = (sign_index * D + part_index) % 12
    else:
        # Generic formula
        div_sign = (sign_index * D + part_index) % 12
    
    return sign_names[div_sign]


def compute_divisionals(planets, asc, scheme=[1, 9, 10, 12, 20, 24, 30, 60]):
    """Compute multiple divisional charts"""
    charts = {}
    
    for D in scheme:
        chart = {}
        for planet, data in planets.items():
            if planet != "Ascendant":
                chart[planet] = get_divisional(data['longitude'], D)
        chart["Ascendant"] = get_divisional(asc, D)
        charts[f"D{D}"] = chart
    
    return charts
