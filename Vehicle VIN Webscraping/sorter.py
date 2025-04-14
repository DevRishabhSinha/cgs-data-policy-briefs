import csv

# File paths
input1_file = "DR2114_Data_new.csv"  # First CSV (VIN, Registration Date)
input2_file = "final_vehicles_filled.csv"  # Second CSV (Detailed Vehicle Info)
sorted_output_file = "sorted_vins.csv"  # Output CSV for sorted VINs

def load_vins_from_csv(file_path, vin_column_name):
    """Load VINs from a CSV file and return as a list."""
    vins = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            vins.append(row[vin_column_name].strip())
    return vins

def sort_csv_by_vins(input1_file, input2_file, sorted_output_file):
    """Sort rows of input2.csv based on the VIN order in input1.csv and save to sorted_output_file."""
    vin_order = load_vins_from_csv(input1_file, "VIN")
    
    with open(input2_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        
    # Sort rows based on VIN order in input1.csv
    vin_to_row = {row["VIN"].strip(): row for row in rows}
    sorted_rows = [vin_to_row[vin] for vin in vin_order if vin in vin_to_row]
    
    # Write sorted rows to a new CSV
    with open(sorted_output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(sorted_rows)
    
    print(f"Sorted CSV saved to {sorted_output_file}")

# Run function
sort_csv_by_vins(input1_file, input2_file, sorted_output_file)
