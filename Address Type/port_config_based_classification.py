import pandas as pd

def classify_by_ports(row):
    """Classifies location based on port configuration."""
    if row['Level2Ports'] > 0 or row['Level3Ports'] > 0:
        if row['Level3Ports'] > 0:
            return "EV Charging Station (High Capacity)"
        elif row['Level2Ports'] > 0:
            return "Location with Level 2 Charging"
    return "Other"

# Example usage
df = pd.read_csv("locations.csv")  # Replace with your CSV file path
df['PortClassification'] = df.apply(classify_by_ports, axis=1)
