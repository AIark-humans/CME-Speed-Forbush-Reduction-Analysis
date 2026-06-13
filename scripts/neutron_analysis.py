import pandas as pd
import numpy as np
import glob
import os

def analyze_neutron_data():
    folder_path = "data"
    csv_files = sorted(glob.glob(os.path.join(folder_path, "NeutronData*.csv")))
    
    print(f"Found {len(csv_files)} neutron data files\n")
    
    all_uncorrected = []
    all_corrected = []
    stats_list = []
    
    for file in csv_files:
        try:
            filename = os.path.basename(file)
            year = filename.replace("NeutronData", "").replace(".csv", "")
            
            df = pd.read_csv(file)
            
            uncorrected = df['UncorrectedCountRate[cts/min]'].values
            corrected = df['CorrectedCountRate[cts/min]'].values
            

            all_uncorrected.extend(uncorrected)
            all_corrected.extend(corrected)
            

            stats = {
                'Year': year,
                'Uncorrected_Std': np.std(uncorrected),
                'Uncorrected_Mean': np.mean(uncorrected),
                'Uncorrected_Min': np.min(uncorrected),
                'Uncorrected_Max': np.max(uncorrected),
                'Corrected_Std': np.std(corrected),
                'Corrected_Mean': np.mean(corrected),
                'Corrected_Min': np.min(corrected),
                'Corrected_Max': np.max(corrected),
                'Count': len(uncorrected)
            }
            stats_list.append(stats)
            
            print(f"{year}:")
            print(f"  Uncorrected - Std: {stats['Uncorrected_Std']:.2f}, Mean: {stats['Uncorrected_Mean']:.2f}")
            print(f"  Corrected   - Std: {stats['Corrected_Std']:.2f}, Mean: {stats['Corrected_Mean']:.2f}")
            print(f"  Data points: {len(uncorrected)}\n")
            
        except Exception as e:
            print(f"Error reading {file}: {e}\n")
    

    print("\n" + "="*60)
    print("OVERALL STATISTICS (All Years Combined)")
    print("="*60)
    print(f"Total data points: {len(all_uncorrected)}")
    print(f"\nUncorrected Count Rate:")
    print(f"  Mean: {np.mean(all_uncorrected):.2f} cts/min")
    print(f"  Std Dev: {np.std(all_uncorrected):.2f} cts/min")
    print(f"  Min: {np.min(all_uncorrected):.2f} cts/min")
    print(f"  Max: {np.max(all_uncorrected):.2f} cts/min")
    
    print(f"\nCorrected Count Rate:")
    print(f"  Mean: {np.mean(all_corrected):.2f} cts/min")
    print(f"  Std Dev: {np.std(all_corrected):.2f} cts/min")
    print(f"  Min: {np.min(all_corrected):.2f} cts/min")
    print(f"  Max: {np.max(all_corrected):.2f} cts/min")
    
    summary_df = pd.DataFrame(stats_list)
    return summary_df

if __name__ == "__main__":
    summary = analyze_neutron_data()
