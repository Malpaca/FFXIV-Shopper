import argparse
import os
import json
import requests

from Shopper import Shopper

def main(file, datacenter, verbose):
    #----------
    # File path name check
    if not os.path.isfile(file):
        print("Provided file path not found")
        exit()
    # Datacenter name check
    try:
        universalis_query = 'https://universalis.app/api/v2/data-centers'
        dc_request = requests.get(universalis_query)
    except:
        print('Error when requesting Universalis API, try later and check API status')
    available_dcs = [x['name'].lower() for x in dc_request.json()]
    if datacenter.lower() not in available_dcs:
        print("Provided datacenter does not exist")
        exit()
    # Message to indicate valid argument
    print("File and Datacenter Valid, creating shopping list")
    #----------
    # Load MakePlace JSON
    try:
        item_data = json.load(open(file))
    except:
        print("Error when loading JSON file")

    # Load data into shopper and make optimized list
    shopper = Shopper(item_data, datacenter, verbose)
    shopper.make_shopping_list()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a 'optimized' shopping list given makeplace JSON itemlist")
    parser.add_argument('--file', '-f', dest='file', required=True, help='Path to json')
    parser.add_argument('--datacenter', '-dc', dest='dc', required=True, help='Shopper datacenter name')
    parser.add_argument('--verbose', '-v', dest='v', action='store_true', help='Verbose, display specific listing for each item instead of just average')
    args = parser.parse_args()

    try:
        file = args.file
        datacenter = args.dc
        verbose = args.v
    except ValueError:
        print("args parser error, this should never happen, if it does, congrat!")
        exit()

    main(file, datacenter, verbose)
