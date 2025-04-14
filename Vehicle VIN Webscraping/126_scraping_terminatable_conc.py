import pandas as pd
import requests
import time
from datetime import datetime
import signal
import sys
import concurrent.futures
from tqdm import tqdm
import threading
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vin_processing.log'),
        logging.StreamHandler()
    ]
)

# NHTSA API endpoint - using DecodeVinExtended for more detailed data
NHTSA_API_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinExtended/"

# Configuration
MAX_WORKERS = 20
BATCH_SIZE = 200
SAVE_INTERVAL = 50
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 0.05

# Headers for API request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
}

# Complete variable mapping
VARIABLE_ID_MAP = {
    26: 'Make',
    27: 'Manufacturer Name',
    28: 'Model',
    29: 'Model Year',
    31: 'Plant City',
    34: 'Series',
    38: 'Trim',
    39: 'Vehicle Type',
    75: 'Plant Country',
    76: 'Plant Company Name',
    77: 'Plant State',
    109: 'Trim2',
    110: 'Series2',
    114: 'Note',
    136: 'Base Price ($)',
    195: 'Non-Land Use',
    5: 'Body Class',
    14: 'Doors',
    40: 'Windows',
    60: 'Wheel Base Type',
    159: 'Track Width (inches)',
    25: 'Gross Vehicle Weight Rating From',
    49: 'Bed Length (inches)',
    54: 'Curb Weight (pounds)',
    111: 'Wheel Base (inches) From',
    112: 'Wheel Base (inches) To',
    184: 'Gross Combination Weight Rating From',
    185: 'Gross Combination Weight Rating To',
    190: 'Gross Vehicle Weight Rating To',
    3: 'Bed Type',
    4: 'Cab Type',
    116: 'Trailer Type Connection',
    117: 'Trailer Body Type',
    118: 'Trailer Length (feet)',
    155: 'Other Trailer Info',
    115: 'Number of Wheels',
    119: 'Wheel Size Front (inches)',
    120: 'Wheel Size Rear (inches)',
    23: 'Entertainment System',
    36: 'Steering Location',
    33: 'Number of Seats',
    61: 'Number of Seat Rows',
    37: 'Transmission Style',
    63: 'Transmission Speeds',
    15: 'Drive Type',
    41: 'Axles',
    145: 'Axle Configuration',
    42: 'Brake System Type',
    52: 'Brake System Description',
    1: 'Other Battery Info',
    2: 'Battery Type',
    48: 'Number of Battery Cells per Module',
    57: 'Battery Current (Amps) From',
    58: 'Battery Voltage (Volts) From',
    59: 'Battery Energy (kWh) From',
    72: 'EV Drive Unit',
    132: 'Battery Current (Amps) To',
    133: 'Battery Voltage (Volts) To',
    134: 'Battery Energy (kWh) To',
    137: 'Number of Battery Modules per Pack',
    138: 'Number of Battery Packs per Vehicle',
    127: 'Charger Level',
    128: 'Charger Power (kW)',
    9: 'Engine Number of Cylinders',
    11: 'Displacement (CC)',
    12: 'Displacement (CI)',
    13: 'Displacement (L)',
    17: 'Engine Stroke Cycles',
    18: 'Engine Model',
    21: 'Engine Power (kW)',
    24: 'Fuel Type - Primary',
    62: 'Valve Train Design',
    64: 'Engine Configuration',
    66: 'Fuel Type - Secondary',
    67: 'Fuel Delivery / Fuel Injection Type',
    71: 'Engine Brake (hp) From',
    122: 'Cooling Type',
    125: 'Engine Brake (hp) To',
    126: 'Electrification Level',
    129: 'Other Engine Info',
    135: 'Turbo',
    139: 'Top Speed (MPH)',
    146: 'Engine Manufacturer',
    78: 'Pretensioner',
    79: 'Seat Belt Type',
    121: 'Other Restraint System Info',
    55: 'Curtain Air Bag Locations',
    56: 'Seat Cushion Air Bag Locations',
    65: 'Front Air Bag Locations',
    69: 'Knee Air Bag Locations',
    107: 'Side Air Bag Locations',
    86: 'Anti-lock Braking System (ABS)',
    99: 'Electronic Stability Control (ESC)',
    100: 'Traction Control',
    168: 'Tire Pressure Monitoring System (TPMS) Type',
    169: 'Active Safety System Note',
    172: 'Auto-Reverse System for Windows and Sunroofs',
    173: 'Automatic Pedestrian Alerting Sound (for Hybrid and EV only)',
    175: 'Event Data Recorder (EDR)',
    176: 'Keyless Ignition',
    181: 'SAE Automation Level From',
    182: 'SAE Automation Level To',
    96: 'NCSA Body Type',
    97: 'NCSA Make',
    98: 'NCSA Model',
    186: 'NCSA Note',
    81: 'Adaptive Cruise Control (ACC)',
    87: 'Crash Imminent Braking (CIB)',
    88: 'Blind Spot Warning (BSW)',
    101: 'Forward Collision Warning (FCW)',
    102: 'Lane Departure Warning (LDW)',
    103: 'Lane Keeping Assistance (LKA)',
    104: 'Backup Camera',
    105: 'Parking Assist',
    147: 'Bus Length (feet)',
    148: 'Bus Floor Configuration Type',
    149: 'Bus Type',
    150: 'Other Bus Info',
    151: 'Custom Motorcycle Type',
    152: 'Motorcycle Suspension Type',
    153: 'Motorcycle Chassis Type',
    154: 'Other Motorcycle Info',
    170: 'Dynamic Brake Support (DBS)',
    171: 'Pedestrian Automatic Emergency Braking (PAEB)',
    174: 'Automatic Crash Notification (ACN) / Advanced Automatic Crash Notification (AACN)',
    177: 'Daytime Running Light (DRL)',
    178: 'Headlamp Light Source',
    179: 'Semiautomatic Headlamp Beam Switching',
    180: 'Adaptive Driving Beam (ADB)',
    183: 'Rear Cross Traffic Alert',
    192: 'Rear Automatic Emergency Braking',
    193: 'Blind Spot Intervention (BSI)',
    194: 'Lane Centering Assistance'
}

