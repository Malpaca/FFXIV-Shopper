import argparse
import os
import json

# from Classes import Item, World, Shopper
from Module.Shopper import Shopper

def arg_check(files, dcRegion):
    #----------
    # File path name check
    for file in files:
        if not os.path.isfile(file):
            print("Provided file path not found")
            exit()
    print("File location Valid, creating shopping list")

def process_and_make_list(files, dcRegion, output, seperate, verbose):
    # not so useful counter for flair
    count = 0
    tot_count = 0

    # some variable and name definition
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
                #shopper creation based on user preference (seperated or united)
                if seperate:
                    shoppers.append(Shopper(dcRegion, shopper_name + ':' + coverage, output, verbose))
                else:
                    #only create big shopper at start, ignore creation line after first loop
                    if i==0:
                        shoppers.append(Shopper(dcRegion, shopper_name + ':' + "All", output, verbose))
                #load specific item coverage into the respective shopper
                for furniture in item_data[coverage]:
                    new_item = shoppers[i*seperate].add_item(furniture["itemId"], furniture["name"])
                    count += new_item
                #output message on how many item are added in a specific section
                if count != 0:
                    print(f"Received {count} items from {coverage} section")
                    tot_count += count
                count = 0

        elif file.lower().endswith("csv"):
            print(f"CSV file detected, this functionality isn't implimented yet, skipping file\"{file}\"")
        else:
            print(f"Unsupported file format, skipping file \"{file}\"")

    print(f"Total {tot_count} unique items received from JSON file\n")

    # optimize list
    for shopper in shoppers:
        shopper.create_shopping_list()

    # output shopping list
    for shopper in shoppers:
        shopper.print_shopping_list()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a 'optimized' shopping list given makeplace JSON itemlist")
    parser.add_argument('--File', '-f', nargs='+', required=True, help='Path to json')
    parser.add_argument('--DatacenterRegion', '-dcRegion', required=True, help='Shopper region or datacenter name (use dash in place of space)')
    parser.add_argument('--Output', '-o',  help='Name of output file, also remove the output in command line')
    parser.add_argument('--Seperate', action='store_true', help='Create different shopping list for each section of the JSON file: interior/exterior fixture/furnitures')
    parser.add_argument('--Verbose', action='store_true', help='Verbose, display specific listing for each item instead of just average')
    args = parser.parse_args()

    try:
        files = args.File
        dcRegion = args.DatacenterRegion
        output = args.Output
        seperate = args.Seperate
        verbose = args.Verbose
    except ValueError:
        print("args parser error, this should never happen, if it does, congrat! open an issue on the github page please")
        exit()

    arg_check(files, dcRegion)
    process_and_make_list(files, dcRegion, output, seperate, verbose)
    #handle output argument
