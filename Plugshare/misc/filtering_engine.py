import csv

# Define the input and output file names
input_file_name = 'scraped_info (4).csv'
output_file_name = 'filtered.csv'

# Open the original CSV file to read and the new CSV file to write
with open(input_file_name, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_file_name, mode='w', newline='', encoding='utf-8') as outfile:

    # Create CSV reader and writer
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames  # Capture the fieldnames from the input
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    # Write the header to the output file
    writer.writeheader()

    # Loop through each row in the input CSV
    for row in reader:
        address = row.get('Address', '')  # Get the address from the current row
        # Check if 'MD' or 'DC' is in the address
        if 'MD' in address or 'DC' in address:
            writer.writerow(row)  # Write the row to the output file if condition is met
