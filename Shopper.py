import requests
import json
import time
import numpy as np
from Item import Item
from World import World
from datetime import datetime

class Shopper:
    def __init__(self, data, datacenter, verbose):
        self.items = {}
        self.worlds = {}
        self.datacenter = datacenter
        self.verbose = verbose
        self.alteration_exist = False
        self.not_on_market_exist = False
        self.parse_shoppinglist(data)

    def parse_shoppinglist(self, data):
        # might want to change this to be out of the shopper class and shopper instead take a list of item/count
        for furniture in data["interiorFurniture"]:
            if furniture["itemId"] not in self.items:
                self.items[furniture["itemId"]] = Item(furniture["name"])
            self.items[furniture["itemId"]].quantity += 1
        print(f"Total {len(self.items)} items received from JSON file")

    def make_shopping_list(self):
        self.fetch_and_optimize()
        self.formate_worlds()

        self.print_header()
        self.print_world_shopping_list()
        self.print_footer()






    def fetch_and_optimize(self):
        # Assume total itemlist is smaller than 100
        # will add a check that breaks up itemIds if its larger than 100 unique items
        print("Fetching item sells data and optimizing")
        for itemid in self.progressbar(self.items.keys()):
            listing_count = min(self.items[itemid].quantity+10, 100)
            try:
                universalis_query = 'https://universalis.app/api/v2/{worldDcRegion}/{itemIds}?listings={listings}&entries=0'
                price_request = requests.get(universalis_query.format(
                    worldDcRegion=self.datacenter, itemIds=itemid, listings=listing_count))
                prices = price_request.json()
            except:
                print('Error when requesting Universalis API, try later and check API status, shopper disconnecting')
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




    def formate_worlds(self):
        print("Formating fetched listing data into worlds")
        for item in self.items.values():
            for world, listings in item.world_prices.items():
                if world not in self.worlds:
                    self.worlds[world] = World(world)
                self.worlds[world].add_listing(item.name, listings)
        for world in self.worlds.values():
            world.calculate_prices()
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

            print(f"{prefix}[{u'█'*x}{('.'*(size-x))}] {j}/{count} Est wait {time_str}", end='\r', flush=True)

        for i, item in enumerate(it):
            yield item
            show(i+1)
        print("\n", flush=True)

    def print_header(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f"\nShopping list was created on {dt_string}")

    def print_world_shopping_list(self):
        for world in self.worlds.values():
            print('------------------------')
            print(f'In {world.name}, {world.world_total_price:,} gil total')
            for item_name, item in world.item_prices.items():
                name = item_name+','
                print(f'\u2514\u2500 {item["quantity"]:>4}x {name:<32} avg price:{item["average"]}')
                if self.verbose:
                    for listing in item["listings"]:
                        print(f'       \u2514\u2500 {listing["quantity"]:>4,} listed,  price per unit:{listing["price per unit"]:,}')
        print('------------------------')

    def print_footer(self):
        total_price = sum([world.world_total_price for world in self.worlds.values()])
        print(f"Total Cost: {total_price:,} gil")
        print(f"Items found on {', '.join(x for x in self.worlds.keys())}")
        if self.alteration_exist:
            print("\nThe following item differs from item list file")
            for item in self.items.values():
                if item.alteration:
                    print(f"   {item.alteration:>4}x {item.name}")
        if self.not_on_market_exist:
            print(f"\nThe following item cannot be found on {self.datacenter} marketboard")
            for item in self.items.values():
                if item.not_on_market:
                    print(f"   {item.quantity:>4}x {item.name}")
        # print('')
        # print(f'Could not find these items on the market. Perhaps they are cash shop or not sellable?')
        # for item in alteration:
        #     print(f'{item[2]}x {item[0]}')
        # print('')
        print("\nShopper disconnected, thank you for shopping!")
