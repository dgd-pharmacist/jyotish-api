"""
Dasha (time period) calculations - Vimshottari, Yogini, etc.
"""
import swisseph as swe


def compute_vimshottari(jd_ut):
    """Calculate Vimshottari Dasha periods"""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    moon_lon = swe.calc_ut(jd_ut, swe.MOON)[0][0] % 360.0
    nak_index = int(moon_lon / (360.0/27.0))
    nak_frac = (moon_lon % (360.0/27.0)) / (360.0/27.0)
    pada = int(nak_frac * 4) + 1

    nak_names = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu",
                 "Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta",
                 "Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha",
                 "Uttara Ashadha","Shravana","Dhanishta","Shatabhisha",
                 "Purva Bhadrapada","Uttara Bhadrapada","Revati"]

    rulers = ['Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury']*3
    ruler = rulers[nak_index]
    nak_name = nak_names[nak_index]

    dasha_years = {
        'Ketu':7,'Venus':20,'Sun':6,'Moon':10,'Mars':7,
        'Rahu':18,'Jupiter':16,'Saturn':19,'Mercury':17
    }

    rem_frac = 1.0 - nak_frac
    bal_years = dasha_years[ruler] * rem_frac

    seq = ['Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury']*20
    start_index = seq.index(ruler)
    jd = jd_ut
    timeline = []
    
    for i in range(9):
        lord = seq[start_index + i]
        years = dasha_years[lord]
        if i == 0:
            years = bal_years
        start = swe.revjul(jd)
        jd += years * 365.25
        end = swe.revjul(jd)
        timeline.append({
            "lord": lord,
            "start": f"{int(start[0])}-{int(start[1]):02d}-{int(start[2]):02d}",
            "end": f"{int(end[0])}-{int(end[1]):02d}-{int(end[2]):02d}",
            "years": round(years,2)
        })

    return {
        "moon_longitude": round(moon_lon,3),
        "nakshatra": nak_name,
        "pada": pada,
        "ruler": ruler,
        "balance_years": round(bal_years,2),
        "table": timeline
    }


def compute_antardasha(vim):
    """Return Antardasha table for the first (current) Mahadasha"""
    order = ['Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury']
    years_table = {
        'Ketu':7,'Venus':20,'Sun':6,'Moon':10,'Mars':7,
        'Rahu':18,'Jupiter':16,'Saturn':19,'Mercury':17
    }

    first = vim['table'][0]
    start_y, start_m, start_d = map(int, first['start'].split('-'))
    jd = swe.julday(start_y, start_m, start_d)
    mahadasha_years = first['years']
    mahadasha_lord = first['lord']
    seq = order[order.index(mahadasha_lord):] + order[:order.index(mahadasha_lord)]
    subperiods = []
    jd_start = jd

    for lord in seq:
        sub_years = mahadasha_years * (years_table[lord] / 120.0)
        start = swe.revjul(jd_start)
        jd_start += sub_years * 365.25
        end = swe.revjul(jd_start)
        subperiods.append({
            "maha": mahadasha_lord,
            "antar": lord,
            "start": f"{int(start[0])}-{int(start[1]):02d}-{int(start[2]):02d}",
            "end": f"{int(end[0])}-{int(end[1]):02d}-{int(end[2]):02d}",
            "years": round(sub_years,2)
        })
    
    return subperiods
