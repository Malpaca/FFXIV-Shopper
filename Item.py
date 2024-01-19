class Item:
    def __init__(self, name):
        self.name = name
        self.quantity = 0
        self.world_prices = {} #structure: {worldname: {}}
        self.alteration = 0
        self.not_on_market = False

    def add_listing(self, worldname, priceperunit, quantity):
        if worldname in self.world_prices:
            self.world_prices[worldname].append({"price per unit":priceperunit, "quantity":quantity})
        else:
            self.world_prices[worldname]=[{"price per unit":priceperunit, "quantity":quantity}]
