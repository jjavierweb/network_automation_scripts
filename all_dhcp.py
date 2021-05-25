import json
import csv
from netaddr import *


def load_file(file_name):

    """
    This function loads a file based on a name
    The file must be on the same location as this script

    It returs a dictionary from the json file
    """

    # creates an empty dictionary
    dhcp_data = {}
    # open the file
    with open(file_name) as f:
        # add the json data to the dict
        dhcp_data.update(json.load(f))
    # return the dictionary
    return dhcp_data["subnets"]


def output_data(file_name, data):

    """
    This function requires a file name and a list

    This will go over the list and will create a file
    in the same location as this scrip with the provided
    name
    """
    # create the file
    with open(file_name, "w") as csv_f:
        field_names = ["Device", "IP Total", "Used IPs", "Free IPs"]
        writer = csv.DictWriter(csv_f, fieldnames=field_names)

        writer.writeheader()
        for item in data:
            writer.writerow(item)


def analyze_pools(location_list, ip_data):

    """
    This function received 2 lists and returns a list with multiple Dictionaries on it

    The first list should contain a list of names "locations" that are used to match
    with the second list( which contains the data )
    """

    # initlize list to store a number of dictionaries inside
    locations_data = []

    # loop over each provided location
    for location in location_list:
        # initialize counters for IPs
        total_ips = 0
        total_free = 0
        total_used = 0
        # loop over each data set from the provided IP data
        for item in ip_data:
            # check that the locations for the data set are the same as the required locations
            if location == item["location"] or location is item["location"]:
                # verify that the IP data to analyze is not in the RFC1918 and add them to totals
                if not (IPAddress(item["first_ip"]).is_private()):
                    total_ips += item["defined"]
                    total_free += item["free"]
                    total_used += item["used"]
        # Adds a dictionary to a list
        locations_data.append(
            {
                "Device": location,
                "IP Total": total_ips,
                "Used IPs": total_used,
                "Free IPs": total_free,
            }
        )
    # Call the output data function to print all to csv file
    output_data("data.csv", locations_data)


def analyze_locations(file_name):
    """
    This function will receive a file name in the form of a function
    The file name and the function call is stored inside a variable
    as the file_name returns a dictionary

    Then we analyze this data and return a set of locations
    """

    # call the load_file function to return the dict that holds all data
    data = file_name
    # Create an empty list to store each location
    locations_names = set([])
    # this will store a dict with all the data per location

    # loop over all the data
    for subnet in data:
        # Grab only the names that have the CPE or internet Name on them
        if (
            subnet["location"][-3:].lower() == "cpe"
            or subnet["location"][:12].lower() == "fttxinternet"
        ):
            # check the location and if it is not duplicated, then add it to the array
            locations_names.add(subnet["location"])

    # call the analyze_pools function and pass the locations and the data
    analyze_pools(locations_names, data)


# Call the analyze_data function
analyze_locations(load_file("test.json"))
