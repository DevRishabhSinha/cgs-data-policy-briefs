import csv

# Specify the input and output file names
input_filename = 'scraped_info (7).csv'
output_filename = 'output.csv'

with open(input_filename, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    # Read the header (first row) and store it separately
    header = next(reader)
    # Read the rest of the rows into a list
    rows = [row for row in reader]

with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    # Write the header to the output file
    writer.writerow(header)
    # Write the rows 10 times in sequence
    for _ in range(10):
        writer.writerows(rows)
