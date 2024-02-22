class World:
    def __init__(self, name):
        self.name = name
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