# Thread-safe progress tracking
processed_lock = threading.Lock()
processed_data = []
processed_vins = set()
error_vins = set()

def signal_handler(sig, frame):
    logging.info('\nProgram terminated by user. Saving progress...')
    save_final_results()
    sys.exit(0)

def fetch_vehicle_data(vin_info):
    """
    Fetch extended vehicle data from NHTSA API for a given VIN with retries
    """
    vin, reg_date = vin_info
    
    for attempt in range(MAX_RETRIES):
        try:
            time.sleep(RATE_LIMIT_DELAY)
            
            response = requests.get(
                f"{NHTSA_API_URL}{vin}?format=json",
                headers=HEADERS
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'Results' in data and data['Results']:
                    processed_data = {'VIN': vin, 'Registration_Date': reg_date}
                    for item in data['Results']:
                        var_id = item['VariableId']
                        if var_id in VARIABLE_ID_MAP:
                            processed_data[VARIABLE_ID_MAP[var_id]] = item['Value']
                    return processed_data
                    
            elif response.status_code == 429:  # Rate limit hit
                wait_time = 2 ** attempt
                logging.warning(f"Rate limit hit for VIN {vin}. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            else:
                logging.warning(f"Failed to fetch VIN {vin}: Status {response.status_code}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)
                    continue
                    
        except Exception as e:
            logging.error(f"Error fetching data for VIN {vin}: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)
                continue
    
    error_vins.add(vin)
    return None

def save_progress(filename, current_data, final=False):
    """
    Save current progress to CSV file with error tracking
    """
    try:
        # Ensure output directory exists
        Path(filename).parent.mkdir(exist_ok=True)
        
        # Save main data
        df = pd.DataFrame(current_data)
        df.to_csv(filename, index=False)
        logging.info(f"Saved {len(current_data)} records to {filename}")
        
        # Save error VINs if any exist
        if error_vins:
            error_file = str(filename).replace('.csv', '_errors.csv')
            pd.DataFrame(list(error_vins), columns=['VIN']).to_csv(error_file, index=False)
            logging.info(f"Saved {len(error_vins)} error VINs to {error_file}")
        
    except Exception as e:
        logging.error(f"Error saving progress: {str(e)}")

def save_final_results():
    """
    Save final results and cleanup
    """
    with processed_lock:
        save_progress(output_filename, processed_data, final=True)

def process_batch(batch_data, output_filename):
    """
    Process a batch of VINs in parallel
    """
    batch_results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Create list of (vin, reg_date) tuples for processing
        vin_info_list = [(row['VIN'], row['Registration Date']) for _, row in batch_data.iterrows()]
        
        # Create futures for each VIN
        future_to_vin = {executor.submit(fetch_vehicle_data, vin_info): vin_info 
                        for vin_info in vin_info_list}
        
        # Process completed futures with progress bar
        for future in tqdm(
            concurrent.futures.as_completed(future_to_vin),
            total=len(future_to_vin),
            desc="Processing batch"
        ):
            vin_info = future_to_vin[future]
            try:
                result = future.result()
                if result:
                    with processed_lock:
                        if result['VIN'] not in processed_vins:
                            processed_data.append(result)
                            processed_vins.add(result['VIN'])
                            batch_results.append(result)
                            
                            # Save progress at intervals
                            if len(processed_data) % SAVE_INTERVAL == 0:
                                save_progress(output_filename, processed_data)
                                
            except Exception as e:
                logging.error(f"Error processing VIN {vin_info[0]}: {str(e)}")
                error_vins.add(vin_info[0])
    
    return batch_results

def process_dr2114_data():
    """
    Main function to process all VINs from the input file
    """
    # Set up signal handler for graceful termination
    signal.signal(signal.SIGINT, signal_handler)
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    global output_filename
    output_filename = output_dir / f'DR2114_Extended_{timestamp}.csv'
    
    # Read the input CSV file
    logging.info("Reading input file...")
    df = pd.read_csv('DR2114_Data.csv')
    total_vins = len(df)
    logging.info(f"Found {total_vins} VINs to process")
    
    # Check for existing progress
    try:
        existing_df = pd.read_csv(output_filename)
        global processed_vins, processed_data
        processed_vins = set(existing_df['VIN'])
        processed_data = existing_df.to_dict('records')
        logging.info(f"Found {len(processed_vins)} already processed VINs")
    except FileNotFoundError:
        # Create empty output file
        save_progress(output_filename, [])
        logging.info(f"Created new output file: {output_filename}")
    
    # Filter out already processed VINs
    df = df[~df['VIN'].isin(processed_vins)]
    remaining_vins = len(df)
    logging.info(f"Processing {remaining_vins} remaining VINs")
    
    try:
        # Process in batches
        for i in range(0, len(df), BATCH_SIZE):
            batch_df = df.iloc[i:i+BATCH_SIZE]
            logging.info(f"\nProcessing batch {(i//BATCH_SIZE)+1}/{(len(df)-1)//BATCH_SIZE+1}")
            
            batch_results = process_batch(batch_df, output_filename)
            
            # Save progress after each batch
            if batch_results:
                with processed_lock:
                    save_progress(output_filename, processed_data)
            
            # Log batch completion
            completed = min(i + BATCH_SIZE, len(df))
            logging.info(f"Completed {completed}/{len(df)} VINs")
        
        # Final save
        save_progress(output_filename, processed_data, final=True)
        
    except Exception as e:
        logging.error(f"Error in main processing loop: {str(e)}")
        save_progress(output_filename)