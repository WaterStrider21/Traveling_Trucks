# New README File
Author: Emily Freund
Project: Truck Routing Problem
Class: DataStructures and Algorithms II

## Introduction
In this project, I will implement the nearest-neighbor algorithm combined with a chained hash table in Python to determine an efficient route for the distribution hub. Using HTML, CSS and JavaScript I created a customizable visualization of the truck route options.

## Description

 The task is to determine an algorithm, write code, and present a solution where all 40 packages will be delivered on time while meeting each package’s requirements and keeping the combined total distance traveled under 140 miles for all trucks. 
 
Assumptions

•  Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.
•  The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.
•  There are no collisions.
•  Three trucks and two drivers are available for deliveries. Each driver stays with the same truck as long as that truck is in service.
•  Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed.
•  The delivery and loading times are instantaneous (i.e., no time passes while at a delivery or when moving packages to a truck at the hub). This time is factored into the calculation of the average speed of the trucks.
•  There is up to one special note associated with a package.
•  The distances provided in the Distance Table are equal regardless of the direction traveled.
•  The day ends when all 40 packages have been delivered.

## Requirements
Python 3.14.2 64-bit on win32
HTML, CSS, JavaScript
Visual Studio Code
Windows 11 Home—Intel Core i7, 16 GB RAM (or similar)

## To Do
### --Clean distance and package data and convert to CSV. Create and address file and paste the addresses, clean the data.

### --Develop a hash table that takes the package ID as input and inserts the data components into the table:
 •   delivery address
•   delivery deadline
•   delivery city
•   delivery zip code
•   package weight
•   delivery status (i.e., at the hub, en route, or delivered), including the delivery time
--Create package class
    Create a package class to represent each package; you should have all the data in the package file
    Add loading_time and delivery_time variables
    Include __Str__ and __repr__ functions you can print your package objects

--Create Hash table class
    Initialize a hash table with 10 buckets and the ability to append new packages.
    Insert a lookup function to search for the packages in the buckets.
    Include _Str_ and _repr_ functions to visualize the table
### --Create two data structures to map the indices of the address and distance tables
--Create a Main.py file and import CSV, then import all of the python classes (Hash_Table, Package)
--Create two data structures address_dict{} and distance_matrix()
--Clean the address data and make sure it matches the Package file
--Map the cleaned string to the index

--For the distance_matrix{} convert null and integer data to float
--Create a function that finds the distance between two locations

### --Create the Distance Algorithm
-- Load the trucks and their deadlines, keeping track of total mileage
--Implement the nearest neighbor algorithm, updating the time for every package.
--Loop through packages, distance and trucks to confirm all packages are delivered, removing delivered package Ids from the list.
--Call the function and dispatch the trucks

### -- Create a User Interface that can be run from the command line

--Rewrite the truck lists into the Ui.py
--Create an intro with menu options for the user to look up the status by "All","Package ID", "Status" or "Truck Number"
--Ensure the time of day is requested from the user
--Ensure there are error messages for invalid times, truck numbers and invalid package IDs
--import the UI into Main.py and test
### -- Create a user interface that can be run from the web browser

--The frontend is served on port 8080 and fetches route data from the backend at: Frontend: http://localhost:8080
-- Backend API: http://localhost:8001/routes
-- Package filters: The UI includes a dropdown and input field that allow filtering by:

    All Packages
    Package ID
    Package Status
    Truck Number
    Map display
    Hub is shown in the center
    Delivery locations are plotted around the hub
    Truck routes are drawn as lines
    Packages are listed in the side panel
## Usages
This python project loads the data for the WGUPS package delivery system into a hash table. It provides a menu for users to interact with the system and view package information, delivery status, and total mileage. It can be modified for a variety of delivery route problems

## References
“Hash table.” Wikipedia, https://en.wikipedia.org/wiki/Hash_table. Accessed 15 April 2026.

“Nearest neighbor algorithm.” Wikipedia, https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm. Accessed 12 April 2026.

Lysecky, R., & Vahid, F. (2018, June). C950: Data Structures and Algorithms II. zyBooks.
Retrieved 12 April 2026, from  https://learn.zybooks.com/zybook/WGUC950AY20182019/
