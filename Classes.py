import time
import requests
import json
import sys
import numpy as np
from datetime import datetime

class Item:
    def __init__(self, name):
        self.name = name
        self.quantity = 0
        self.world_prices = {} #structure: {worldname: {{"price per unit", "quantity"}...}}
        self.alteration = 0
        self.not_on_market = False

    def add_listing(self, worldname, priceperunit, quantity):
        if worldname in self.world_prices:
            self.world_prices[worldname].append({"price per unit":priceperunit, "quantity":quantity})
        else:
            self.world_prices[worldname]=[{"price per unit":priceperunit, "quantity":quantity}]

class World:
    def __init__(self, name):
        self.name = name
        self.dcRegion = ''
        self.item_prices = {}
        self.world_total_price = 0

    def add_listing(self, item_name, listings):
        if item_name in self.item_prices:
            self.item_prices[item_name]["listings"].extend(listings)
        else:
            self.item_prices[item_name]={"listings":listings}

    def calculate_prices(self):
        for item in self.item_prices.values():
            item_total_price = 0
            item_total_count = 0
            for listing in item["listings"]:
                item_total_count += listing ["quantity"]
                item_total_price += listing["price per unit"] * listing ["quantity"]
                self.world_total_price += listing["price per unit"] * listing ["quantity"]
            item["total_price"] = item_total_price
            item["quantity"] = item_total_count
            item["average"] = int(item_total_price/item_total_count)

class Shopper:
    def __init__(self, datacenter, coverage, output, verbose):
        self.items = {}
        self.worlds = {}
        self.datacenter = datacenter
        self.coverage = coverage
        self.verbose = verbose
        self.alteration_exist = False
        self.not_on_market_exist = False
        self.output = output if output != None else sys.stdout

    def create_shopping_list(self):
        self.fetch_and_optimize_listing()
        self.reorganize_listing()






    def fetch_and_optimize_listing(self):
        # Assume total itemlist is smaller than 100
        # will add a check that breaks up itemIds if its larger than 100 unique items
        print(f"Fetching item sells data and optimizing for \"{self.coverage}\"")
        for itemid in self.progressbar(self.items.keys()):
            listing_count = min(self.items[itemid].quantity+10, 100)
            try:
                universalis_query = 'https://universalis.app/api/v2/{worldDcRegion}/{itemIds}?listings={listings}&entries=0'
                price_request = requests.get(universalis_query.format(
                    worldDcRegion=self.datacenter, itemIds=itemid, listings=listing_count))
                prices = price_request.json()
            except:
                print('Error when requesting Universalis API, try later and check API status, shopper disconnecting')
                universalis_query = 'https://universalis.app/api/v2/{worldDcRegion}/{itemIds}?listings={listings}&entries=0'
                price_request = requests.get(universalis_query.format(
                    worldDcRegion=self.datacenter, itemIds=itemid, listings=listing_count))
                prices = price_request.json()
                exit()

            # print(json.dumps(prices, indent=4))

            if prices["itemID"] != itemid:
                self.items[itemid].not_on_market = True
                self.not_on_market_exist = True
                continue
            else:
                sack_size = int(np.ceil(self.items[itemid].quantity*1.5)) #I know this is ugly, but since we already use argmin from numpy for search speedup, why not also use it for ceiling
                sack = [float('inf')] * sack_size
                sack[0] = 0
                sack_listings = [[]] * sack_size
                for listing in prices["listings"]:
                    for i in range(sack_size-1, -1, -1):
                        if i - listing["quantity"] < 0:\
                            continue
                        new_sack = sack[i-listing["quantity"]] + listing["pricePerUnit"]*listing["quantity"]
                        if new_sack < sack[i]:
                            sack[i] = new_sack
                            sack_listings[i] = sack_listings[i-listing["quantity"]]+[(listing["worldName"], listing["pricePerUnit"], listing["quantity"])]
                index_min = np.argmin(sack[self.items[itemid].quantity:])+self.items[itemid].quantity
                # index may not be true min, check if corresponding value is finite, if its not return the right
                if np.isposinf(sack[index_min]):
                    for i in range(sack_size-1, -1, -1):
                        if not np.isposinf(sack[i]):
                            index_min = i
                            break
                self.items[itemid].alteration = sack[index_min] - self.items[itemid].quantity
                for listing in sack_listings[index_min]:
                    self.items[itemid].add_listing(listing[0], listing[1], listing[2]) #listing["worldName"], listing["pricePerUnit"], listing["quantity"]
        # print(sack, sack_listings, index_min)
        # print(self.items[22569].world_prices)
        # exit()




    def reorganize_listing(self):
        print(f"Reorganizing fetched listing data by worlds for \"{self.coverage}\"")
        for item in self.progressbar(self.items.values()):
            for world, listings in item.world_prices.items():
                if world not in self.worlds:
                    self.worlds[world] = World(world)
                self.worlds[world].add_listing(item.name, listings)
        for world in self.worlds.values():
            world.calculate_prices()
        # Find DCRegion name for each world
        try:
            universalis_query = 'https://universalis.app/api/v2/data-centers'
            dc_request = requests.get(universalis_query, timeout=1)
            universalis_query = 'https://universalis.app/api/v2/worlds'
            world_request = requests.get(universalis_query, timeout=1)
        except:
            print('Error when requesting Universalis API, try later and check API status')
            exit()
        for world in self.worlds.values():
            dc_entries = dc_request.json()
            world_entries = world_request.json()
            world_id = None
            for world_entry in world_entries:
                if world.name == world_entry['name']:
                    world_id = world_entry['id']
            for dc_entry in dc_entries:
                if world_id in dc_entry['worlds']:
                    world.dcRegion = dc_entry['name'] + ' ' + dc_entry['region']
        # Testing World data storage
        # for world in self.worlds.values():
        #     print(world.name, world.item_prices)



