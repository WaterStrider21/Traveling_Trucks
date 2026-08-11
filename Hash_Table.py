#Emily Freund
#C950
#011720184
from Package import Package
import csv

#hash table class to store packages with chaining for collision resolution
class Hash_Table:
    def __init__(self):
        self.table = [[] for _ in range(10)]  # Initialize hash table with 10 buckets
        
    def insert(self, package):
        key = package.package_id % 10
        self.table[key].append(package)  # Insert package into the appropriate bucket
    
    def  lookup(self,package_id):
        key = package_id % 10  # Compute hash key
        for package in self.table[key]:  # Search for the package in the bucket
            if package.package_id == package_id:
                return package 
        return None
    #Str and repr methods for better visualization of the hash table
    def __str__(self):
        bucket_counts = [len(bucket) for bucket in self.table]
        return f"Hash_Table with {len(self.table)} buckets: {bucket_counts}"
    def __repr__(self):
        return f"Hash_Table({self.table})"

# Implement a method to load packages from a CSV file
hash_table = Hash_Table()

with open('Package.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    for row in reader:
        if not row:
            continue
        pkg_id = int(row[0])
        address = row[1]
        pkg_city = row[2]
        pkg_state = row[3]
        zip_code = row[4]
        delivery_deadline = row[5]
        mass_kg = float(row[6])
        special_notes = row[7] if len(row) > 7 else ""
        package = Package(pkg_id, address, pkg_city, pkg_state, zip_code, delivery_deadline, mass_kg, special_notes)
        hash_table.insert(package)
