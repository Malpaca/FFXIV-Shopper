from .GarlandToolsAPIWrapper import GarlandTools
import numpy as np

class Optimizer:
    def __init__(self):
        self.garlandtools_api = GarlandTools()

    def optimize(self, itemid, desired_quantity, market_listings):
        vendor_price, vendor_id, vendor_name, vendor_area, vendor_coord = self.vendor_look_up(itemid)
        sack_size = int(np.ceil(desired_quantity*1.5)) #I know this is ugly, but since we already use argmin from numpy for search speedup, why not also use it for ceiling
        sack = [float('inf')] * sack_size
        sack[0] = 0
        sack_listings = [[]] * sack_size
        for listing in market_listings:
            if listing["pricePerUnit"] > vendor_price:
            #     print("cheaper vendor price exist")
                continue
            for i in range(sack_size-1, -1, -1):
                if i - listing["quantity"] < 0:
                    continue
                new_sack = sack[i-listing["quantity"]] + listing["pricePerUnit"]*listing["quantity"]
                if new_sack < sack[i]:
                    sack[i] = new_sack
                    sack_listings[i] = sack_listings[i-listing["quantity"]]+[(listing["worldID"], listing["worldName"], listing["pricePerUnit"], listing["quantity"])]
        index_min = np.argmin(sack[desired_quantity:])+desired_quantity
        # index may not be true min, check if corresponding value is finite, 
        # if its not return the right most finite value index if no vendor exist
        if np.isposinf(sack[index_min]):
            for i in range(sack_size-1, -1, -1):
                if not np.isposinf(sack[i]):
                    index_min = i
                    break
        alteration = int(index_min - desired_quantity)
        if alteration >= 0 or vendor_name is None:
            vendor_info = None
        else:
            alteration = 0
            vendor_info = {
                "vendor_price_per_unit": vendor_price,
                "vendor_id": vendor_id,
                "vendor_name": vendor_name,
                "vendor_area": vendor_area,
                "vendor_coord": vendor_coord,
                "vendor_quantity": int(desired_quantity - index_min)
            }
        return alteration, sack_listings[index_min], vendor_info

    def vendor_look_up(self, item_id):
        item_json = self.garlandtools_api.item(item_id)
        core_json = self.garlandtools_api.core()

        if "vendors" in item_json["item"]:
            npc_id = item_json["item"]["vendors"][0]
            npc_json = self.garlandtools_api.npc(npc_id)

            npc_area_id = npc_json["npc"]["zoneid"]
            npc_area = core_json["locationIndex"][str(npc_area_id)]["name"]
            npc_coord = npc_json["npc"]["coords"]
            return item_json["item"]["price"], npc_id, npc_json["npc"]["name"], npc_area, npc_coord
            # print(f"item {item_json["item"]["name"]} can be bought from NPC for {item_json["item"]["price"]}, from {npc_json["npc"]["name"]} located in {npc_area} {npc_coord}")
        else:
            return float('inf'), None, None, None, None   