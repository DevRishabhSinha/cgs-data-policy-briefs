import pandas as pd
import requests
import time
from datetime import datetime

# NHTSA API endpoint
NHTSA_API_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/"

def fetch_vehicle_data(vin):
    """
    Fetch vehicle data from NHTSA API for a given VIN
    """
    try:
        response = requests.get(f"{NHTSA_API_URL}{vin}?format=json")
        if response.status_code == 200:
            return response.json()['Results'][0]
        return None
    except Exception as e:
        print(f"Error fetching data for VIN {vin}: {str(e)}")
        return None

def process_dr2114_data():
    # Read the CSV file
    df = pd.read_csv('DR2114_Data.csv')
    
    # Initialize lists to store the processed data
    processed_data = []
    
    # Process each VIN
    for index, row in df.iterrows():
        vin = row['VIN']
        reg_date = row['Registration Date']
        
        # Fetch vehicle data from NHTSA
        vehicle_data = fetch_vehicle_data(vin)
        
        if vehicle_data:
            # Extract relevant information
            processed_row = {
                'VIN': vin,
                'Registration_Date': reg_date,
                'Make': vehicle_data.get('Make', ''),
                'Model': vehicle_data.get('Model', ''),
                'ModelYear': vehicle_data.get('ModelYear', ''),
                'FuelTypePrimary': vehicle_data.get('FuelTypePrimary', ''),
                'ElectrificationLevel': vehicle_data.get('ElectrificationLevel', ''),
                'BodyClass': vehicle_data.get('BodyClass', ''),
                'Manufacturer': vehicle_data.get('Manufacturer', '')
            }
            processed_data.append(processed_row)
            
            # Add a small delay to avoid overwhelming the API
            time.sleep(0.5)
            
            # Print progress
            print(f"Processed VIN {vin} ({index + 1}/{len(df)})")
    
    # Create a new DataFrame with the processed data
    result_df = pd.DataFrame(processed_data)
    
    # Save to CSV
    output_filename = f'DR2114_Processed_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    result_df.to_csv(output_filename, index=False)
    print(f"\nProcessing complete. Results saved to {output_filename}")

if __name__ == "__main__":
    process_dr2114_data()