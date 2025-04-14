import pandas as pd
import requests

variable_id_map = {
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

def fetch_and_extract_data(vin_number, model_year=None):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinExtended/{vin_number}?format=json"
    if model_year:
        url += f"&modelyear={model_year}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Process the JSON data here to match your desired output format
        # For simplicity, we'll just return the entire response.
        return data
    else:
        return {"error": f"Failed to fetch data for VIN: {vin_number}"}


# Load and shuffle the data
filtered_df = pd.read_csv('filtered_df.csv').sample(frac=1, random_state=42).reset_index(drop=True)
filtered_df = filtered_df[0:1000]

# Collect data
all_data = [fetch_and_extract_data(row['VIN']) for _, row in filtered_df.iterrows()]
# Initialize an empty list to collect base prices


all_records = []
vins = []

# Loop through all_data to extract the value corresponding to VariableIDs
for i, record in enumerate(all_data):
    row_data = {}  # Initialize an empty dictionary for each VIN
    row_data['VIN'] = filtered_df.iloc[i]['VIN']  # Add the VIN to the dictionary
    vins.append(row_data['VIN'])  # Also add VIN to the separate list

    found = False  # Initialize flag for each VariableID
    for item in record['Results']:
        var_id = item['VariableId']
        if var_id in variable_id_map:  # Check if this VariableID is in our mapping
            row_data[variable_id_map[var_id]] = item['Value']  # Add it to the row data dictionary
            found = True

    if not found:  # If a VariableID is not found, we can handle it here (optional)
        pass

    all_records.append(row_data)  # Add this VIN's data to the all_records list

# Create a DataFrame from the list of dictionaries
final_df = pd.DataFrame(all_records)

# Save DataFrame to CSV
final_df.to_csv('extended_vin_data.csv', index=False)

print("Extended VIN data saved to 'extended_vin_data.csv'")


# Save data
df = pd.DataFrame(all_data)
df.to_csv('vin_data.csv', index=False)

print("Data saved to 'vin_data.csv'")
