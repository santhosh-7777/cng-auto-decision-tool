#!/usr/bin/env python3
"""
CNG Share-Auto Decision Tool — Parimal Debnath (NIT Agartala <-> Motor Stand)
Pure Python 3 standard library only.
"""

import csv
import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

# ==============================================================================
# EDITABLE CONSTANTS (Modify these live during code review)
# ==============================================================================
PEAK_START_HOUR = 16           # 4:00 PM evening rush start
PEAK_END_HOUR = 20             # 8:00 PM evening rush end
MAX_ACCEPTABLE_WAIT_MINS = 7   # Max minutes worth waiting for remaining seats
MIN_SAFE_CNG_LEVEL = "Half"    # Minimum safe CNG level ("Low", "Half", "Full")
SEAT_CAPACITY = 5              # 5-passenger share-auto limit

AVG_DRIVE_MINS = 30.0          # One-way drive time: NIT Agartala <-> Motor Stand
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.csv")
HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
CNG_RANK = {"Low": 1, "Half": 2, "Full": 3}


def get_csv_metrics() -> dict:
    """Reads data.csv live on every request and skips bad rows without crashing."""
    trips = []
    skipped = 0

    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as f:
        for line_num, row in enumerate(csv.DictReader(f), start=2):
            try:
                t1 = datetime.strptime(row["arrival_time"].strip(), "%H:%M:%S")
                t2 = datetime.strptime(row["departure_time"].strip(), "%H:%M:%S")
                wait_mins = (t2 - t1).total_seconds() / 60.0
                pax = int(row["passengers_boarded"])
                fare = float(row["fare_per_passenger_inr"])
                refill = float(row["refill_queued_mins"])
                cng = row["cng_level"].strip().capitalize()

                if wait_mins <= 0 or not (1 <= pax <= SEAT_CAPACITY) or fare <= 0 or refill < 0 or cng not in CNG_RANK:
                    raise ValueError("Out-of-range value")

                trips.append({
                    "is_peak": PEAK_START_HOUR <= t1.hour < PEAK_END_HOUR,
                    "wait": wait_mins,
                    "pax": pax,
                    "rev": pax * fare,
                    "fare": fare,
                    "refill": refill,
                })
            except Exception as err:
                skipped += 1
                print(f"[CSV WARNING] Skipping line {line_num}: {err}")

    if not trips:
        return {"valid": 0, "skipped": skipped, "avg_gap": 2.5, "peak_gap": 1.8, "offpeak_gap": 3.5,
                "avg_wait": 8.0, "avg_fare": 30.0, "peak_rate": 240.0, "offpeak_rate": 160.0,
                "peak_refill": 32.0, "offpeak_refill": 11.0}

    peak = [t for t in trips if t["is_peak"]] or trips
    offpeak = [t for t in trips if not t["is_peak"]] or trips

    def calc_gap(group):
        return sum(t["wait"] for t in group) / sum(max(1, t["pax"] - 1) for t in group)

    def calc_rate(group):
        return (sum(t["rev"] for t in group) / sum(t["wait"] + AVG_DRIVE_MINS for t in group)) * 60.0

    peak_refills = [t["refill"] for t in peak if t["refill"] > 0]
    off_refills = [t["refill"] for t in offpeak if t["refill"] > 0]

    return {
        "valid": len(trips),
        "skipped": skipped,
        "avg_gap": round(calc_gap(trips), 2),
        "peak_gap": round(calc_gap(peak), 2),
        "offpeak_gap": round(calc_gap(offpeak), 2),
        "avg_wait": round(sum(t["wait"] for t in trips) / len(trips), 2),
        "avg_fare": round(sum(t["fare"] for t in trips) / len(trips), 2),
        "peak_rate": round(calc_rate(peak), 2),
        "offpeak_rate": round(calc_rate(offpeak), 2),
        "peak_refill": round(sum(peak_refills) / len(peak_refills), 1) if peak_refills else 32.0,
        "offpeak_refill": round(sum(off_refills) / len(off_refills), 1) if off_refills else 11.0,
    }


