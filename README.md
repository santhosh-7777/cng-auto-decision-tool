# CNG Share-Auto Decision Tool — Parimal Debnath (NIT Agartala ↔ Motor Stand)

A zero-dependency, mobile-first local web app built for **Parimal Debnath**, who drives a **5-passenger CNG share-auto** daily between **NIT Agartala** and **Motor Stand, Agartala**. With two thumb taps (**Passengers Seated** and **CNG Level**), it reads live trip logs from `data.csv` and recommends **LEAVE NOW**, **WAIT FOR FULL AUTO**, or **REFILL CNG NOW** with exact Rupee math.

---

## 1. Setup & Run Instructions
1. Ensure Python 3.8+ is installed (uses standard library only—no `pip install` needed).
2. Keep `app.py`, `index.html`, and `data.csv` in the same folder and run:
   ```powershell
   python app.py