import pandas as pd
import re

def classify_by_keywords(row):
    """Classifies location based on keywords in name or address."""
    text = f"{row['LocName']} {row['address']}".lower()
    
    patterns = {
        'Hotel/Lodging': r'\b(hotel|motel|inn|suites|resort|lodging)\b',
        'Shopping Center': r'\b(mall|plaza|shopping|centre|center)\b',
        'Gas Station': r'\b(gas station|fuel|petrol)\b',
        'Restaurant': r'\b(restaurant|cafe|diner|eatery)\b',
        'Park/Recreation': r'\b(park|recreation|trail|garden)\b',
    }
    
    for category, pattern in patterns.items():
        if re.search(pattern, text):
            return category
    
    return "Other"

# Example usage
df = pd.read_csv("locations.csv")  # Replace with your CSV file path
df['KeywordClassification'] = df.apply(classify_by_keywords, axis=1)