def make_decision(pax: int, cng: str, hour: int, m: dict) -> dict:
    """Applies economic opportunity-cost logic to return Action, Color, and Rupee Math."""
    is_peak = PEAK_START_HOUR <= hour < PEAK_END_HOUR
    rate = m["peak_rate"] if is_peak else m["offpeak_rate"]
    gap = m["peak_gap"] if is_peak else m["offpeak_gap"]
    seats_left = max(0, SEAT_CAPACITY - pax)

    # Rule 1: Refill if CNG is below safe threshold
    if CNG_RANK[cng] < CNG_RANK[MIN_SAFE_CNG_LEVEL]:
        rush_loss = round((m["peak_refill"] / 60.0) * m["peak_rate"], 1)
        now_loss = round((m["offpeak_refill"] / 60.0) * rate, 1)
        saved = max(0.0, round(rush_loss - now_loss, 1))
        return {
            "action": "REFILL CNG NOW",
            "color": "red",
            "wait_est": 0.0,
            "extra_fare": 0.0,
            "idle_cost": rush_loss,
            "is_peak": is_peak,
            "explanation": (
                f"CNG is {cng} (below {MIN_SAFE_CNG_LEVEL}). Peak pump queues average {m['peak_refill']} min "
                f"(losing ₹{rush_loss:.0f} at ₹{m['peak_rate']:.0f}/hr) vs {m['offpeak_refill']} min off-peak. "
                f"Refilling now saves ~₹{saved:.0f} in lost rush-hour fares."
            ),
        }

    # Rule 2: Full 5-seat auto leaves immediately
    if seats_left == 0:
        return {
            "action": "LEAVE NOW",
            "color": "green",
            "wait_est": 0.0,
            "extra_fare": 0.0,
            "idle_cost": 0.0,
            "is_peak": is_peak,
            "explanation": (
                f"Full auto ({SEAT_CAPACITY}/{SEAT_CAPACITY} seats = ₹{SEAT_CAPACITY * m['avg_fare']:.0f}). "
                f"Every extra minute parked burns ₹{rate / 60.0:.2f}/min. Depart for {'Motor Stand' if hour < 14 else 'NIT Agartala'} now."
            ),
        }

    # Rule 3: Compare extra seat revenue vs waiting opportunity cost
    wait_est = round(seats_left * gap, 1)
    extra_fare = round(seats_left * m["avg_fare"], 1)
    idle_cost = round((wait_est / 60.0) * rate, 1)

    if wait_est <= MAX_ACCEPTABLE_WAIT_MINS and extra_fare >= idle_cost:
        return {
            "action": "WAIT FOR FULL AUTO",
            "color": "blue",
            "wait_est": wait_est,
            "extra_fare": extra_fare,
            "idle_cost": idle_cost,
            "is_peak": is_peak,
            "explanation": (
                f"Wait for {seats_left} more rider(s) (~{wait_est} min at {gap} min/pax, within {MAX_ACCEPTABLE_WAIT_MINS} min limit). "
                f"Extra fare (+₹{extra_fare:.0f}) beats stand idle cost (₹{idle_cost:.1f} at ₹{rate:.0f}/hr)."
            ),
        }

    return {
        "action": "LEAVE NOW",
        "color": "green",
        "wait_est": wait_est,
        "extra_fare": extra_fare,
        "idle_cost": idle_cost,
        "is_peak": is_peak,
        "explanation": (
            f"Roll now with {pax}/{SEAT_CAPACITY} riders (₹{pax * m['avg_fare']:.0f} locked in). "
            f"Waiting for {seats_left} more seat(s) takes ~{wait_est} min (limit: {MAX_ACCEPTABLE_WAIT_MINS} min) "
            f"and costs ₹{idle_cost:.1f} in lost road time."
        ),
    }


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            with open(HTML_PATH, "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)
        elif parsed.path == "/api/decision":
            q = parse_qs(parsed.query)
            pax = max(1, min(SEAT_CAPACITY, int(q.get("passengers", ["3"])[0])))
            cng = q.get("cng", ["Half"])[0].capitalize()
            cng = cng if cng in CNG_RANK else "Half"
            hour = int(q["hour"][0]) if q.get("hour", [""])[0] != "" else datetime.now().hour

            metrics = get_csv_metrics()
            decision = make_decision(pax, cng, hour, metrics)
            payload = json.dumps({"hour": hour, "capacity": SEAT_CAPACITY, "metrics": metrics, "decision": decision}).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(payload)
        else:
            self.send_error(404)


if __name__ == "__main__":
    print(f"Running at http://localhost:8000 | Route: NIT Agartala <-> Motor Stand | Seats: {SEAT_CAPACITY}")
    HTTPServer(("0.0.0.0", 8000), AppHandler).serve_forever()