import argparse
import os
import json
import requests

from Classes import Item, World, Shopper

def arg_check(files, datacenter):
    #----------
    # File path name check
    for file in files:
        if not os.path.isfile(file):
            print("Provided file path not found")
            exit()
    # Datacenter name check
    dc_request = requests.get('https://universalis.app/api/v2/data-centers')
    try:
        universalis_query = 'https://universalis.app/api/v2/data-centers'
        dc_request = requests.get(universalis_query, timeout=1)
    except:
        print('Error when requesting Universalis API, try later and check API status')
        exit()
    available_dcs = [x['name'].lower() for x in dc_request.json()]
    if datacenter.lower() not in available_dcs:
        print("Provided datacenter does not exist")
        exit()
    # Message to indicate valid argument
    print("File and Datacenter Valid, creating shopping list")

def process_and_make_list(files, datacenter, verbose, seperate):
    # not so useful counter for flair
    count = 0
    tot_count = 0

    # some variable and name definition
    num_shopper = 4 + len(files) - 1
    coverages = ["interiorFurniture", "exteriorFurniture", "interiorFixture", "exteriorFixture"]

    shoppers = []
    for file in files:
        shopper_name = file.split('.')[0]
        if file.lower().endswith("json"):
            print("Reading JSON file")
            try:
                item_data = json.load(open(file))
            except:
                print("Error when loading JSON file")


            for i, coverage in enumerate(coverages):
                if seperate:
                    shoppers.append(Shopper(datacenter, shopper_name + ':' + coverage, verbose))
                else:
                    if i==0:
                        shoppers.append(Shopper(datacenter, shopper_name + ':' + "All", verbose))
                for furniture in item_data[coverage]:
                    if furniture["itemId"] not in shoppers[i*seperate].items:
                        count+=1
                        shoppers[i*seperate].items[furniture["itemId"]] = Item(furniture["name"])
                    shoppers[i*seperate].items[furniture["itemId"]].quantity += 1
                if count != 0:
                    print(f"Received {count} items from interior furniture section")
                    tot_count += count
                    count = 0
        elif file.lower().endswith("csv"):
            print("CSV file detected, this functionality isn't implimented yet, skipping this file")
        else:
            print("Unsupported file format, skipping this file")

    print(f"Total {tot_count} unique items received from JSON file")

    # optimize list
    for shopper in shoppers:
        shopper.create_shopping_list()

    # output shopping list
    for shopper in shoppers:
        shopper.print_shopping_list()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a 'optimized' shopping list given makeplace JSON itemlist")
    parser.add_argument('--file', '-f', nargs='+', required=True, help='Path to json')
    parser.add_argument('--datacenter', '-dc', required=True, help='Shopper datacenter name')
    parser.add_argument('--seperate', action='store_true', help='Create different shopping list for each section of the JSON file: interior/exterior fixture/furnitures')
    parser.add_argument('--verbose', action='store_true', help='Verbose, display specific listing for each item instead of just average')
    args = parser.parse_args()

    try:
        files = args.file
        datacenter = args.datacenter
        verbose = args.verbose
        seperate = args.seperate
    except ValueError:
        print("args parser error, this should never happen, if it does, congrat! open an issue on the github page please")
        exit()

    arg_check(files, datacenter)
    process_and_make_list(files, datacenter, verbose, seperate)
