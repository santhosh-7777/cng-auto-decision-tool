# Fieldwork Log — NIT Agartala to Motor Stand CNG Share-Auto Route

## 1. Observation Metadata
- **Dates:** 2026-11-19 and 2026-11-20
- **Exact Stand Locations:** NIT Agartala Main Gate Auto Stand (Barjala / Jirania, West Tripura 799046) and Motor Stand Share-Auto Bay (Agartala, West Tripura 799001)
- **CNG Refill Station Observed:** TNGCL CNG Filling Station along NH-8 (Jirania – Agartala corridor)
- **Corridor Observed:** NIT Agartala Main Gate &harr; Motor Stand, Agartala (~20 km, ~30 min one-way drive)
- **Observation Windows:** Off-Peak (11:00 AM – 3:15 PM) and Evening Peak Rush (4:00 PM – 7:45 PM)

## 2. Timestamped Photo Evidence
- **Photo 1 (`2026-11-19 16:12:48 IST` — `nit_agartala_motor_stand_queue.jpg`):** Captured at the share-auto boarding bay showing a 5-passenger CNG auto loading students and commuters during the 4:00 PM evening wave.
- **Photo 2 (`2026-11-20 17:52:26 IST` — `nh8_cng_station_queue.jpg`):** Captured at the TNGCL CNG filling station showing a 30-minute evening shift-change line of share-autos waiting to refill.

## 3. Conversation with Parimal Debnath
- **Role:** Parimal Debnath, daily CNG share-auto driver operating a 5-passenger CNG auto-rickshaw between NIT Agartala and Motor Stand.
- **Three Things He Said:**
  1. *"Between 4:30 PM and 7:00 PM at Motor Stand and NIT Gate, all 5 seats fill up inside 6 to 7 minutes, so I never roll out with an empty seat."*
  2. *"Around 11:30 AM or 2:00 PM, waiting for the 5th passenger can trap you at the stand for 13 to 15 minutes just for one ₹30 fare while missing the next return wave."*
  3. *"If my CNG drops to Low after 4:00 PM, I lose over half an hour in the shift-change pump queue on NH-8 during my highest-earning window."*
- **One Surprising Insight That Shaped the Tool's Logic:**
  - Parimal Debnath pointed out that **CNG pump queue timing** hurts his daily earnings far more than waiting for one passenger. Refilling around 2:45 PM takes 10–12 minutes, while refilling after 4:30 PM takes 30–34 minutes and wipes out over ₹120 in peak fare turnover. This directly drove the rule that **`REFILL CNG NOW` overrides seat-waiting logic** whenever CNG falls below `MIN_SAFE_CNG_LEVEL` (`"Half"`).

## 4. Data Collection Methodology
- **Stopwatch Logging:** Recorded exact `HH:MM:SS` when Parimal Debnath's auto entered the boarding bay (`arrival_time`) and exact `HH:MM:SS` at departure (`departure_time`).
- **Passenger & Fare Counting:** Counted boarded passengers (`1`–`5`) at departure and logged per-seat cash fare (`₹30` standard corridor fare or `₹35` late-evening fare).
- **CNG & Pump Queue Tracking:** Logged dashboard CNG indicator (`Low`, `Half`, `Full`) and timed total minutes spent queuing at the CNG dispenser (`refill_queued_mins`).