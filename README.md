# CNG Share-Auto Decision Tool — Parimal Debnath (NIT Agartala ↔ Motor Stand)

- **Built For:** Parimal Debnath (5-passenger CNG share-auto driver)
- **Place:** NIT Agartala Main Gate (Jirania) ↔ Motor Stand (Agartala, West Tripura) & NH-8 CNG Station
- **Dates:** November 19–20, 2026

## What This Tool Does
This is a simple local web app built for **Parimal Debnath**, who drives a 5-seat CNG share-auto daily between NIT Agartala and Motor Stand. Instead of guessing at the stand, he taps two buttons—**how many passengers are seated (1–5)** and **his CNG level (Low, Half, Full)**—and the app reads `data.csv` to tell him whether to **LEAVE NOW**, **WAIT FOR FULL AUTO**, or **REFILL CNG NOW** with exact Rupee numbers.

---

## How to Run It
1. Make sure Python 3 is installed (no extra libraries needed).
2. Open a terminal in this folder and run:

    python app.py

3. Open `http://localhost:8000` in your browser.
4. To test live changes, edit the numbers at the top of `app.py` (`PEAK_START_HOUR`, `PEAK_END_HOUR`, `MAX_ACCEPTABLE_WAIT_MINS`, `MIN_SAFE_CNG_LEVEL`) or add/edit rows in `data.csv`—the app reads `data.csv` fresh on every tap.

---

## Real Output (From My 22-Trip `data.csv`)
When running on my collected data (`22 valid` rows, `0 skipped`), here is an actual output at **5:00 PM (Evening Rush)** with **4 passengers seated** and **Half CNG**:

- **Decision:** `WAIT FOR FULL AUTO`
- **Explanation:** *"Wait for 1 more rider(s) (~1.6 min at 1.63 min/pax, within 7 min limit). Extra fare (+₹30) beats stand idle cost (₹6.5 at ₹245/hr)."*

Raw JSON from `/api/decision`:

    {
      "hour": 17,
      "capacity": 5,
      "metrics": {
        "valid": 22,
        "skipped": 0,
        "avg_gap": 2.41,
        "peak_gap": 1.63,
        "offpeak_gap": 3.45,
        "avg_wait": 8.95,
        "avg_fare": 30.45,
        "peak_rate": 245.12,
        "offpeak_rate": 161.84,
        "peak_refill": 32.0,
        "offpeak_refill": 11.0
      },
      "decision": {
        "action": "WAIT FOR FULL AUTO",
        "color": "blue",
        "wait_est": 1.6,
        "extra_fare": 30.5,
        "idle_cost": 6.5,
        "is_peak": true,
        "explanation": "Wait for 1 more rider(s) (~1.6 min at 1.63 min/pax, within 7 min limit). Extra fare (+₹30) beats stand idle cost (₹6.5 at ₹245/hr)."
      }
    }

---

## What This Tool Gets Wrong
1. **Heavy Rain Rush:** When it rains suddenly near NIT Agartala Gate, stranded students fill all 5 seats in under a minute even at 1:00 PM, so historical off-peak wait times are too slow.
2. **NH-8 Traffic Jams:** Roadblocks or traffic jams near Jirania or Khayerpur can stretch the 30-minute drive to 50+ minutes, which lowers actual hourly earnings compared to the CSV average.
3. **Sudden CNG Pump Shutdowns:** Low gas pressure or compressor issues at the TNGCL CNG station can turn a normal 11-minute off-peak refill into a 60-minute wait.
4. **Full "Reserve" Bookings:** Sometimes students or families pay a flat ₹150–₹180 to book the whole auto immediately; this tool assumes individual ₹30 shared seats.

---