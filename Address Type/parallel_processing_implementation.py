import pandas as pd
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def classify_with_nlp(df, reference_categories):
    """
    Classifies ambiguous cases using NLP and cosine similarity.
    
    Parameters:
        df: DataFrame containing ambiguous cases.
        reference_categories: Dictionary with reference texts for each category.
        
    Returns:
        DataFrame with NLP-based classifications.
    """
    # Combine location name and address into a single text column
    df['CombinedText'] = df['LocName'] + " " + df['address']
    
    # Generate TF-IDF embeddings for all texts
    vectorizer = TfidfVectorizer(stop_words='english')
    text_embeddings = vectorizer.fit_transform(df['CombinedText'])
    
    # Generate embeddings for reference categories
    reference_texts = list(reference_categories.values())
    reference_embeddings = vectorizer.transform(reference_texts)
    
    # Compute cosine similarity between each text and reference categories
    similarity_scores = cosine_similarity(text_embeddings, reference_embeddings)
    
    # Assign category with highest similarity score
    df['NLPClassification'] = similarity_scores.argmax(axis=1).apply(
        lambda idx: list(reference_categories.keys())[idx]
    )
    
    return df

import pandas as pd

def classify_by_ports(row):
    """Classifies location based on port configuration."""
    if row['Level2Ports'] > 0 or row['Level3Ports'] > 0:
        if row['Level3Ports'] > 0:
            return "EV Charging Station (High Capacity)"
        elif row['Level2Ports'] > 0:
            return "Location with Level 2 Charging"
    return "Other"

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


def process_chunk(chunk_df):
    """Applies classification pipeline to a chunk of data."""
    chunk_df['PortClassification'] = chunk_df.apply(classify_by_ports, axis=1)
    chunk_df['KeywordClassification'] = chunk_df.apply(classify_by_keywords, axis=1)
    
    # Filter ambiguous cases for NLP classification (if needed)
    ambiguous_cases = chunk_df[chunk_df['PortClassification'] == "Other"]
    
    if not ambiguous_cases.empty:
        reference_categories = {
            'EV Charging Station': "Electric vehicle charging station",
            'Hotel/Lodging': "Hotel or lodging facility",
            'Shopping Center': "Shopping mall or plaza",
        }
        classified_ambiguous = classify_with_nlp(ambiguous_cases, reference_categories)
        chunk_df.loc[ambiguous_cases.index, 'NLPClassification'] = classified_ambiguous['NLPClassification']
    
    return chunk_df

def classify_locations_parallel(df, n_workers=4):
    """Classifies locations in parallel using multiple workers."""
    chunks = np.array_split(df, n_workers)  # Split dataframe into chunks
    
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        results = list(executor.map(process_chunk, chunks))
    
    return pd.concat(results)

# Example usage
df_full = pd.read_csv("locations.csv")  # Replace with your CSV file path
classified_df_full = classify_locations_parallel(df_full)

import matplotlib.pyplot as plt

# Use NLPClassification if available, otherwise fall back to PortClassification
classified_df_full['FinalClassification'] = classified_df_full['NLPClassification'].fillna(
    classified_df_full['PortClassification']
)

# Plot bar chart of classification counts
classification_counts = classified_df_full['FinalClassification'].value_counts()
classification_counts.plot(kind='bar')
plt.xlabel('Location Type')
plt.ylabel('Count')
plt.title('Distribution of Classified Location Types')
plt.tight_layout()
plt.show()

# Save the updated DataFrame to a new CSV file
classified_df_full.to_csv("classified_locations_with_types.csv", index=False)
