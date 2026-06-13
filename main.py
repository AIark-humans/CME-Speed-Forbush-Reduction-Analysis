import sys
import numpy as np
sys.path.insert(0, "scripts") 

from forbush import normalRate, minimumRate, forbushReduction, possionError
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

if __name__ == "__main__":


    folder_path = "data/CMEdata"
    csv_files = sorted(glob.glob(os.path.join(folder_path, "*.csv")))
    velocities = []
    reductions = []
    energy = []
    error = []
    normals = []
    for file in csv_files:
        set = False
        
        try:
            name = os.path.basename(file)
            name = name.strip("CME").rstrip(".csv")
            name.split("_")
            year = int(name.split("_")[0])  
            month = int(name.split("_")[1])
            day = int(name.split("_")[2])
            df = pd.read_csv("data/CleanedCMEData.csv")
            reduction = forbushReduction(year, month, day)
            if np.isnan(reduction):
                continue
            if reduction < 1 or reduction > 99.9: #Filtering for strong events only, switch to 3 for more data points
                #print(f"Filtered reduction for {year}/{month}/{day}: {reduction:.2f}%")
                continue
            for cme in df.itertuples():
                if cme[1] == f"{year}/{month:02d}/{day:02d}":
                    if cme[5] != '----':
                        velocities.append(float(cme[5]))
                        reductions.append(reduction)
                        energy.append(float(cme[6].strip("*")))
                        error.append(possionError(year, month, day))
                        normals.append(normalRate(year, month, day))
                        print(f"Added data for {year}/{month}/{day}: Speed={cme[5]} km/s, Energy={cme[6]} J, Reduction={reduction:.2f}%")
                    set = True
            if not set:
                print(f"No CME data for {year}/{month}/{day}")
        except Exception as e:
            print(f"Error with {file}: {e}")

    print(f"Num Velocities: {len(velocities)}")
    print(f"Num Reductions: {len(reductions)}")
    
    # Diagnostics
    reductions_array = np.array(reductions, dtype=float)
    print(f"\nReductions stats:")
    print(f"  NaN count: {np.isnan(reductions_array).sum()}")
    print(f"  Min: {np.nanmin(reductions_array)}")
    print(f"  Max: {np.nanmax(reductions_array)}")
    print(f"  Mean: {np.nanmean(reductions_array)}")
    print(f"  Std: {np.nanstd(reductions_array)}")
    
    velocities = np.array(velocities, dtype=float)
    reductions = np.array(reductions, dtype=float)
    energy = np.array(energy, dtype=float)

    # regression line
    m, b = np.polyfit(velocities, reductions, 1)
    x_line = np.linspace(np.min(velocities), np.max(velocities), 100)
    y_line = m * x_line + b

    print(f"Best-fit line: reduction = {m:.6f} * speed + {b:.6f}")
    print(f"Slope (m): {m:.6f}")
    print(f"Intercept (b): {b:.6f}")

    plt.scatter(velocities, reductions)
    plt.plot(x_line, y_line, color='red', label=f"Fit: y={m:.3e}x+{b:.3f}")
    plt.xlabel("CME Speed (km/s)")
    plt.ylabel("Forbush Reduction (%)")
    plt.title("CME Speed vs Forbush Reduction")
    plt.legend()
    plt.grid(True) 
    plt.savefig("graphs\\all_speed_vs_forbush.png") 
    plt.show()
    


r = np.corrcoef(velocities, reductions)[0, 1]
print(np.std(velocities))
print(np.std(reductions))
print(f"Correlation coefficient: {r:.2f}")
print(F"Average Maximum Error: {np.average(error)}")
print(F"Average Fractional Maximum Error: {np.average(error)/np.average(normals)}")




    