# Function that handles printing to
    def progressbar(self, it, prefix="", size=40): # Python3.6+
        count = len(it)
        start = time.time()
        def show(j):
            x = int(size*j/count)
            remaining = ((time.time() - start) / j) * (count - j)

            mins, sec = divmod(remaining, 60)
            time_str = f"{int(mins):02}:{int(sec):02}"

            print(f"  {prefix}[{u'█'*x}{('.'*(size-x))}] {j}/{count} Est wait {time_str}", end='\r', flush=True)

        for i, item in enumerate(it):
            yield item
            show(i+1)
        print("", flush=True)

    def print_shopping_list(self):
    # def print_shopping_list(self):
        #---Header---
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f"\n\n\nShopping list for \"{self.coverage}\" created on {dt_string}", file=self.output)

        #---World_shopping_list---
        for world in self.worlds.values():
            print('------------------------', file=self.output)
            print(f'In {world.name} {world.dcRegion}, {world.world_total_price:,} gil total', file=self.output)
            for item_name, item in world.item_prices.items():
                name = item_name+','
                print(f'\u2514\u2500 {item["quantity"]:>4}x {name:<32} avg price:{item["average"]}', file=self.output)
                if self.verbose:
                    for listing in item["listings"]:
                        print(f'       \u2514\u2500 {listing["quantity"]:>4,} listed,  price per unit:{listing["price per unit"]:,}', file=self.output)
        print('------------------------', file=self.output)

        #---Footer---
        total_price = sum([world.world_total_price for world in self.worlds.values()])
        print(f"Total Cost: {total_price:,} gil", file=self.output)
        print(f"Items found on {', '.join(x for x in self.worlds.keys())}", file=self.output)
        if self.alteration_exist:
            print("\nThe following item differs from item list file", file=self.output)
            for item in self.items.values():
                if item.alteration:
                    print(f"   {item.alteration:>4}x {item.name}", file=self.output)
        if self.not_on_market_exist:
            print(f"\nThe following item cannot be found on {self.datacenter} marketboard", file=self.output)
            for item in self.items.values():
                if item.not_on_market:
                    print(f"   {item.quantity:>4}x {item.name}", file=self.output)
        print("\nShopper disconnected, thank you for shopping!", file=self.output)
