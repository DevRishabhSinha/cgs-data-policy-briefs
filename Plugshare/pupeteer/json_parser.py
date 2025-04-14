import json
import csv

# Function to parse the JSON data
def parse_json_to_csv(json_data, csv_file_path):
    # Open CSV file for writing
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        # Define the CSV writer
        csvwriter = csv.writer(csvfile)
        
        # Write header row
        header = ['url', 'locationName', 'address', 'plugTypes', 'networkProvider', 'chargingSpeed', 'numberOfChargers', 
                  'poiType', 'amenities', 'hours', 'paymentRequired', 'rate', 'parking', 'review_date', 
                  'review_user', 'review_vehicle', 'review_rating', 'review_comment', 'photos']
        csvwriter.writerow(header)

        # Iterate through the JSON list (each item represents a charging station)
        for item in json_data:
            # Extract common fields
            url = item.get('url', '')
            location_name = item.get('locationName', '')
            address = item.get('address', '')
            plug_types = ', '.join(item.get('plugTypes', []))
            network_provider = item.get('networkProvider', '')
            charging_speed = item.get('chargingSpeed', '')
            number_of_chargers = item.get('numberOfChargers', '')
            poi_type = item.get('poiType', '')
            amenities = ', '.join(item.get('amenities', []))
            hours = item.get('hours', '')
            payment_required = item['pricing'].get('paymentRequired', '') if 'pricing' in item else ''
            rate = item['pricing'].get('rate', '') if 'pricing' in item else ''
            parking = item.get('parking', '')
            photos = ', '.join(item.get('photos', []))
            
            # Process each review
            reviews = item.get('reviews', [])
            if reviews:
                for review in reviews:
                    review_date = review.get('date', '')
                    review_user = review.get('user', '')
                    review_vehicle = review.get('vehicle', '')
                    review_rating = review.get('rating', '')
                    review_comment = review.get('comment', '')
                    
                    # Write the row for each review
                    csvwriter.writerow([url, location_name, address, plug_types, network_provider, charging_speed, 
                                        number_of_chargers, poi_type, amenities, hours, payment_required, rate, 
                                        parking, review_date, review_user, review_vehicle, review_rating, 
                                        review_comment, photos])
            else:
                # Write a row with no reviews
                csvwriter.writerow([url, location_name, address, plug_types, network_provider, charging_speed, 
                                    number_of_chargers, poi_type, amenities, hours, payment_required, rate, 
                                    parking, '', '', '', '', '', photos])

# Load the JSON data
with open('scraped_plugshare_data.json', 'r') as json_file:
    data = json.load(json_file)

# Parse the JSON data into a CSV file
parse_json_to_csv(data, 'charging_stations.csv')

print("CSV file created successfully!")
