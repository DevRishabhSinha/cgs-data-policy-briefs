import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import spacy
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('locations.csv')

# Fill NaN values with empty strings
df['LocName'] = df['LocName'].fillna('')
df['address'] = df['address'].fillna('')

# Combine text columns
df['combined_text'] = df['LocName'] + ' ' + df['address']

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

# Named Entity Recognition (NER)
def extract_location_type(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ in ['FAC', 'ORG', 'GPE']]

df['extracted_types'] = df['combined_text'].apply(extract_location_type)

# TF-IDF Vectorization
tfidf = TfidfVectorizer(max_features=1000, stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_text'])

# K-means Clustering
num_clusters = 20
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(tfidf_matrix)

# Top terms per cluster
def get_top_terms(cluster_center, feature_names, n=10):
    terms = [(term, score) for term, score in zip(feature_names, cluster_center)]
    return sorted(terms, key=lambda x: x[1], reverse=True)[:n]

feature_names = tfidf.get_feature_names_out()

for i in range(num_clusters):
    print(f"Cluster {i}:")
    top_terms = get_top_terms(kmeans.cluster_centers_[i], feature_names)
    print(", ".join([term for term, _ in top_terms]))
    print()

# Visualization
plt.figure(figsize=(12, 6))
sns.countplot(x='cluster', data=df)
plt.title('Distribution of Location Clusters')
plt.xlabel('Cluster')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

# Rule-based Classification
def classify_location(row):
    text = row['combined_text'].lower()
    if 'gas' in text or 'fuel' in text:
        return 'Gas Station'
    elif 'charger' in text or 'charging' in text:
        return 'EV Charger'
    elif 'rest' in text and 'stop' in text:
        return 'Rest Stop'
    else:
        return 'Other'

df['location_type'] = df.apply(classify_location, axis=1)

# Final analysis
print(df['location_type'].value_counts())

# Save output
df.to_csv('classified_locations.csv', index=False)
