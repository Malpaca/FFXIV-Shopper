# FFXIV-Shopper
usage: main.py [-h] --file FILE --datacenter DATACENTER [--verbose]

Generate a 'optimized' shopping list given makeplace JSON itemlist

options:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Path to json
  --datacenter DATACENTER, -dc DATACENTER
                        Shopper datacenter name
  --verbose, -v         Verbose, display specific listing for each item instead of just average

## TODO
Actually implement the optimization step. Currently it only accept makeplace JSON file since all item have 1 count, and we can just grab the top N item on the marketboard. But stackable item it will look through top M marketboard listing and choose a combination that buys required amount of item with least amount of gil spent (e.g., crystals usually sell in stack of 5000, but if you only need 500 then its worth buying a listing with more price per item but less total price)

## Example Output
```
Shopping list was created on 16/01/2024 05:47:56
------------------------
In Hyperion, 21,800 gil total
└─    1x Alpine Pillar,                   avg price:21800
       └─    1 listed,  price per unit:21,800
------------------------
In Ultros, 87,150 gil total
└─    1x Carbuncle Chronometer,           avg price:150
       └─    1 listed,  price per unit:150
└─    3x Corner Counter,                  avg price:29000
       └─    1 listed,  price per unit:29,000
       └─    1 listed,  price per unit:29,000
       └─    1 listed,  price per unit:29,000
------------------------
In Leviathan, 60,717 gil total
└─    1x Cooking Stove,                   avg price:60717
       └─    1 listed,  price per unit:60,717
------------------------
In Famfrit, 83,495 gil total
└─    1x Cooking Stove,                   avg price:83495
       └─    1 listed,  price per unit:83,495
------------------------
Total Cost: 253,162 gil
Items found on Hyperion, Ultros, Leviathan, Famfrit

Shopper disconnected, thank you for shopping!
```
