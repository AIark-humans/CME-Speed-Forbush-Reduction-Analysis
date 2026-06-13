import pandas as pd
import matplotlib.pyplot as plt
import glob
import os


folder_path = "data/CMEdata"
csv_files = sorted(glob.glob(os.path.join(folder_path, "*.csv")))
print(f"Found {len(csv_files)} CSV files.")

for file in csv_files:
    try:
        print(f"\nOpening: {os.path.basename(file)}")

        df = pd.read_csv(file)

        x_col = df.columns[0]  
        counts = df.columns[1] 

        plt.figure(figsize=(12, 5))
        plt.plot(df[x_col], df[counts])

        plt.title(os.path.basename(file))
        plt.xlabel(x_col)
        plt.ylabel(counts)

        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"Error with {file}: {e}")
