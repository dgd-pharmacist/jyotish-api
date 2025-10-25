"""
Planetary strength calculations - Shad-Bala, Avastha, etc.
"""
import swisseph as swe


def compute_avastha(lon):
    """Calculate Avastha (age state) of a planet"""
    deg_in_sign = lon % 30
    if deg_in_sign < 6:
        return "Bala (infant)"
    elif deg_in_sign < 12:
        return "Kumara (youth)"
    elif deg_in_sign < 18:
        return "Yuva (young adult)"
    elif deg_in_sign < 24:
        return "Vriddha (old)"
    else:
        return "Mrita (dead)"


def compute_shadbala(jd_ut, lat, lon, planet_data):
    """
    Calculate simplified Shad-Bala (sixfold strength) for planets
    Note: This is a simplified version. Full Shad-Bala is extremely complex.
    """
    # Natural strengths (Naisargika bala)
    naisargika = {
        "Sun": 60, "Moon": 51.43, "Mercury": 25.71,
        "Venus": 42.85, "Mars": 17.14, "Jupiter": 34.28, "Saturn": 8.57
    }
    
    # Get sunrise for Kala bala
    try:
        sunrise_result = swe.rise_trans(jd_ut, swe.SUN, lon, lat, rsmi=swe.CALC_RISE)
        sunrise_jd = sunrise_result[1][0] if isinstance(sunrise_result[1], tuple) else sunrise_result[1]
    except:
        sunrise_jd = jd_ut
    
    strengths = {}
    planet_ids = {"Sun":swe.SUN, "Moon":swe.MOON, "Mercury":swe.MERCURY,
                  "Venus":swe.VENUS, "Mars":swe.MARS, "Jupiter":swe.JUPITER, "Saturn":swe.SATURN}
    
    for name, pid in planet_ids.items():
        result = swe.calc_ut(jd_ut, pid)
        lon_planet = result[0][0]
        speed = result[0][3] if len(result[0]) > 3 else 0
        
        # 1. Sthana bala (positional strength) - simplified
        sthana = 30 + (lon_planet % 30)
        
        # 2. Dig bala (directional strength) - simplified
        dig = 30
        
        # 3. Kala bala (temporal strength) - day/night
        is_day = (jd_ut - sunrise_jd) % 1.0 < 0.5
        if name in ["Sun", "Jupiter", "Venus"] and is_day:
            kala = 30
        elif name in ["Moon", "Mars", "Saturn"] and not is_day:
            kala = 30
        else:
            kala = 15
        
        # 4. Cheshta bala (motional strength)
        cheshta = 60 if speed < 0 else 30
        
        # 5. Naisargika bala (natural strength)
        nais = naisargika.get(name, 30)
        
        # 6. Drik bala (aspectual strength) - simplified
        drik = 25
        
        # Total strength
        total = sthana + dig + kala + cheshta + nais + drik
        
        # Avastha
        avastha = compute_avastha(lon_planet)
        
        strengths[name] = {
            "sthana_bala": round(sthana, 2),
            "dig_bala": round(dig, 2),
            "kala_bala": round(kala, 2),
            "cheshta_bala": round(cheshta, 2),
            "naisargika_bala": round(nais, 2),
            "drik_bala": round(drik, 2),
            "total_bala": round(total, 2),
            "strength_percentage": round((total / 390) * 100, 1),
            "avastha": avastha
        }
    
    return strengths
