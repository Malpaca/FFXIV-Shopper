import time
import sys
from datetime import datetime
from .Optimizer import Optimizer
from .UniversalisAPIWrapper import Universalis

class Shopper:
    def __init__(self, datacenter, coverage, output, verbose):
        self.optimizer = Optimizer()
        self.universalis_api = Universalis()
        data_centers = self.universalis_api.data_centers()
        available_dcs = [x['name'].lower() for x in data_centers] + [x['region'].lower() for x in data_centers]
        if datacenter.lower() not in available_dcs:
            print("Provided datacenter or region does not exist")
            exit()

        self.items = {}
        '''
        {
            item_ID: {
                "name": str
                "quantity": int
                "alteration": int
                "not_on_market": bool
                "world_prices":{
                    world_ID:{
                        "world_name": str,
                        "listings": [{"price_per_unit": int", quantity": int}, ...]
                    }, ...
                }
                "vendor_info:{
                    "vendor_price_per_unit"： int
                    "vendor_name"： str
                    "vendor_area"： str
                    "vendor_coord"： tuple
                    "vendor_quantity"： int
                }
            }, ...
        }
        '''
        self.worlds = {}
        '''
        {
            world_ID: {
                "name": str
                "dcRegion": str
                "world_total_price": int
                "item_prices":{
                    item_name:{
                        "listings": [{"price_per_unit": int, "quantity": int}, ...]
                        "total_price": int
                        "quantity": int
                        "average": int (float rounds to int)
                    }, ...
                }
            }, ...
        }
        '''
        self.npcs = {}
        '''
        {
            npcid: {
                "name": str
                "area": str
                "coordinate": tuple
                "item_prices":{
                    item_name:{
                        "price_per_unit": int
                        "quantity": int
                    }, ...
                }
            }
        }
        '''
        self.datacenter = datacenter
        self.coverage = coverage
        self.verbose = verbose
        self.alteration_exist = False
        self.not_on_market_exist = False
        self.output = open(output, "w", encoding="utf-8") if output != None else sys.stdout
        



    def create_shopping_list(self):
        self.fetch_and_optimize_listing()
        self.reorganize_listing()

    def add_item(self, item_ID, name):
        if item_ID == 0:
            # Makeplace file also include district information as part of interiorFixture
            # Easiest and safest way of getting around this problem is to ignore item_ID 0
            # As this item id isn't valid anyway
            return False
        
        new_item = False
        if item_ID not in self.items:
            new_item = True
            self.items[item_ID] = {
                "name": name,
                "quantity": 0,
                "alteration": 0,
                "not_on_market": False,
                "world_prices":{},
                "vendor_info": None
            }
        self.items[item_ID]["quantity"] += 1
        return new_item



    def fetch_and_optimize_listing(self):
        # Assume total itemlist is smaller than 100
        # will add a check that breaks up item_IDs if its larger than 100 unique items
        print(f"Fetching item sells data and optimizing for \"{self.coverage}\"")
        for item_ID in self.progressbar(self.items.keys()):
            listing_count = min(self.items[item_ID]["quantity"], 100)
            prices = self.universalis_api.market_board(self.datacenter, item_ID, {'listings':listing_count , 'entries':0})
            if prices == None:
                self.items[item_ID]["not_on_market"] = True
                self.not_on_market_exist = True
                continue
            else:
                alteration, optimized_listings, vendor_info = self.optimizer.optimize(item_ID, self.items[item_ID]["quantity"], prices["listings"])
                self.items[item_ID]["alteration"] = alteration
                self.items[item_ID]["vendor_info"] = vendor_info
                for listing in optimized_listings:
                    world_ID = listing[0]
                    world_name = listing[1]
                    priceperunit = listing[2]
                    quantity = listing[3]
                    if world_ID in self.items[item_ID]["world_prices"]:
                        self.items[item_ID]["world_prices"][world_ID]["listings"].append({"price per unit":priceperunit, "quantity":quantity})
                    else:
                        self.items[item_ID]["world_prices"][world_ID] = {"listings":[{"price per unit":priceperunit, "quantity":quantity}]}
                        self.items[item_ID]["world_prices"][world_ID]["world_name"] = world_name


    def reorganize_listing(self):
        print(f"Reorganizing fetched listing data by worlds for \"{self.coverage}\"")
        for item in self.progressbar(self.items.values()):
            # arrange vendor keyed info to shopper
            if item["vendor_info"] != None:
                vendor_id = item["vendor_info"]["vendor_id"]
                if vendor_id not in self.npcs:
                    self.npcs[vendor_id] = {
                        "name": item["vendor_info"]["vendor_name"],
                        "area": item["vendor_info"]["vendor_area"],
                        "coordinate": item["vendor_info"]["vendor_coord"],
                        "item_prices":{}
                    }
                if item["name"] in self.npcs[vendor_id]["item_prices"]:
                    raise Exception("This shouldn't happen, exiting")
                self.npcs[vendor_id]["item_prices"][item["name"]]={"price_per_unit": item["vendor_info"]["vendor_price_per_unit"], "quantity": item["vendor_info"]["vendor_quantity"]}
            # arrange world keyed info to shopper
            for world_ID, world_info in item["world_prices"].items():
                if world_ID not in self.worlds:
                    self.worlds[world_ID] = {
                        "name": world_info["world_name"],
                        "dcRegion": '',
                        "world_total_price": 0,
                        "item_prices":{}
                    }
                if item["name"] in self.worlds[world_ID]["item_prices"]:
                    raise Exception("This shouldn't happen, exiting")
                self.worlds[world_ID]["item_prices"][item["name"]]={"listings":world_info["listings"]}

        # print(json.dumps(self.items, indent=4))
        # print(json.dumps(self.worlds,indent=4))
        # print(json.dumps(self.npcs,  indent=4))
        # exit()

        for world in self.worlds.values():
            for item in world["item_prices"].values():
                item_total_price = 0
                item_total_count = 0
                for listing in item["listings"]:
                    item_total_count += listing ["quantity"]
                    item_total_price += listing["price per unit"] * listing ["quantity"]
                    world["world_total_price"] += listing["price per unit"] * listing ["quantity"]
                item["total_price"] = item_total_price
                item["quantity"] = item_total_count
                item["average"] = int(item_total_price/item_total_count)

        dc_entries = self.universalis_api.data_centers()
        # world_entries = self.universalis_api.worlds()
        for world_ID, world in self.worlds.items():
            # world_id = None
            # for world_entry in world_entries:
            #     if world["name"] == world_entry['name']:
            #         world_id = world_entry['id']
            for dc_entry in dc_entries:
                if world_ID in dc_entry['worlds']:
                    world["dcRegion"] = dc_entry['name'] + ' ' + dc_entry['region']



    # function that handles progressbar printing during optimizing and reorganizing
    def progressbar(self, it, prefix="", size=40):
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
            print(f'In {world["name"]} {world["dcRegion"]}, {world["world_total_price"]:,} gil total', file=self.output)
            for item_name, item in world["item_prices"].items():
                name = item_name+','
                print(f'\u2514\u2500 {item["quantity"]:>4}x {name:<32} avg price:{item["average"]}', file=self.output)
                if self.verbose:
                    for listing in item["listings"]:
                        print(f'       \u2514\u2500 {listing["quantity"]:>4,} listed,  price per unit:{listing["price per unit"]:,}', file=self.output)
        print('------------------------', file=self.output)

        #---NPC_shopping_list---
        print('\nSome item should be bought from vendor at a cheaper price than market')
        for npc in self.npcs.values():
            print('------------------------', file=self.output)
            print(f'Vendor {npc["name"]} at {npc["area"]}: {npc["coordinate"]}', file=self.output)
            for item_name, item in npc["item_prices"].items():
                name = item_name+','
                print(f'\u2514\u2500 {item["quantity"]:>4}x {name:<32} price:{item["price_per_unit"]}', file=self.output)
        print('------------------------', file=self.output)

        #---Footer---
        total_price = sum([world["world_total_price"] for world in self.worlds.values()]) + sum([sum([item["quantity"] * item["price_per_unit"] for item in npc["item_prices"].values()])for npc in self.npcs.values()])
        print(f"Total Cost: {total_price:,} gil", file=self.output)
        print(f"Items found on {', '.join(world['name'] for world in self.worlds.values())}", file=self.output)
        if self.alteration_exist:
            print("\nThe following item differs from the desired quantities", file=self.output)
            for item in self.items.values():
                if item['alteration']:
                    print(f"   {item['alteration']:>4}x {item['name']}", file=self.output)
        if self.not_on_market_exist:
            print(f"\nThe following item cannot be found on {self.datacenter} marketboard", file=self.output)
            for item in self.items.values():
                if item["not_on_market"]:
                    print(f"   {item['quantity']:>4}x {item['name']}", file=self.output)
        print("\nShopper disconnected, thank you for shopping!", file=self.output)
        self.output.close()
