import pandas as pd
import numpy as np
import re

def combine_location_categories():
    """
    Combines three CSV files with different location categorizations,
    selecting the most specific category for each location.
    """
    print("Loading datasets...")
    # Load the datasets
    locations_final = pd.read_csv('categorized_locations_final.csv')
    locations1 = pd.read_csv('categorized_locations1.csv') 
    osm_sample = pd.read_csv('osm_categorized_sample.csv')
    
    print(f"Loaded datasets with rows: Final={len(locations_final)}, Loc1={len(locations1)}, OSM={len(osm_sample)}")
    
    # Create a unified dataset based on the final dataset
    combined_df = locations_final.copy()
    
    # Instead of using set_index which requires unique values, use merge
    # First, create a mapping dataframe with just the columns we need
    locations1_mapping = locations1[['LocID', 'LocationType']].copy()
    osm_mapping = osm_sample[['LocID', 'OSMPlaceType']].copy()
    
    # Merge the mapping dataframes with the combined_df
    combined_df = combined_df.merge(locations1_mapping, on='LocID', how='left')
    combined_df = combined_df.merge(osm_mapping, on='LocID', how='left')
    
    # Define categories by specificity level (high to low)
    category_specificity = {
        'highly_specific': [
            'tesla supercharger', 'mcdonalds', 'starbucks', 'walmart', 'target',
            'shell', 'marriott', 'hilton', 'best buy', 'whole foods', 'costco', 
            'bank of america', 'chase bank', 'cvs', 'walgreens', 'home depot', 'lowes',
            'chipotle', 'ikea', 'dicks sporting goods', 'panera', 'chick-fil-a'
        ],
        
        'specific': [
            'gas station', 'hotel', 'motel', 'restaurant', 'cafe', 'fast food',
            'grocery store', 'supermarket', 'convenience store', 'pharmacy',
            'bank', 'hospital', 'school', 'university', 'ev charger', 
            'charging station', 'car dealership', 'post office', 'police station',
            'fire station', 'library', 'gym', 'fitness center', 'movie theater',
            'stadium', 'church', 'synagogue', 'mosque', 'temple'
        ],
        
        'general': [
            'retail', 'store', 'mall', 'shopping center', 'office building',
            'apartments', 'lodging', 'dining', 'parking garage', 'rest stop',
            'service area', 'park', 'recreation', 'entertainment', 'medical',
            'financial', 'public building', 'government', 'transit'
        ],
        
        'vague': [
            'commercial', 'residential', 'industrial', 'parking', 'building',
            'mixed use', 'business', 'center', 'complex', 'facility'
        ]
    }
    
    # Flatten for easier lookup
    specificity_scores = {}
    for level, terms in category_specificity.items():
        score = {'highly_specific': 4, 'specific': 3, 'general': 2, 'vague': 1}[level]
        for term in terms:
            specificity_scores[term] = score
    
    def get_specificity_score(category):
        """Calculate how specific a category label is"""
        if pd.isna(category):
            return 0
            
        category = str(category).lower()
        
        # Check for exact terms first
        for term, score in specificity_scores.items():
            if term in category:
                return score
        
        # Count words as a fallback (more words usually = more specific)
        word_count = len(re.findall(r'\w+', category))
        return min(0.5 * word_count, 2.5)  # Max 2.5 for word count alone
    
    def is_ev_location(row):
        """Detect if a location is an EV charging station"""
        # Check port data
        ev_indicators = [
            pd.notna(row.get('Level1Ports', 0)) and row['Level1Ports'] > 0,
            pd.notna(row.get('Level2Ports', 0)) and row['Level2Ports'] > 0,
            pd.notna(row.get('Level3Ports', 0)) and row['Level3Ports'] > 0,
            pd.notna(row.get('PortsAvail', 0)) and row['PortsAvail'] > 0,
            pd.notna(row.get('has_ports', False)) and row['has_ports'],
            pd.notna(row.get('num_ports', 0)) and row['num_ports'] > 0
        ]
        
        # Check Tesla-specific indicators
        tesla_indicators = [
            pd.notna(row.get('NetTesla', 0)) and row['NetTesla'] > 0,
            pd.notna(row.get('is_tesla', False)) and row['is_tesla']
        ]
        
        # Check text fields for EV terms
        ev_terms = ['ev', 'electric vehicle', 'charger', 'charging']
        tesla_terms = ['tesla', 'supercharger']
        
        has_ev_terms = False
        has_tesla_terms = False
        
        for field in ['LocName', 'LocationTag', 'address', 'text_features', 'combined_text']:
            if field in row and pd.notna(row[field]):
                text = str(row[field]).lower()
                if any(term in text for term in ev_terms):
                    has_ev_terms = True
                if any(term in text for term in tesla_terms):
                    has_tesla_terms = True
        
        # Determine category
        if any(ev_indicators) or has_ev_terms:
            if any(tesla_indicators) or has_tesla_terms:
                return 'Tesla Supercharger'
            else:
                return 'EV Charging Station'
                
        return None
    
    def select_best_category(row):
        """Select the most specific category from available sources"""
        # First check if it's an EV charging location (highest priority)
        ev_category = is_ev_location(row)
        if ev_category:
            return ev_category
        
        # Collect all available categories
        categories = {}
        
        if 'Category' in row and pd.notna(row['Category']):
            categories['Category'] = row['Category']
        
        if 'LocationType' in row and pd.notna(row['LocationType']):
            categories['LocationType'] = row['LocationType']
            
        if 'OSMPlaceType' in row and pd.notna(row['OSMPlaceType']):
            categories['OSMPlaceType'] = row['OSMPlaceType']
            
        if not categories:
            return None
            
        # Calculate specificity scores for each category
        scores = {source: get_specificity_score(category) for source, category in categories.items()}
        
        # Add source weights (prioritize certain data sources)
        source_weights = {
            'OSMPlaceType': 0.5,  # OSM data is often more precise but limited sample
            'Category': 0.3,      # Final dataset has good coverage
            'LocationType': 0.2   # Base priority
        }
        
        # Apply weights
        for source in scores:
            scores[source] += source_weights.get(source, 0)
            
        # Get the source with highest score
        best_source = max(scores, key=scores.get)
        return categories[best_source]
    
    print("Selecting best categories...")
    # Apply selection logic to get the best category for each location
    combined_df['BestCategory'] = combined_df.apply(select_best_category, axis=1)
    
    # Format categories consistently
    def format_category(category):
        if pd.isna(category):
            return category
            
        # Apply consistent formatting
        formatted = str(category).strip()
        
        # Title case with special handling for acronyms
        words = []
        for word in formatted.split():
            if word.lower() in ['ev', 'cvs', 'atm', 'bp', 'kfc']:
                words.append(word.upper())
            else:
                words.append(word.capitalize())
                
        formatted = ' '.join(words)
        
        # Special case replacements
        replacements = {
            'Mcdonalds': 'McDonald\'s',
            'Walmart': 'Walmart',
            'Ikea': 'IKEA',
            'Osm': 'OSM'
        }
        
        for old, new in replacements.items():
            formatted = formatted.replace(old, new)
            
        return formatted
    
    combined_df['FinalCategory'] = combined_df['BestCategory'].apply(format_category)
    
    # Create the final dataset with all original columns plus the new category
    final_columns = [col for col in combined_df.columns 
                    if col not in ['BestCategory', 'LocationType', 'OSMPlaceType', 'Category']]
    
    if 'Category' in combined_df.columns:
        final_columns.insert(final_columns.index('FinalCategory'), 'Category')
        
    final_df = combined_df[final_columns]
    
    # Calculate statistics
    total = len(final_df)
    categorized = final_df['FinalCategory'].notna().sum()
    
    print(f"\nResults:")
    print(f"Total locations: {total}")
    print(f"Categorized locations: {categorized} ({categorized/total*100:.1f}%)")
    
    # Print top categories
    print("\nTop 10 most common categories:")
    top_cats = final_df['FinalCategory'].value_counts().head(10)
    for cat, count in top_cats.items():
        print(f"  {cat}: {count} ({count/total*100:.1f}%)")
    
    # Save the final dataset
    output_file = 'locations_with_precise_categories.csv'
    final_df.to_csv(output_file, index=False)
    print(f"\nSaved combined dataset to {output_file}")
    
    return final_df

if __name__ == "__main__":
    combine_location_categories()