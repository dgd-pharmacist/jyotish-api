"""
Yoga (planetary combination) detection
"""


def vedic_aspects(chart):
    """Calculate Vedic (Parashari) aspects for planets"""
    sign_names = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
                  "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
    aspects = {}
    
    for p in chart.keys():
        if p == "Ascendant":
            continue
        lon = chart[p]["longitude"]
        sign = int(lon / 30)
        
        if p in ["Sun","Moon","Mercury","Venus"]:
            targets = [(sign+6)%12]
        elif p == "Mars":
            targets = [(sign+3)%12, (sign+6)%12, (sign+7)%12]
        elif p == "Jupiter":
            targets = [(sign+4)%12, (sign+6)%12, (sign+8)%12]
        elif p in ["Saturn","Rahu"]:
            targets = [(sign+2)%12, (sign+6)%12, (sign+9)%12]
        else:
            targets = []
        
        aspects[p] = [sign_names[t] for t in targets]
    
    return aspects


def western_aspects(chart, orb=6):
    """Calculate Western angular aspects between planets"""
    pairs = []
    names = [k for k in chart.keys() if k != "Ascendant"]
    
    for i, p1 in enumerate(names):
        lon1 = chart[p1]["longitude"]
        for p2 in names[i+1:]:
            lon2 = chart[p2]["longitude"]
            diff = abs((lon1 - lon2 + 180) % 360 - 180)
            
            for angle, label in [(0,"Conjunction"), (60,"Sextile"), (90,"Square"), 
                                  (120,"Trine"), (180,"Opposition")]:
                if abs(diff - angle) <= orb:
                    pairs.append({
                        "planet1": p1,
                        "planet2": p2,
                        "aspect": label,
                        "orb": round(diff - angle, 2),
                        "exact_angle": round(diff, 2)
                    })
    
    return pairs


def detect_yogas(chart, aspects, asc_sign_index):
    """Detect various yogas in the chart"""
    sign_names = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
                  "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
    yogas = []
    
    # Gaja Kesari Yoga
    if "Jupiter" in chart and "Moon" in chart:
        jup_sign = int(chart["Jupiter"]["longitude"] / 30)
        moon_sign = int(chart["Moon"]["longitude"] / 30)
        diff = (jup_sign - moon_sign) % 12
        if diff in [0, 3, 6, 9]:
            yogas.append("Gaja Kesari Yoga (Jupiter-Moon in mutual kendras)")
    
    # Dhana Yoga
    if "Venus" in chart and "Jupiter" in chart:
        ven_sign = int(chart["Venus"]["longitude"] / 30)
        jup_sign = int(chart["Jupiter"]["longitude"] / 30)
        if ven_sign == jup_sign:
            yogas.append("Dhana Yoga (Venus-Jupiter conjunction)")
        elif sign_names[jup_sign] in aspects.get("Venus", []) or sign_names[ven_sign] in aspects.get("Jupiter", []):
            yogas.append("Dhana Yoga (Venus-Jupiter mutual aspect)")
    
    # Budhaditya Yoga
    if "Sun" in chart and "Mercury" in chart:
        sun_sign = int(chart["Sun"]["longitude"] / 30)
        merc_sign = int(chart["Mercury"]["longitude"] / 30)
        if sun_sign == merc_sign:
            yogas.append("Budhaditya Yoga (Sun-Mercury conjunction for intellect)")
    
    # Chandra Mangala Yoga
    if "Moon" in chart and "Mars" in chart:
        moon_sign = int(chart["Moon"]["longitude"] / 30)
        mars_sign = int(chart["Mars"]["longitude"] / 30)
        if moon_sign == mars_sign:
            yogas.append("Chandra Mangala Yoga (Moon-Mars conjunction for wealth)")
    
    # Beneficial planet positions
    kendras = [0, 3, 6, 9]
    trikonas = [0, 4, 8]
    
    for planet in ["Jupiter", "Venus", "Mercury"]:
        if planet in chart:
            planet_sign = int(chart[planet]["longitude"] / 30)
            house_from_asc = (planet_sign - asc_sign_index) % 12
            if house_from_asc in kendras:
                yogas.append(f"Beneficial: {planet} in Kendra house ({house_from_asc + 1})")
            elif house_from_asc in trikonas:
                yogas.append(f"Beneficial: {planet} in Trikona house ({house_from_asc + 1})")
    
    return yogas if yogas else ["No major yogas detected"]
