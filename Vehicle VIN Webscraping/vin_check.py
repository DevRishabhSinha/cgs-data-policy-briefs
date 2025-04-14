import csv

input1_file = "DR2114_Data_new.csv"  # First CSV (VIN, Registration Date)
input2_file = "vehicles_filled2copy.csv"  # Second CSV (Detailed Vehicle Info)
output_file = "missing_vins.csv"  # Output CSV for missing VINs

def load_vins_from_csv(file_path, vin_column_name):
    """Load VINs from a CSV file and return as a set."""
    vins = set()
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            vins.add(row[vin_column_name].strip())
    return vins

def find_missing_vins(input1_file, input2_file, output_file):
    """Find VINs in input1 that are not in input2 and save them to output_file."""
    # Load VINs from both CSVs
    input1_vins = load_vins_from_csv(input1_file, "VIN")
    input2_vins = load_vins_from_csv(input2_file, "VIN")
    
    # Find missing VINs
    missing_vins = input1_vins - input2_vins
    
    # Write missing VINs to a new CSV
    with open(input1_file, mode='r', newline='', encoding='utf-8') as file_in, \
         open(output_file, mode='w', newline='', encoding='utf-8') as file_out:
        reader = csv.DictReader(file_in)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(file_out, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            if row["VIN"].strip() in missing_vins:
                writer.writerow(row)
    
    print(f"Missing VINs saved to {output_file}")

# Run the function
find_missing_vins(input1_file, input2_file, output_file)
