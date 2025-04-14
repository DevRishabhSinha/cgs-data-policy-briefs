import requests
import csv
from datetime import datetime
from typing import Dict, List, Any
import time

class EVStationCollector:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = 'https://api.openchargemap.io/v3/poi/'
        self.locations = [
            {'latitude': 37.0902, 'longitude': -95.7129, 'distance': 1600},  # Central US
            {'latitude': 40.7128, 'longitude': -74.0060, 'distance': 800},   # Northeast (NYC)
            {'latitude': 34.0522, 'longitude': -118.2437, 'distance': 800},  # West Coast (LA)
            {'latitude': 47.6062, 'longitude': -122.3321, 'distance': 800},  # Northwest (Seattle)
            {'latitude': 29.7604, 'longitude': -95.3698, 'distance': 800},   # South (Houston)
            {'latitude': 41.8781, 'longitude': -87.6298, 'distance': 800}    # Midwest (Chicago)
        ]
        self.all_stations = {}
        
        # Define CSV headers
        self.csv_headers = [
            'StationID', 'LocationName', 'Address', 'City', 'State', 'Postcode', 
            'Country', 'Latitude', 'Longitude', 'PlugTypes', 'PowerKW', 'Quantity',
            'NetworkProvider', 'UsageType', 'Status', 'LastVerified', 'Comments',
            'UsageCost', 'PaymentRequired', 'MembershipRequired'
        ]

    def safe_get(self, obj: Dict[str, Any], *keys: str, default: Any = 'N/A') -> Any:
        """Safely get nested dictionary values"""
        try:
            for key in keys:
                if obj is None:
                    return default
                obj = obj.get(key)
            return obj if obj is not None else default
        except (AttributeError, TypeError):
            return default

    def format_comment(self, comment: Dict[str, Any]) -> str:
        """Format a user comment with all available information"""
        if not comment:
            return ""
        
        parts = []
        date_created = self.safe_get(comment, 'DateCreated')
        if date_created:
            parts.append(f"Date: {date_created}")
        
        username = self.safe_get(comment, 'UserName')
        if username:
            parts.append(f"User: {username}")
        
        comment_text = self.safe_get(comment, 'Comment')
        if comment_text:
            parts.append(f"Comment: {comment_text}")
        
        status = self.safe_get(comment, 'CheckinStatusType', 'Title')
        if status:
            parts.append(f"Status: {status}")
        
        url = self.safe_get(comment, 'RelatedURL')
        if url:
            parts.append(f"URL: {url}")
        
        return " | ".join(parts)

    def process_comments(self, station: Dict[str, Any]) -> str:
        """Process and merge all types of comments for a station"""
        comments = []
        
        # General comments
        general_comment = self.safe_get(station, 'GeneralComments')
        if general_comment and general_comment != 'N/A':
            comments.append(f"General: {general_comment}")
        
        # User comments
        if station.get('UserComments'):
            for comment in station['UserComments']:
                formatted = self.format_comment(comment)
                if formatted:
                    comments.append(formatted)
        
        # Media comments
        if station.get('MediaItems'):
            for item in station['MediaItems']:
                if item.get('Comment'):
                    media_comment = f"Media {self.safe_get(item, 'DateCreated', default='')}: {item['Comment']}"
                    if item.get('ItemURL'):
                        media_comment += f" (URL: {item['ItemURL']})"
                    comments.append(media_comment)
        
        # Access comments
        access_comment = self.safe_get(station, 'AddressInfo', 'AccessComments')
        if access_comment and access_comment != 'N/A':
            comments.append(f"Access: {access_comment}")
        
        # Return empty string if no comments, otherwise join with comma
        return ', '.join(comments) if comments else ''

    def fetch_data(self):
        """Fetch data from the API"""
        for loc in self.locations:
            params = {
                'output': 'json',
                'latitude': loc['latitude'],
                'longitude': loc['longitude'],
                'distance': loc['distance'],
                'maxresults': 100000,
                'includecomments': True,  # Include user comments
                'verbose': True,          # Get full details
                'key': self.api_key
            }
            
            try:
                response = requests.get(self.url, params=params)
                response.raise_for_status()
                data = response.json()
                
                for station in data:
                    station_id = station.get('ID')
                    if station_id and station_id not in self.all_stations:
                        self.all_stations[station_id] = station
                
                print(f"Successfully processed location: {loc['latitude']}, {loc['longitude']}")
                time.sleep(1)  # Rate limiting
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for coordinates {loc['latitude']}, {loc['longitude']}: {e}")
            except Exception as e:
                print(f"Unexpected error processing location {loc['latitude']}, {loc['longitude']}: {e}")

    def process_station(self, station: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single station's data"""
        try:
            address_info = self.safe_get(station, 'AddressInfo', default={})
            connections = self.safe_get(station, 'Connections', default=[])
            usage_type = self.safe_get(station, 'UsageType', default={})
            status_type = self.safe_get(station, 'StatusType', default={})
            operator_info = self.safe_get(station, 'OperatorInfo', default={})

            # Process comments
            merged_comments = self.process_comments(station)

            # Process connection data
            plug_types = []
            power_values = []
            quantity = 0
            
            for conn in connections:
                if not conn:
                    continue
                    
                conn_type = self.safe_get(conn, 'ConnectionType', default={})
                title = self.safe_get(conn_type, 'Title')
                if title:
                    plug_types.append(title)
                
                power = self.safe_get(conn, 'PowerKW')
                if power:
                    power_values.append(str(power))
                
                qty = self.safe_get(conn, 'Quantity', default=0)
                if isinstance(qty, (int, float)):
                    quantity += qty

            return {
                'StationID': self.safe_get(station, 'ID'),
                'LocationName': self.safe_get(address_info, 'Title'),
                'Address': self.safe_get(address_info, 'AddressLine1'),
                'City': self.safe_get(address_info, 'Town'),
                'State': self.safe_get(address_info, 'StateOrProvince'),
                'Postcode': self.safe_get(address_info, 'Postcode'),
                'Country': self.safe_get(address_info, 'Country', 'Title'),
                'Latitude': self.safe_get(address_info, 'Latitude'),
                'Longitude': self.safe_get(address_info, 'Longitude'),
                'PlugTypes': ', '.join(plug_types) if plug_types else 'N/A',
                'PowerKW': ', '.join(power_values) if power_values else 'N/A',
                'Quantity': quantity,
                'NetworkProvider': self.safe_get(operator_info, 'Title'),
                'UsageType': self.safe_get(usage_type, 'Title'),
                'Status': self.safe_get(status_type, 'Title'),
                'LastVerified': self.safe_get(station, 'DateLastVerified'),
                'Comments': merged_comments,
                'UsageCost': self.safe_get(station, 'UsageCost'),
                'PaymentRequired': self.safe_get(usage_type, 'IsPayAtLocation'),
                'MembershipRequired': self.safe_get(usage_type, 'IsMembershipRequired')
            }
        except Exception as e:
            print(f"Error processing station {self.safe_get(station, 'ID', default='Unknown')}: {e}")
            return {header: 'Error' for header in self.csv_headers}

    def save_to_csv(self, filename: str = 'ev_charging_stations_usa_three.csv'):
        """Save all station data to CSV"""
        print(f"Writing {len(self.all_stations)} stations to CSV...")
        
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.csv_headers)
                writer.writeheader()
                
                for station in self.all_stations.values():
                    processed_data = self.process_station(station)
                    writer.writerow(processed_data)
            
            print(f"Data successfully saved to '{filename}'")
        except Exception as e:
            print(f"Error saving to CSV: {e}")

def main():
    # Initialize with your API key
    api_key = 'c0b81fcf-a1b0-4923-8cdd-aaeed7bb06b0'
    collector = EVStationCollector(api_key)
    
    # Fetch and process the data
    collector.fetch_data()
    
    # Save to CSV
    collector.save_to_csv()

if __name__ == "__main__":
    main()