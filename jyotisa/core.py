"""
Core Swiss Ephemeris utilities and position calculations
"""
import swisseph as swe
from datetime import datetime, timedelta


def compute_positions(date, time, timezone_offset, lat, lon, ayanamsa="LAHIRI"):
    """Compute planetary positions and basic chart data"""
    # Parse date and time
    date_parts = [int(x) for x in date.split("-")]
    time_parts = [int(x) for x in time.split(":")]
    utc_dt = datetime(date_parts[0], date_parts[1], date_parts[2],
                      time_parts[0], time_parts[1]) - timedelta(hours=timezone_offset)
    
    # Calculate Julian Day
    jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                       utc_dt.hour + utc_dt.minute/60.0)
    
    # Set ayanamsa
    ayanamsa_map = {
        "LAHIRI": swe.SIDM_LAHIRI,
        "RAMAN": swe.SIDM_RAMAN,
        "KRISHNAMURTI": swe.SIDM_KRISHNAMURTI
    }
    swe.set_sid_mode(ayanamsa_map.get(ayanamsa, swe.SIDM_LAHIRI))
    
    # Calculate planetary positions
    planets = {"Sun":swe.SUN, "Moon":swe.MOON, "Mercury":swe.MERCURY,
               "Venus":swe.VENUS, "Mars":swe.MARS, "Jupiter":swe.JUPITER,
               "Saturn":swe.SATURN, "Rahu":swe.MEAN_NODE}
    
    sign_names = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
                  "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
    
    planet_data = {}
    planet_lons = {}
    
    for name, pid in planets.items():
        result = swe.calc_ut(jd_ut, pid)
        lon = result[0][0] % 360.0
        speed = result[0][3] if len(result[0]) > 3 else 0
        planet_lons[name] = lon
        planet_data[name] = {
            "longitude": round(lon, 3),
            "sign": sign_names[int(lon/30)],
            "retrograde": speed < 0
        }
    
    # Calculate Ascendant and house cusps
    houses_data = swe.houses(jd_ut, lat, lon)
    cusps = houses_data[0]
    asc = houses_data[1][0]
    
    house_cusps = {str(i+1): round(cusps[i], 3) for i in range(12)}
    
    planet_data["Ascendant"] = {
        "longitude": round(asc, 3),
        "sign": sign_names[int(asc/30)]
    }
    
    return {
        "jd": jd_ut,
        "planets": planet_data,
        "planet_longitudes": planet_lons,
        "ascendant": asc,
        "houses": house_cusps,
        "lat": lat,
        "lon": lon
    }
