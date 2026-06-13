import pandas as pd

def normalRate(year, month, day):
    df = pd.read_csv(f"data/CMEdata/CME{year}_{month}_{day}.csv")
    return df["Counts"][0:48].mean()

def minimumRate(year, month, day):
    df = pd.read_csv(f"data/CMEdata/CME{year}_{month}_{day}.csv")
    return df["Counts"][48:].min()

def forbushReduction(year, month, day):
    normal = normalRate(year, month, day)
    minimum = minimumRate(year, month, day)
    if normal <= 0:
        print(f"Warning: normalRate for {year}/{month}/{day} is {normal} (invalid)")
        return float('nan')
    if minimum < 0:
        print(f"Warning: minimumRate for {year}/{month}/{day} is {minimum} (invalid)")
        return float('nan')
    reduction = (normal - minimum) / normal * 100
    return reduction

def possionError(year, month, day):
    normal = normalRate(year, month, day)
    error = normal ** (1/2)
    return error