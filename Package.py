#Emily Freund
#C950
#011720184
from datetime import datetime

#package class to represent each package with its attributes and methods
class Package:
    def __init__(self, pkg_id, address, pkg_city, pkg_state, zip_code, delivery_deadline, mass_kg, special_notes):
        self.package_id = pkg_id
        self.address = address
        self.city = pkg_city
        self.state = pkg_state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.mass_kg = mass_kg
        self.special_notes = special_notes
        self.status = "At Hub"
        #add attributes for delivery time and loading time, initialized to None
        self.delivery_time = None
        self.loading_time = None
        
    def __str__(self):
        #wrap delivery_time and loading_time in str() to handle None values
        delivery_time_str = str(self.delivery_time) if self.delivery_time else "N/A"
        loading_time_str = str(self.loading_time) if self.loading_time else "N/A"
        
        return f"Package ID: {self.package_id}, Address: {self.address}, City: {self.city}, State: {self.state}, Zip: {self.zip_code}, Deadline: {self.delivery_deadline}, Weight: {self.mass_kg}kg, Notes: {self.special_notes}, Status: {self.status}, Loaded At: {loading_time_str}, Delivered At: {delivery_time_str}"