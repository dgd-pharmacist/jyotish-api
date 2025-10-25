"""
Transit calculations - current and progressive transits
"""
import swisseph as swe
from datetime import datetime


def current_transits(lat, lon):
    """Calculate current planetary transits"""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    now = datetime.utcnow()
    jd = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60.0)
    
    planets = {"Sun":swe.SUN, "Moon":swe.MOON, "Mercury":swe.MERCURY,
               "Venus":swe.VENUS, "Mars":swe.MARS, "Jupiter":swe.JUPITER,
               "Saturn":swe.SATURN, "Rahu":swe.MEAN_NODE}
    sign_names = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
                  "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
    data = {}
    
    for name, pid in planets.items():
        result = swe.calc_ut(jd, pid)
        lon = result[0][0] % 360.0
        speed = result[0][3] if len(result[0]) > 3 else 0
        data[name] = {
            "longitude": round(lon, 2),
            "sign": sign_names[int(lon/30)],
            "retrograde": speed < 0
        }
    
    return data


def compute_transit_hits(natal_chart, transiting_planets, orb=3.0):
    """Find transit conjunctions and aspects to natal planets"""
    hits = []
    
    for t_planet, t_data in transiting_planets.items():
        if t_planet == "Ascendant":
            continue
        t_lon = t_data['longitude']
        
        for n_planet, n_data in natal_chart.items():
            if n_planet == "Ascendant":
                continue
            n_lon = n_data['longitude']
            
            # Calculate angular difference
            diff = abs((t_lon - n_lon + 180) % 360 - 180)
            
            # Check for conjunction
            if diff <= orb:
                hits.append({
                    "transit_planet": t_planet,
                    "natal_planet": n_planet,
                    "aspect": "Conjunction",
                    "orb": round(diff, 2),
                    "exact": diff < 1.0
                })
    
    return hits
