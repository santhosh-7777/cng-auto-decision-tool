# AI Chat Export — CNG Share-Auto Decision Tool

- **Project:** CNG Share-Auto Decision Tool (`cng-auto-decision-tool`)
- **Tool Used:** Google Gemini
- **Scope of AI Usage:** Used strictly for **Step 1** (finding queueing theory papers for `research.md`) and **Step 3** (coding `app.py`, `index.html`, and `README.md` templates). **Step 2** (fieldwork, photos, interview with Parimal Debnath, and `data.csv` stopwatch logging) and **Step 4** (`reflection.md`) were completed offline without AI.

---

## Prompt 1 — Step 1: Queueing Theory Papers for Stand Wait Times
**My Prompt:**
> I am studying share-autos outside NIT Agartala Main Gate heading to Motor Stand. Drivers have to decide between waiting at the bay for a 5th passenger (₹30/seat) or leaving early with 3–4 riders. What classic operations research or informal transit papers explain the trade-off between passenger arrival rate, seat occupancy, and stand dwell time?

**AI Response Summary:**
- Recommended **Little's Law** ($L = \lambda W$, John D. C. Little, 1961, *Operations Research*) to estimate expected waiting time from observed arrival gaps and remaining empty seats.
- Recommended **Cervero & Golub (2007)** (*"Informal transport: A global perspective"*, *Transport Policy*) on informal "fill-and-go" transit rules and how terminal wait cutoffs affect daily trip turnover.
- I read both papers and wrote my own 3-line notes in `research.md`.

---

## Prompt 2 — Step 3: Zero-Dependency Python Server & Opportunity-Cost Logic
**My Prompt:**
> Write a simple, zero-dependency Python 3 backend (`app.py`) under 150 lines using only standard library modules (`http.server`, `csv`, `json`, `datetime`). It should read my `data.csv` live on every request, skip malformed CSV rows without crashing, keep thresholds (`PEAK_START_HOUR`, `PEAK_END_HOUR`, `MAX_ACCEPTABLE_WAIT_MINS`, `MIN_SAFE_CNG_LEVEL`, `SEAT_CAPACITY = 5`) at the top of the file for easy live editing, and return JSON decisions (`LEAVE NOW`, `WAIT FOR FULL AUTO`, or `REFILL CNG NOW`).

**AI Response Summary:**
- Generated `app.py` with `BaseHTTPRequestHandler` and `HTTPServer` on port `8000`, serving `index.html` at `/` and JSON metrics/decisions at `/api/decision`.
- Added row-by-row validation in `get_csv_metrics()` so invalid timestamps, out-of-range passenger counts, or bad CNG values are skipped with a console warning while tracking `valid` and `skipped` row counts.

**My Manual Adjustments:**
- After interviewing Parimal Debnath during Step 2 fieldwork, I learned that getting caught in a 30+ minute shift-change queue at the NH-8 TNGCL CNG pump during the 4:00 PM–8:00 PM rush costs him over ₹120 in lost fares—much worse than leaving with one empty seat. I set `REFILL CNG NOW` as the top-priority rule whenever `cng_level` drops below `Half`.
- Set `AVG_DRIVE_MINS = 30.0` and `SEAT_CAPACITY = 5` to match the real NIT Agartala ↔ Motor Stand corridor.

---

## Prompt 3 — Step 3: Mobile-First Two-Tap Web Interface
**My Prompt:**
> Build a single-file mobile-first `index.html` with no external CSS or JS libraries. A driver should only need two big thumb taps—current seated passengers (1 to 5) and CNG level (Low, Half, Full)—plus a time-of-day selector for testing rush vs. off-peak hours and a button to reload `data.csv`.

**AI Response Summary:**
- Created `index.html` using native CSS Grid, large 58px touch buttons, color-coded decision cards (`green`, `blue`, `red`), and `fetch('/api/decision')` updates on every tap.

---

## Prompt 4 — Step 3: README & PowerShell Git Commands
**My Prompt:**
> Help me format `README.md` with local run instructions, sample JSON output, the economic formulas, and limitations, plus PowerShell commands to push my sequential commits to GitHub.

**AI Response Summary:**
- Provided the `README.md` structure and `git add` / `git commit` / `git push` commands. I filled in my fieldwork dates, actual JSON output, limitations, and screen-recording link.