import pandas as pd
import requests
import time
from datetime import datetime
import signal
import sys

# NHTSA API endpoint - using DecodeVinExtended for more detailed data
NHTSA_API_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinExtended/"

# Variable mapping from the original script
VARIABLE_ID_MAP = {
    26: 'Make', 27: 'Manufacturer Name', 28: 'Model', 29: 'Model Year',
    31: 'Plant City', 34: 'Series', 38: 'Trim', 39: 'Vehicle Type',
    75: 'Plant Country', 76: 'Plant Company Name', 77: 'Plant State',
    109: 'Trim2', 110: 'Series2', 114: 'Note', 136: 'Base Price ($)',
    195: 'Non-Land Use', 5: 'Body Class', 14: 'Doors', 40: 'Windows',
    60: 'Wheel Base Type', 159: 'Track Width (inches)',
    25: 'Gross Vehicle Weight Rating From', 49: 'Bed Length (inches)',
    54: 'Curb Weight (pounds)', 111: 'Wheel Base (inches) From',
    112: 'Wheel Base (inches) To', 184: 'Gross Combination Weight Rating From',
    185: 'Gross Combination Weight Rating To', 190: 'Gross Vehicle Weight Rating To',
    3: 'Bed Type', 4: 'Cab Type', 116: 'Trailer Type Connection',
    117: 'Trailer Body Type', 118: 'Trailer Length (feet)',
    155: 'Other Trailer Info', 115: 'Number of Wheels',
    119: 'Wheel Size Front (inches)', 120: 'Wheel Size Rear (inches)',
    23: 'Entertainment System', 36: 'Steering Location', 33: 'Number of Seats',
    61: 'Number of Seat Rows', 37: 'Transmission Style', 63: 'Transmission Speeds',
    15: 'Drive Type', 41: 'Axles', 145: 'Axle Configuration',
    42: 'Brake System Type', 52: 'Brake System Description',
    1: 'Other Battery Info', 2: 'Battery Type', 48: 'Number of Battery Cells per Module',
    57: 'Battery Current (Amps) From', 58: 'Battery Voltage (Volts) From',
    59: 'Battery Energy (kWh) From', 72: 'EV Drive Unit',
    132: 'Battery Current (Amps) To', 133: 'Battery Voltage (Volts) To',
    134: 'Battery Energy (kWh) To', 137: 'Number of Battery Modules per Pack',
    138: 'Number of Battery Packs per Vehicle', 127: 'Charger Level',
    128: 'Charger Power (kW)', 9: 'Engine Number of Cylinders',
    11: 'Displacement (CC)', 12: 'Displacement (CI)', 13: 'Displacement (L)',
    17: 'Engine Stroke Cycles', 18: 'Engine Model', 21: 'Engine Power (kW)',
    24: 'Fuel Type - Primary', 62: 'Valve Train Design', 64: 'Engine Configuration',
    66: 'Fuel Type - Secondary', 67: 'Fuel Delivery / Fuel Injection Type',
    71: 'Engine Brake (hp) From', 122: 'Cooling Type', 125: 'Engine Brake (hp) To',
    126: 'Electrification Level', 129: 'Other Engine Info', 135: 'Turbo',
    139: 'Top Speed (MPH)', 146: 'Engine Manufacturer', 78: 'Pretensioner',
    79: 'Seat Belt Type', 121: 'Other Restraint System Info',
    55: 'Curtain Air Bag Locations', 56: 'Seat Cushion Air Bag Locations',
    65: 'Front Air Bag Locations', 69: 'Knee Air Bag Locations',
    107: 'Side Air Bag Locations', 86: 'Anti-lock Braking System (ABS)',
    99: 'Electronic Stability Control (ESC)', 100: 'Traction Control',
    168: 'Tire Pressure Monitoring System (TPMS) Type', 169: 'Active Safety System Note',
    172: 'Auto-Reverse System for Windows and Sunroofs',
    173: 'Automatic Pedestrian Alerting Sound (for Hybrid and EV only)',
    175: 'Event Data Recorder (EDR)', 176: 'Keyless Ignition',
    181: 'SAE Automation Level From', 182: 'SAE Automation Level To',
    96: 'NCSA Body Type', 97: 'NCSA Make', 98: 'NCSA Model', 186: 'NCSA Note',
    81: 'Adaptive Cruise Control (ACC)', 87: 'Crash Imminent Braking (CIB)',
    88: 'Blind Spot Warning (BSW)', 101: 'Forward Collision Warning (FCW)',
    102: 'Lane Departure Warning (LDW)', 103: 'Lane Keeping Assistance (LKA)',
    104: 'Backup Camera', 105: 'Parking Assist', 147: 'Bus Length (feet)',
    148: 'Bus Floor Configuration Type', 149: 'Bus Type', 150: 'Other Bus Info',
    151: 'Custom Motorcycle Type', 152: 'Motorcycle Suspension Type',
    153: 'Motorcycle Chassis Type', 154: 'Other Motorcycle Info',
    170: 'Dynamic Brake Support (DBS)',
    171: 'Pedestrian Automatic Emergency Braking (PAEB)',
    174: 'Automatic Crash Notification (ACN) / Advanced Automatic Crash Notification (AACN)',
    177: 'Daytime Running Light (DRL)', 178: 'Headlamp Light Source',
    179: 'Semiautomatic Headlamp Beam Switching', 180: 'Adaptive Driving Beam (ADB)',
    183: 'Rear Cross Traffic Alert', 192: 'Rear Automatic Emergency Braking',
    193: 'Blind Spot Intervention (BSI)', 194: 'Lane Centering Assistance'
}

