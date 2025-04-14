import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from tqdm import tqdm

# Load data
print("Loading data...")
df = pd.read_csv('locations.csv')
print(f"Loaded {len(df)} locations")

# Clean and prepare data
df['LocName'] = df['LocName'].str.replace('"', '').fillna('')
df['address'] = df['address'].fillna('')
df['text_features'] = df['LocName'] + ' ' + df['address']

# Create port-related features
df['has_ports'] = (df['Level3Ports'] + df['Level2Ports'] + df['Level1Ports']) > 0
df['num_ports'] = df['Level3Ports'] + df['Level2Ports'] + df['Level1Ports'] 
df['is_tesla'] = df['NetTesla'] > 0

# Define comprehensive category patterns
category_patterns = {
    'EV Supercharger': [r'supercharger', r'fl supercharger', r'tx supercharger'],
    'Tesla Destination Charger': [r'tesla destination'],
    'Gas Station': [r'gas', r'fuel', r'wawa', r'sunoco', r'shell', r'exxon', r'7-eleven'],
    'Hotel/Resort': [r'hotel', r'resort', r'inn', r'suites', r'marriott', r'hilton', r'ritz', r'courtyard'],
    'Shopping/Retail': [r'mall', r'shopping', r'plaza', r'target', r'walmart', r'shops', r'store'],
    'Residential': [r'apartment', r'condominium', r'residence', r'tower', r'villa', r'home'],
    'Office/Corporate': [r'office', r'corporate', r'headquarters', r'building', r'center'],
    'Parking': [r'garage', r'parking'],
    'Restaurant/Food': [r'restaurant', r'café', r'cafe', r'dining', r'bar', r'grill', r'food'],
    'Car Dealership': [r'dealership', r'motors', r'ford', r'toyota', r'honda', r'bmw', r'audi', r'volkswagen'],
    'Recreation': [r'park', r'garden', r'recreation', r'tennis', r'beach', r'club'],
    'Medical/Healthcare': [r'hospital', r'medical', r'health', r'clinic', r'care'],
    'Municipal/Government': [r'city', r'town', r'municipal', r'government', r'department'],
    'Education': [r'school', r'university', r'college', r'campus', r'education']
}

# Step 1: Rule-based classification with detailed logic
print("Applying rule-based classification...")
def classify_location(row):
    text = row['text_features'].lower()
    
    # Special case for superchargers
    if 'supercharger' in text:
        return 'EV Supercharger'
    
    # Special case for Tesla Destination Chargers
    if 'tesla destination' in text:
        return 'Tesla Destination Charger'
    
    # Handle EV charging stations based on port data
    if row['has_ports']:
        if row['is_tesla']:
            return 'Tesla Charging Station'
        else:
            return 'EV Charging Station'
    
    # Process all other categories
    for category, patterns in category_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return category
    
    return None  # Unknown category

# Apply classification
df['Category'] = df.apply(classify_location, axis=1)

# Step 2: Handle unclassified locations with clustering
unclassified = df[df['Category'].isnull()]
print(f"Classified {len(df) - len(unclassified)} locations by rules")
print(f"Clustering {len(unclassified)} unclassified locations...")

if len(unclassified) > 0:
    # Feature extraction
    vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
    X = vectorizer.fit_transform(unclassified['text_features'])
    
    # Determine optimal number of clusters
    n_clusters = min(20, max(5, len(unclassified) // 100))
    
    # Cluster the unclassified locations
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    unclassified['Cluster'] = kmeans.fit_predict(X)
    
    # Generate meaningful cluster labels
    feature_names = vectorizer.get_feature_names_out()
    cluster_labels = {}
    
    for cluster_id in range(n_clusters):
        # Get top terms for this cluster from the centroid
        centroid = kmeans.cluster_centers_[cluster_id]
        top_indices = centroid.argsort()[-5:][::-1]
        top_terms = [feature_names[i] for i in top_indices]
        
        # Create a descriptive label
        cluster_labels[cluster_id] = f"Unknown Type: {', '.join(top_terms)}"
    
    # Apply cluster labels
    unclassified['Category'] = unclassified['Cluster'].map(cluster_labels)
    
    # Update the main dataframe
    for idx in unclassified.index:
        df.at[idx, 'Category'] = unclassified.at[idx, 'Category']

# Step 3: Visualization and analysis
print("Generating visualizations...")

# Category distribution
plt.figure(figsize=(16, 10))
category_counts = df['Category'].value_counts().head(20)
sns.barplot(x=category_counts.index, y=category_counts.values)
plt.xticks(rotation=45, ha='right')
plt.title('Top 20 Location Types')
plt.tight_layout()
plt.savefig('location_types.png')

# EV charging station analysis
ev_df = df[df['Category'].isin(['EV Supercharger', 'Tesla Destination Charger', 
                              'Tesla Charging Station', 'EV Charging Station'])]

plt.figure(figsize=(14, 8))
sns.countplot(data=ev_df, x='Category')
plt.title('Distribution of EV Charging Station Types')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('ev_station_types.png')

# Geographic distribution (if folium is available)
try:
    import folium
    from folium.plugins import MarkerCluster
    
    # Sample data for map (500 points max for performance)
    map_sample = df.sample(min(500, len(df)))
    
    # Create map centered on data
    m = folium.Map(location=[map_sample['Lat'].mean(), map_sample['Long'].mean()], 
                  zoom_start=6)
    
    # Add clustered markers
    marker_cluster = MarkerCluster().add_to(m)
    
    # Create color mapping
    category_colors = {}
    categories = df['Category'].unique()
    colormap = plt.cm.get_cmap('tab20', len(categories))
    
    for i, category in enumerate(categories):
        category_colors[category] = f'#{int(colormap(i)[0]*255):02x}{int(colormap(i)[1]*255):02x}{int(colormap(i)[2]*255):02x}'
    
    # Add markers
    for idx, row in map_sample.iterrows():
        popup_text = f"""
        <b>{row['LocName']}</b><br>
        Type: {row['Category']}<br>
        Address: {row['address']}
        """
        folium.Marker(
            location=[row['Lat'], row['Long']],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=row['LocName'],
            icon=folium.Icon(color='blue')
        ).add_to(marker_cluster)
    
    m.save('location_map.html')
    print("Created interactive map: location_map.html")
except ImportError:
    print("Folium not available, skipping map creation")

# Save the final categorized data
df.to_csv('categorized_locations_final.csv', index=False)

print("Process complete! Categorized data saved to 'categorized_locations_final.csv'")
