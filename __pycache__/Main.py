import csv
from datetime import datetime, timedelta
from Package import Package
from csv import reader
from Hash_Table import Hash_Table, hash_table

# Get today's date for dynamic time calculations
today = datetime.now().date()

#Write a data structure for the distance data - 2 data structures: a list of lists, 0 holds the data floats from the distance table 
#Create a dictionary to map addresses to their corresponding index in the distance table
#The indices of the current location of the truck and next location of the truck will be used to look up the distance in the distance table

#import the distance and address data from the csv files and store them in the appropriate data structures
distance_matrix= []
address_dict = {}
        
#Get the address data
with open('Address.csv','r',encoding='utf-8-sig') as address_file:
    reader = csv.reader(address_file)

    index = 0

    for row in reader:
        if not row:
            continue #skipping blank lines
        #extract just the street address from the CSV row
        address_string = row[0]
        address_line = address_string.split('\n')

        if len(address_line)>1:
            clean_address = address_line[1].strip()
        else:
            # If no newline, try splitting by comma (for format "Name,Address")
            address_parts = address_string.split(',')
            if len(address_parts) > 1:
                clean_address = address_parts[1].strip()
            else:
                clean_address = address_parts[0].strip()
        
        #make sure data matches package.csv
        if "4001 South 700 East" in clean_address:
            clean_address = "4001 South 700 East"
        if "13302100 S" in clean_address:
            clean_address = "1330 2100 S"
        if "14884800 S" in clean_address:
            clean_address = "1488 4800 S"
        if "3575 W Valley Central" in clean_address:
            clean_address = "3575 W Valley Central Station bus Loop"

        #map new string to index
        address_dict[clean_address] = index

        index +=1

with open('Distance.csv', 'r',encoding='utf-8-sig') as distance_file:
    reader = csv.reader(distance_file)


    for row in reader:
        if not row:
            continue #skipping blank lines


        distance_row = [float(distance) if distance != '' else 0.0 for distance in row]

        distance_matrix.append(distance_row)


def distance_between(address1, address2):
    index1 = address_dict[address1]
    index2 = address_dict[address2]
    #get distance from the matrix

    distance = distance_matrix[index1][index2]

    if distance == 0.0 and index1 != index2:
        distance = distance_matrix[index2][index1]
    return distance


### --Create the Distance Algorithm

# Load the trucks and their deadlines, keeping track of total mileage

#Truck1: Early Delivery 9am - 10:30 am.
#package 14  must be delivered with 15 and 19
#package 16 must be delivered with 13 and 19
#package 20 must be delivered with 13 and 15
truck_1_list = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40, 10, 11, 12]

#Truck 2: delayed packages (6, 25, 28, 32) and packages restricted to truck 2 (
truck_2_list = [3, 6, 18, 25, 28, 32, 36, 38, 2, 4, 5, 7, 8, 17, 21, 22]
#Truck 3: Package 9 (wrong address) and EOD packages leftover
truck_3_list = [9, 23, 24, 26, 27, 33, 35, 39]

total_mileage = 0.0
#Implement the nearest neighbor algorithm, updating the time for every package.
def delivery_route(truck_list, start_time):
    global total_mileage

    #truck starts at hub:
    current_location = "4001 South 700 East"
    current_time = start_time

    # Set loading times for all packages at the hub
    for package_id in truck_list:
        package = hash_table.lookup(package_id)
        package.loading_time = start_time
        
    # Loop through packages, distance and trucks to confirm all packages are delivered, removing delivered package Ids from the list.
    while len(truck_list) > 0:
        nearest_location = float('inf')
        next_package = None
        
        # find the nearest location for undelivered packages
        for package_id in truck_list:
            package = hash_table.lookup(package_id)
            
            # find package 9 (wrong address until 10:20 am)
            if package.package_id == 9:
                package_9_time = datetime.combine(today, datetime.min.time()).replace(hour=10, minute=20)
                if current_time < package_9_time:
                    continue  # Skip package 9 until the address is updated at 10:20 am
                else:
                    # Update package 9's address after 10:20 am
                    package.address = "410 S State St"
                    package.zip_code = "84111"
                          
            # find distance to next address
            distance = distance_between(current_location, package.address)

            if distance < nearest_location:
                nearest_location = distance
                next_package = package
                
        # if no package is found - skip ahead to next delivery
        if next_package is None:
            current_time += timedelta(minutes=1)
            continue

        total_mileage += nearest_location
        current_location = next_package.address
        
        # Calculate how long the drive was
        truck_time = (nearest_location / 18.0) * 60
        current_time += timedelta(minutes=truck_time)

        # update package status
        next_package.delivery_time = current_time
        next_package.status = "Delivered"
        
        # remove delivered package
        truck_list.remove(next_package.package_id)
        
    return current_time
              
#Call the function and dispatch the trucks
#truck 1 leaves at 8am
truck_1_start= delivery_route(truck_1_list, datetime.combine(today, datetime.min.time()).replace(hour=8, minute=0))
truck_1_end = delivery_route(truck_1_list, truck_1_start)


#truck 2 leaves at 9:05 am
truck_2_start = delivery_route(truck_2_list, datetime.combine(today, datetime.min.time()).replace(hour=9, minute=5))
truck_2_end = delivery_route(truck_2_list, truck_2_start)

#Driver 1 takes truck 3 and leaves at 10:40 am after package 9 is updated (10:20 am) and truck 1 returns (after 10:35:20 am)
truck_3_start = max(truck_1_end, datetime.combine(today, datetime.min.time()).replace(hour=10, minute=35))
truck_3_end = delivery_route(truck_3_list, truck_3_start)

#connect to the user interface
if __name__ == '__main__':
    import Ui
    Ui.main_menu(hash_table, total_mileage, today)