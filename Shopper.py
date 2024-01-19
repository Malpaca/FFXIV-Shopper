import requests
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

    def make_shopping_list(self):
        self.get_prices()
        self.formate_worlds()

        self.print_header()
        self.print_world_shopping_list()
        self.print_footer()






    def get_prices(self):
        # Assume total itemlist is smaller than 100
        # will add a check that breaks up itemIds if its larger than 100 unique items
        largest_quantity = max([item.quantity for item in self.items.values()])
        itemIds = ','.join(str(x) for x in self.items.keys())
        print("Fetching Universalis data")
        try:
            universalis_query = 'https://universalis.app/api/v2/{worldDcRegion}/{itemIds}?listings={listings}&entries=0'
            price_request = requests.get(universalis_query.format(
                worldDcRegion=self.datacenter, itemIds=itemIds, listings=largest_quantity))
            prices = price_request.json()
        except:
            print('Error when requesting Universalis API, try later and check API status')

        for itemid in prices["unresolvedItems"]:
            self.items[itemid].not_on_market = True
            self.not_on_market_exist = True
        print("optimizing")
        for itemid in self.items.keys():
            self.optimize_buys_and_process(prices, itemid)
        # Testing Item data storage
        # for item in self.items.values():
        #     print(item.name, item.world_prices)

    def optimize_buys_and_process(self, prices, itemid):
        # Currently it just grab the top [quantity] listing
        # will create a search that minize gil spent to buy at least [quantity] items later
        if not self.items[itemid].not_on_market:
            for listing in prices["items"][str(itemid)]["listings"][:self.items[itemid].quantity]:
                self.items[itemid].add_listing(listing["worldName"], listing["pricePerUnit"], listing["quantity"])





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
