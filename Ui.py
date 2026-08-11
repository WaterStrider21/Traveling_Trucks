#Emily Freund
#C950
#011720184
from datetime import datetime, timedelta
#from Hash_Table import Hash_Table, hash_table
from Package import Package

today = datetime.now().date()

# This file contains the user interface for the WGUPS package delivery system. It provides a menu for users to interact with the system and view package information, delivery status, and total mileage.
#Intro
def main_menu(hash_table, total_mileage,today):
    print("Welcome to the WGUPS - Western Governors University Parcel Service- User Portal")
    print(f"Total mileage for all trucks: {total_mileage:.2f} miles")
    print(f"Current date: {today.strftime('%Y-%m-%d')}")
    print("========================================")
    
    
    #Status selection menu
    
    while True:
        print("\nPlease select an option:")
        print("1. View status of all packages")
        print("2. View package by ID")
        print("3. View package by status")
        print("4. View package by Truck")
        print("5. Exit")

        user_choice = input("\nEnter your choice:(1, 2, 3, 4 or 5): ")

        if user_choice == '5':
            print("Are you sure you want to exit? (y/n)")
            confirm = input().lower()
            if confirm == 'y':
                break
        elif user_choice == 'n':
            continue
        elif user_choice in ['1', '2','3','4']:
#request the time
            time_input = input("Enter a time to view package status (HH:MM AM/PM): ")
       
#combine with today:      
        try:
           parsed_time = datetime.strptime(time_input, "%I:%M %p").time()
           combined_datetime = datetime.combine(today, parsed_time)
           print(f"Package status as of {combined_datetime.strftime('%Y-%m-%d %I:%M %p')}:")
           
#continue looping through the menu options           #continue looping through the menu options
#Option 1: view all packages
           if user_choice == '1':
               print(f"\n-- All Packages as of {time_input}--")
               for package_id in range(1, 41):
                   package = hash_table.lookup(package_id)
                   print_package_status(package, combined_datetime, today)
           elif user_choice == '2':
               package_id_input = input("Enter your package ID (1-40): ")
               package= hash_table.lookup(int(package_id_input))
               if package:
                   print(f"\n -- Package Information -- {package.package_id} at time {time_input} --")
                   print_package_status(package, combined_datetime, today)
               else:
                   print("Invalid package ID. Please try again.")
#Option 3: search by status
           elif user_choice == '3':
                status_input = input("Enter status to search for (e.g., 'Delivered', 'En Route', 'At Hub', 'Delayed'): ").lower()
                print(f"\n--- Packages with status '{status_input}' at {time_input} ---")
                    
                found = False
                for package_id in range(1, 41):
                    package = hash_table.lookup(package_id)
                    current_status = get_base_status(package, combined_datetime, today).lower()
                        
                    if status_input in current_status:
                        print_package_status(package, combined_datetime, today)
                        found = True
  #option 4: search by truck                          
                if not found:
                    print("No packages found with that status at that time.")
           elif user_choice == '4':
                truck_input = input("Enter truck number (1, 2, or 3): ")
                if truck_input in ['1', '2', '3']:
                    print(f"\n--- Packages on Truck {truck_input} at {time_input} ---")
                    truck_packages = {
                        '1': [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40, 10, 11, 12],
                        '2': [3, 6, 18, 25, 28, 32, 36, 38, 2, 4, 5, 7, 8, 17, 21, 22],
                        '3': [9, 23, 24, 26, 27, 33, 35, 39]
                    }
                    for package_id in truck_packages[truck_input]:
                        package = hash_table.lookup(package_id)
                        print_package_status(package, combined_datetime,today)
                else:
                    print("Invalid truck number. Please enter 1, 2 or 3.")
                        
        except ValueError:
                print("Invalid time format! Please use HH:MM AM/PM (e.g., 08:35 AM)")
#Set status for delayed packages, packages at the hub, en route, and delivered based on the current time and package attributes
        #delayed packages arrive at 9:05 am
def get_base_status(package, combined_datetime, today):
    if package.package_id in [6, 25, 28, 32] and combined_datetime < datetime.combine(today, datetime.min.time()).replace(hour=9, minute=5):
        return "Delayed"
    elif combined_datetime < package.loading_time:
        return "At Hub"
    elif combined_datetime < package.delivery_time:
        return "En Route"
    else:
        delivered_str = package.delivery_time.strftime('%Y-%m-%d %I:%M %p')
        return f"Delivered at {delivered_str}"
def print_package_status(package, combined_datetime, today):
    display_address = package.address
    display_zip = package.zip_code
    
    if package.package_id == 9 and combined_datetime < datetime.combine(today, datetime.min.time()).replace(hour=10, minute=20):
        display_address = "300 State St"
        display_zip = "84103"
        
    if package.package_id in [6, 25, 28, 32] and combined_datetime < datetime.combine(today, datetime.min.time()).replace(hour=9, minute=5):
        status = "Delayed, package will arrive at hub at 9:05 AM"
    elif combined_datetime < package.loading_time:
        status = "At Hub"
    elif combined_datetime < package.delivery_time:
       status = "En Route"
    else:
        delivered_str = package.delivery_time.strftime('%Y-%m-%d %I:%M %p')
        status = f"Delivered at {delivered_str}"
        status = get_base_status(package, combined_datetime, today)
        
#print the truck number
    if package.package_id in [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40, 10, 11, 12]:
        truck_num = "1"
    elif package.package_id in [3, 6, 18, 25, 28, 32, 36, 38, 2, 4, 5, 7, 8, 17, 21, 22]:
        truck_num = "2"
    else:
        truck_num = "3"
    
    print(f"ID: {package.package_id:2} | Truck: {truck_num} | Status: {status} | Address: {display_address}, {package.city}, {package.state}, {display_zip} | Deadline: {package.delivery_deadline} | Weight: {package.mass_kg} | Notes: {package.special_notes}")