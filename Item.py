class Item:
    def __init__(self, name):
        self.name = name
        self.quantity = 0
        self.world_prices = {} #structure: {worldname: {}}
        self.alteration = 0
        self.not_on_market = False

    def add_listing(self, listing):
        if listing["worldName"] in self.world_prices:
            self.world_prices[listing["worldName"]].append({"price per unit":listing["pricePerUnit"], "quantity":listing["quantity"]})
        else:
            self.world_prices[listing["worldName"]]=[{"price per unit":listing["pricePerUnit"], "quantity":listing["quantity"]}]
