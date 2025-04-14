"""
Location Type Classifier
------------------------
A Python solution to classify location types from CSV data. This script:
1. Reads a CSV file containing location data
2. Classifies each location based on name and address using a rule-based approach
3. Visualizes the distribution of location types
4. Exports the classified data to a new CSV file

Usage: python location_classifier.py path/to/locations.csv
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import argparse
from pathlib import Path
import time

def classify_location(row):
    """
    Classify a location based on its name, address, and other features.
    
    Args:
        row: A pandas Series containing location data
        
    Returns:
        str: The classified location type
    """
    # Prepare text for pattern matching
    name = str(row.get('LocName', '')).lower().replace('"', '')
    address = str(row.get('address', '')).lower()
    combined_text = f"{name} {address}"
    
    # Get port information
    level2_ports = row.get('Level2Ports', 0) or 0
    level3_ports = row.get('Level3Ports', 0) or 0
    
    # Check if this is an EV charging location
    is_ev_location = level2_ports > 0 or level3_ports > 0
    
    # Define patterns for location types
    patterns = {
        'hotel': r'hotel|resort|inn|suites|ritz|intercontinental|hilton|marriott|hyatt',
        'parking': r'park(ing|\s)garage|garage|parking',
        'supermarket': r'supermarket|grocery|publix|walmart|costco|target|kroger|safeway|market|store',
        'shopping': r'mall|plaza|shopping|center',
        'educational': r'university|college|campus|school|education',
        'medical': r'hospital|medical|healthcare|clinic|doctor|physician',
        'government': r'municipal|city hall|town hall|government|city of|town of|county|department',
        'residential': r'apartment|residential|condo|villa|house|home|living',
        'office': r'office|corporate|business|tower|center|financial',
        'library': r'library',
        'restaurant': r'restaurant|cafe|dining|food|bar|grill',
        'gas_station': r'gas station|shell|bp|exxon|chevron|7-eleven|petrol',
        'park': r'park|recreation|garden|playground',  # Exclude 'parking'
        'beach': r'beach|marina|ocean|sea|bay|harbor|coast'
    }
    
    # Check for patterns in combined text
    if is_ev_location:
        # For EV charging locations
        for location_type, pattern in patterns.items():
            if re.search(pattern, combined_text):
                # Special case for parks (avoid matching "parking")
                if location_type == 'park' and re.search(r'parking', combined_text):
                    continue
                return f"{location_type.replace('_', ' ').title()} Charging"
        
        # Default for EV locations
        return "EV Charging Station"
    else:
        # For non-EV locations
        for location_type, pattern in patterns.items():
            if re.search(pattern, combined_text):
                # Special case for parks
                if location_type == 'park' and re.search(r'parking', combined_text):
                    continue
                return location_type.replace('_', ' ').title()
        
        # Default for non-EV locations
        return "Unknown"

def process_csv(file_path, output_path=None, sample_size=None, visualize=True):
    """
    Process a CSV file, classify locations, and optionally visualize and export results.
    
    Args:
        file_path: Path to the input CSV file
        output_path: Path for the output CSV file (optional)
        sample_size: Number of rows to process (optional, for testing)
        visualize: Whether to generate visualizations
        
    Returns:
        pandas.DataFrame: The processed data with classifications
    """
    print(f"Reading CSV file: {file_path}")
    start_time = time.time()
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    if sample_size:
        df = df.head(sample_size)
    
    print(f"Read {len(df)} rows in {time.time() - start_time:.2f} seconds")
    print(f"Columns: {', '.join(df.columns)}")
    
    # Apply the classifier to each row
    print("Classifying locations...")
    classification_start = time.time()
    df['LocationType'] = df.apply(classify_location, axis=1)
    print(f"Classification completed in {time.time() - classification_start:.2f} seconds")
    
    # Calculate summary statistics
    type_counts = df['LocationType'].value_counts()
    percentage_classified = (len(df) - type_counts.get('Unknown', 0)) / len(df) * 100
    
    print(f"\nPercentage of locations classified: {percentage_classified:.2f}%")
    print("\nTop 10 location types:")
    for loc_type, count in type_counts.head(10).items():
        print(f"  {loc_type}: {count} ({count/len(df)*100:.2f}%)")
    
    # EV vs non-EV statistics
    ev_count = df[(df['Level2Ports'] > 0) | (df['Level3Ports'] > 0)].shape[0]
    non_ev_count = len(df) - ev_count
    print(f"\nEV Charging Locations: {ev_count} ({ev_count/len(df)*100:.2f}%)")
    print(f"Non-EV Locations: {non_ev_count} ({non_ev_count/len(df)*100:.2f}%)")
    
    # Generate visualizations
    if visualize:
        generate_visualizations(df, type_counts)
    
    # Export to CSV
    if output_path:
        print(f"\nExporting classified data to: {output_path}")
        df.to_csv(output_path, index=False)
        print("Export completed")
    
    print(f"\nTotal processing time: {time.time() - start_time:.2f} seconds")
    return df

def generate_visualizations(df, type_counts):
    """
    Generate visualizations of the location type distribution.
    
    Args:
        df: The processed DataFrame
        type_counts: Series of location type counts
    """
    print("\nGenerating visualizations...")
    
    # Set the style
    plt.style.use('ggplot')
    
    # 1. Pie chart of location types
    plt.figure(figsize=(12, 8))
    
    # Group smaller categories
    min_percent_threshold = 1.0
    main_categories = type_counts[type_counts/len(df)*100 >= min_percent_threshold]
    other_count = type_counts[type_counts/len(df)*100 < min_percent_threshold].sum()
    
    if other_count > 0:
        pie_data = pd.concat([main_categories, pd.Series({'Other': other_count})])
    else:
        pie_data = main_categories
    
    # Create the pie chart
    plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', 
            shadow=True, startangle=90, textprops={'fontsize': 9})
    plt.axis('equal')
    plt.title('Distribution of Location Types', fontsize=14)
    plt.tight_layout()
    plt.savefig('location_types_pie.png', dpi=300, bbox_inches='tight')
    
    # 2. Bar chart of top 15 location types
    plt.figure(figsize=(14, 8))
    top_types = type_counts.head(15)
    
    sns.barplot(x=top_types.index, y=top_types.values)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Location Type')
    plt.ylabel('Count')
    plt.title('Top 15 Location Types by Frequency', fontsize=14)
    plt.tight_layout()
    plt.savefig('location_types_bar.png', dpi=300, bbox_inches='tight')
    
    # 3. Heatmap of level 2 vs level 3 ports by location type
    plt.figure(figsize=(14, 10))
    
    # Calculate average ports by location type
    port_data = df.groupby('LocationType').agg({
        'Level2Ports': 'mean',
        'Level3Ports': 'mean'
    }).fillna(0)
    
    # Sort by total ports
    port_data['TotalPorts'] = port_data['Level2Ports'] + port_data['Level3Ports']
    port_data = port_data.sort_values('TotalPorts', ascending=False).head(15)
    port_data = port_data.drop('TotalPorts', axis=1)
    
    # Create heatmap
    sns.heatmap(port_data, annot=True, cmap='YlGnBu', fmt='.2f')
    plt.title('Average Number of Charging Ports by Location Type', fontsize=14)
    plt.tight_layout()
    plt.savefig('charging_ports_heatmap.png', dpi=300, bbox_inches='tight')
    
    print("Visualizations saved to current directory")

def main():
    """Main function to parse arguments and process the CSV file."""
    parser = argparse.ArgumentParser(description='Classify locations from a CSV file')
    parser.add_argument('input_file', help='Path to the input CSV file')
    parser.add_argument('--output', '-o', help='Path to the output CSV file')
    parser.add_argument('--sample', '-s', type=int, help='Process only a sample of rows')
    parser.add_argument('--no-viz', '-n', action='store_true', help='Skip visualizations')
    
    args = parser.parse_args()
    
    # If no output path specified, create one based on input file
    if not args.output:
        input_path = Path(args.input_file)
        args.output = input_path.with_name(f"{input_path.stem}_classified.csv")
    
    # Process the CSV file
    process_csv(
        args.input_file, 
        args.output, 
        sample_size=args.sample, 
        visualize=not args.no_viz
    )

if __name__ == "__main__":
    main()