def signal_handler(sig, frame):
    print('\nProgram terminated by user. Progress has been saved.')
    sys.exit(0)

def fetch_vehicle_data(vin):
    """
    Fetch extended vehicle data from NHTSA API for a given VIN
    """
    try:
        response = requests.get(f"{NHTSA_API_URL}{vin}?format=json")
        if response.status_code == 200:
            data = response.json()
            if 'Results' in data and data['Results']:
                # Process the extended data format
                processed_data = {'VIN': vin}
                for item in data['Results']:
                    var_id = item['VariableId']
                    if var_id in VARIABLE_ID_MAP:
                        processed_data[VARIABLE_ID_MAP[var_id]] = item['Value']
                return processed_data
        return None
    except Exception as e:
        print(f"Error fetching data for VIN {vin}: {str(e)}")
        return None

def process_dr2114_data():
    # Set up signal handler for graceful termination
    signal.signal(signal.SIGINT, signal_handler)
    
    # Generate output filename with timestamp
    output_filename = f'missing_stragglers{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    # Read the input CSV file
    df = pd.read_csv('missing_vins.csv')
    
    # Check for existing progress
    try:
        existing_df = pd.read_csv(output_filename)
        processed_vins = set(existing_df['VIN'])
        processed_data = existing_df.to_dict('records')
        print(f"Found {len(processed_vins)} already processed VINs")
    except FileNotFoundError:
        processed_vins = set()
        processed_data = []
    
    # Process each VIN
    total_vins = len(df)
    for index, row in df.iterrows():
        vin = row['VIN']
        
        # Skip if VIN was already processed
        if vin in processed_vins:
            continue
        
        # Get registration date from original data
        reg_date = row['Registration Date']
        
        # Fetch extended vehicle data from NHTSA
        vehicle_data = fetch_vehicle_data(vin)
        
        if vehicle_data:
            # Add registration date to the vehicle data
            vehicle_data['Registration_Date'] = reg_date
            processed_data.append(vehicle_data)
            processed_vins.add(vin)
            
            # Save progress every 10 records
            if len(processed_data) % 10 == 0:
                pd.DataFrame(processed_data).to_csv(output_filename, index=False)
                print(f"Progress saved. {len(processed_data)} records written to {output_filename}")
            
            # Add a small delay to avoid overwhelming the API
        
        # Print progress
        print(f"Processed VIN {vin} ({index + 1}/{total_vins})")
    
    # Final save of any remaining records
    pd.DataFrame(processed_data).to_csv(output_filename, index=False)
    print(f"\nProcessing complete. Results saved to {output_filename}")

if __name__ == "__main__":
    process_dr2114_data()