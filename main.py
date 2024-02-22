import argparse
import os
import json
import requests

from Classes import Item, World, Shopper

def arg_check(file, datacenter):
    #----------
    # File path name check
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

def process_and_make_list(file, datacenter, verbose, seperate):
    #----------
    # Load MakePlace JSON
    try:
        item_data = json.load(open(file))
    except:
        print("Error when loading JSON file")

    #----------

    count = 0
    tot_count = 0
    print("Reading JSON file")

    coverages = ["interiorFurniture", "exteriorFurniture", "interiorFixture", "exteriorFixture"]

    if seperate:
        num_shopper = 4
        shoppers = [None] * num_shopper

        for i, coverage in enumerate(coverages):
            shoppers[i] = Shopper(datacenter, coverage, verbose)
            for furniture in item_data[coverage]:
                if furniture["itemId"] not in shoppers[i].items:
                    count+=1
                    shoppers[i].items[furniture["itemId"]] = Item(furniture["name"])
                shoppers[i].items[furniture["itemId"]].quantity += 1
            if count != 0:
                print(f"Received {count} items from interior furniture section")
                tot_count += count
                count = 0
    else:
        shoppers = [Shopper(datacenter, "All", verbose)]
        for i, coverage in enumerate(coverages):
            for furniture in item_data[coverage]:
                if furniture["itemId"] not in shoppers[0].items:
                    count+=1
                    shoppers[0].items[furniture["itemId"]] = Item(furniture["name"])
                shoppers[0].items[furniture["itemId"]].quantity += 1
            if count != 0:
                print(f"Received {count} items from interior furniture section")
                tot_count += count
                count = 0

    print(f"Total {tot_count} unique items received from JSON file")

        # for furniture in data["interiorFurniture"]:
        #     if furniture["itemId"] not in self.items:
        #         count+=1
        #         self.items[furniture["itemId"]] = Item(furniture["name"])
        #     self.items[furniture["itemId"]].quantity += 1
        # if count != 0:
        #     print(f"Received {count} items from interior furniture section")
        #     tot_count += count
        #     count = 0
        #
        # for furniture in data["exteriorFurniture"]:
        #     if furniture["itemId"] not in self.items:
        #         count+=1
        #         self.items[furniture["itemId"]] = Item(furniture["name"])
        #     self.items[furniture["itemId"]].quantity += 1
        # if count != 0:
        #     print(f"Received {count} items from interior furniture section")
        #     tot_count += count
        #     count = 0
        #
        # for furniture in data["interiorFixture"]:
        #     if furniture["itemId"] not in self.items:
        #         count+=1
        #         self.items[furniture["itemId"]] = Item(furniture["name"])
        #     self.items[furniture["itemId"]].quantity += 1
        # if count != 0:
        #     print(f"Received {count} items from interior furniture section")
        #     tot_count += count
        #     count = 0
        #
        # for furniture in data["exteriorFixture"]:
        #     if furniture["itemId"] not in self.items:
        #         count+=1
        #         self.items[furniture["itemId"]] = Item(furniture["name"])
        #     self.items[furniture["itemId"]].quantity += 1
        # if count != 0:
        #     print(f"Received {count} items from interior furniture section")
        #     tot_count += count
        #     count = 0

    # optimize list
    for shopper in shoppers:
        shopper.create_shopping_list()

    for shopper in shoppers:
        shopper.print_shopping_list()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a 'optimized' shopping list given makeplace JSON itemlist")
    parser.add_argument('--file', '-f', required=True, help='Path to json')
    parser.add_argument('--datacenter', '-dc', required=True, help='Shopper datacenter name')
    parser.add_argument('--verbose', action='store_true', help='Verbose, display specific listing for each item instead of just average')
    parser.add_argument('--seperate', action='store_true', help='Create different shopping list for each section of the JSON file: interior/exterior fixture/furnitures')
    args = parser.parse_args()

    try:
        file = args.file
        datacenter = args.datacenter
        verbose = args.verbose
        seperate = args.seperate
    except ValueError:
        print("args parser error, this should never happen, if it does, congrat! open an issue on the github page please")
        exit()

    arg_check(file, datacenter)
    process_and_make_list(file, datacenter, verbose, seperate)
