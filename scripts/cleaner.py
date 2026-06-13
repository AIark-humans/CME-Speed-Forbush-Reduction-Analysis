import pandas as pd
import matplotlib as plt
from datetime import date as d
import re

input_file = "data/RawCMEData.txt"
output_file = "data/CleanedCMEData.csv"

rows = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue
        parts = re.split(r"\s+", line, maxsplit=11)

        if len(parts) < 12:
            continue
        date = parts[0]
        time = parts[1]
        cpa = parts[2]
        width = parts[3]
        speed = parts[4]
        kinetic_energy = parts[-3]

        if cpa == "Halo" and not "poor" in parts[-1].lower() and not "-" in kinetic_energy:
            rows.append({
            "Date": date,
            "Time": time,
            "CPA": cpa,
            "Width": width,
            "Speed_km_s": speed,
            "KineticEnergy_J": kinetic_energy
            })
df = pd.DataFrame(rows)
df.to_csv(output_file, index=False)
counter = 0
for cme in df.itertuples():
    year, month, day = cme[1].split("/")
    year = int(year)
    month = int(month)
    day = int(day)
    intDateEvent = d(year, month, day).timetuple().tm_yday
    #print(intDateEvent)
    row = []
    df2 = pd.read_csv(f"data/NeutronData{year}.csv")
    counter += 1
    for data in df2.itertuples():
        outfile = f"data/CMEdata/CME{year}_{month}_{day}.csv"
        intDate = data[2]
        if((intDate >= intDateEvent - 2) and (intDate <= intDateEvent + 5)):
            row.append(data[4])

    s = pd.Series(row, name = "Counts")
    s.to_csv(outfile, index = True)
            



        
        







