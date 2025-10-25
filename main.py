# main.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
from datetime import datetime

# Import our jyotisa modules
from jyotisa import core, dashas, divisional, transits, strengths, yogas, events

app = FastAPI(
    title="Swiss Ephemeris API - Professional Jyotish Engine",
    version="3.0",
    description="Complete Vedic Astrology calculation system with modular architecture"
)


# ----------  Request schemas ----------
class ChartRequest(BaseModel):
    date: str  # "1984-06-22"
    time: str  # "09:05"
    timezone_offset: float  # +5.5
    lat: float
    lon: float
    ayanamsa: str = "LAHIRI"  # Options: LAHIRI, RAMAN, KRISHNAMURTI


# ----------  Main Chart Endpoint ----------
@app.post("/compute_chart")
def compute_chart(req: ChartRequest):
    """
    Compute complete birth chart with all astrological calculations

    Returns:
    - Planetary positions (tropical + sidereal)
    - House cusps
    - Divisional charts (D1, D9, D10, D12, D20, D24, D30, D60)
    - Vimshottari Dasha periods
    - Shad-Bala planetary strengths
    - Vedic & Western aspects
    - Yoga detections
    """
    # Core planetary positions
    chart_data = core.compute_positions(req.date, req.time,
                                        req.timezone_offset, req.lat, req.lon,
                                        req.ayanamsa)

    # Vimshottari Dasha
    vim_dasha = dashas.compute_vimshottari(chart_data["jd"])
    vim_dasha["antardasha"] = dashas.compute_antardasha(vim_dasha)

    # Divisional charts
    div_charts = divisional.compute_divisionals(
        chart_data["planets"],
        chart_data["ascendant"],
        scheme=[1, 9, 10, 12, 20, 24, 30, 60])

    # Planetary strengths
    shadbala = strengths.compute_shadbala(chart_data["jd"], chart_data["lat"],
                                          chart_data["lon"],
                                          chart_data["planets"])

    # Aspects
    vedic_asp = yogas.vedic_aspects(chart_data["planets"])
    western_asp = yogas.western_aspects(chart_data["planets"], orb=6)

    # Yoga detection
    asc_sign_index = int(chart_data["ascendant"] / 30)
    detected_yogas = yogas.detect_yogas(chart_data["planets"], vedic_asp,
                                        asc_sign_index)

    return {
        "ayanamsa": req.ayanamsa,
        "chart": chart_data["planets"],
        "houses": chart_data["houses"],
        "divisional": div_charts,
        "vimshottari": vim_dasha,
        "shadbala": shadbala,
        "aspects": {
            "vedic": vedic_asp,
            "western": western_asp
        },
        "yogas": detected_yogas
    }


# ----------  Transit Endpoint ----------
@app.get("/transit_now")
def transit_now(lat: float, lon: float):
    """
    Get current planetary transits for a given location

    Parameters:
    - lat: Latitude
    - lon: Longitude

    Returns current positions of all planets
    """
    current = transits.current_transits(lat, lon)

    return {"date_utc": datetime.utcnow().isoformat(), "transit": current}


# ----------  Transit Hits Endpoint ----------
@app.post("/transit_hits")
def compute_transit_hits(req: ChartRequest,
                         orb: float = Query(3.0,
                                            description="Orb in degrees")):
    """
    Compare current transits with natal chart to find active conjunctions

    Returns all transiting planets making exact aspects to natal planets
    """
    # Get natal chart
    natal = core.compute_positions(req.date, req.time, req.timezone_offset,
                                   req.lat, req.lon, req.ayanamsa)

    # Get current transits
    current = transits.current_transits(req.lat, req.lon)

    # Find hits
    hits = transits.compute_transit_hits(natal["planets"], current, orb)

    return {
        "date_utc": datetime.utcnow().isoformat(),
        "natal_date": req.date,
        "transit_hits": hits,
        "total_hits": len(hits)
    }


# ----------  Event Analysis Endpoint ----------
@app.post("/analyze_event")
def analyze_event(
    req: ChartRequest,
    event_type: str = Query(
        ...,
        description=
        "Event type: education, career, marriage, health, wealth, etc.")):
    """
    Analyze chart for potential of specific life events

    Parameters:
    - event_type: Type of event (education, career, marriage, health, wealth, property, etc.)

    Returns analysis based on house activation and dasha lord
    """
    # Get chart
    chart_data = core.compute_positions(req.date, req.time,
                                        req.timezone_offset, req.lat, req.lon,
                                        req.ayanamsa)

    # Get current dasha
    vim_dasha = dashas.compute_vimshottari(chart_data["jd"])
    current_dasha_lord = vim_dasha["ruler"]

    # Analyze event potential
    analysis = events.analyze_event_potential(event_type,
                                              chart_data["planets"],
                                              current_dasha_lord)

    # Add relevant houses info
    relevant_houses = events.get_relevant_houses(event_type)

    return {
        "event_type": event_type,
        "relevant_houses": relevant_houses,
        "current_dasha_lord": current_dasha_lord,
        "analysis": analysis
    }


# ----------  Health Check ----------
@app.get("/")
def root():
    """API health check and information"""
    return {
        "service":
        "Swiss Ephemeris API - Jyotish Engine",
        "version":
        "3.0",
        "status":
        "active",
        "features": [
            "Planetary positions (Lahiri/Raman/Krishnamurti ayanamsa)",
            "Vimshottari Dasha & Antardasha", "8 Divisional charts (D1-D60)",
            "Shad-Bala strength calculations", "Vedic & Western aspects",
            "Yoga detection", "Transit analysis", "Event timing analysis"
        ],
        "endpoints": {
            "POST /compute_chart": "Complete birth chart calculation",
            "GET /transit_now": "Current planetary transits",
            "POST /transit_hits": "Transit conjunctions to natal chart",
            "POST /analyze_event": "Event timing analysis",
            "GET /docs": "Interactive API documentation"
        }
    }
