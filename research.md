# Problem
Share-auto drivers on the daily NIT Agartala–Motor Stand route lose peak income (4:00 PM–8:00 PM) guessing when to depart versus waiting for a 5th passenger.
During off-peak lulls, waiting 12+ minutes for one extra ₹30 fare costs more in missed trip turnover than the extra ticket earns.
Entering the 4:00 PM rush with a Low CNG tank traps drivers in 30+ minute shift-change pump queues when hourly earnings peak.
Drivers need a zero-typing rule built on real stand arrival gaps and local CNG pump queue delays.

# Person
- **Name:** Parimal Debnath
- **Role:** Full-time CNG share-auto driver (5-passenger capacity CNG auto-rickshaw)
- **Route / Stand:** NIT Agartala Main Gate (Jirania) &harr; Motor Stand (Agartala, West Tripura) daily corridor
- **Daily Shift Pattern:** Morning college/office wave (8:00 AM–10:30 AM), midday lull, and peak evening rush (4:00 PM–8:00 PM).

# Existing solutions
1. **Visual Road-Scanning & Gut-Feel Guessing at the Stand:**
   - *How it works:* Drivers scan NH-8 / stand approaches for walking students or ask peers when the last auto left.
   - *Why it falls short:* Drivers fall for the sunk-cost trap during off-peak lulls (waiting 14 minutes for a 5th rider) and underestimate how a 30-minute CNG queue wipes out peak ₹/hour earnings.
2. **Generic Ride-Hailing Apps (Ola / Uber / Rapido):**
   - *How it works:* Point-to-point single-party bookings with algorithmic surge pricing and turn-by-turn navigation.
   - *Why it falls short:* They do not model fixed-corridor 5-seat shared boarding (₹30 per passenger), informal stand queues, or local TNGCL CNG station refill bottlenecks.

# Sources
1. **Little, J. D. C. (1961). "A Proof for the Queuing Formula: $L = \lambda W$." *Operations Research*, 9(3), 383–387.**
   - Direct URL: https://pubsonline.informs.org/doi/10.1287/opre.9.3.383
   - **Plain-English Takeaway:**
     Average waiting time ($W$) depends directly on passenger arrival rate ($\lambda$) and remaining empty seats ($L$).
     When arrival rates drop off-peak, the time needed to fill the 4th and 5th seats increases proportionally.
     Measuring empirical arrival gaps lets a driver predict exact expected wait minutes instead of guessing.
2. **Cervero, R., & Golub, A. (2007). "Informal transport: A global perspective." *Transport Policy*, 14(6), 445–457.**
   - Direct URL: https://www.sciencedirect.com/science/article/pii/S0967070X07000376
   - **Plain-English Takeaway:**
     Informal shared-transit drivers operate on "fill-and-go" rules, creating a direct trade-off between stand dwell time and daily trip cycles.
     Over-waiting at terminals for 100% seat occupancy cuts total round-trips completed during high-demand waves.
     Enforcing a strict maximum wait cutoff raises net hourly earnings compared to waiting indefinitely for a full 5-seat load.