# FFXIV-Shopper
FFXIV-Shopper takes in a Makeplace JSON file, and generate a market shopping list that's seperated into different worlds on your provided datacenter/region, so you can minimize your money and shopping time by buying all the item you need from a world at once with (hopefully) the lowest cost.
If certain item can be stacked (I don't think furniture can do that, but I have included the feature for the program to eventually extend into a generic shopping list, not just Makeplace JSON), it will look through the top few marketboard listing and find the cheapest combination of them that satisfy your desired item quantity.
If in game vendor exist for the item, it will reject all market listing that is above the vendor price and inform you to buy from the vendor instead, with vendor name, location, and coordinate given
The output is neatly organized into different worlds, with total gil per world, average gil per item for each item in that world, and total gil of the full shopping list.
The output can also be seperated into 4 different list using the seperate argument, that distinguish interior/exterior furniture/fixture. Eventually also distinguish between different input shopping list.
It can also be run with a verbose argument, that prints out the selected listings for an item for more information but will make the shopping list bit more cluttered, refer to [this section](#running-the-program) for detail.

## Requirement
This program uses ```argparse``` and ```numpy``` for argument parsing and minor math speed up (very minor, but I'm lazy to write a non numpy version), and ```requests``` and ```requests-cache``` for html get requests
Install requirement via
```
python -m pip install argparse numpy requests requests-cache
```
or
```
python3 -m pip install argparse numpy requests requests-cache
```
Depending on your python alias on your system

## Running the program
The program can only be run in commandline, maybe I'll make a GUI version in the future, but so far only commandline

```
usage: main.py [-h] --File FILE [FILE ...] --DatacenterRegion DATACENTERREGION [--Output OUTPUT] [--Seperate] [--Verbose]

Generate a 'optimized' shopping list given makeplace JSON itemlist

options:
  -h, --help            show this help message and exit
  --File FILE [FILE ...], -f FILE [FILE ...]
                        Path to json
  --DatacenterRegion DATACENTERREGION, -dcRegion DATACENTERREGION
                        Shopper region or datacenter name (use dash in place of space)
  --Output OUTPUT, -o OUTPUT
                        Name of output file, also remove the output in command line
  --Seperate            Create different shopping list for each section of the JSON file: interior/exterior fixture/furnitures
  --Verbose             Verbose, display specific listing for each item instead of just average
```
To have a taste with the example json file, run
```
python main.py -f ShopperTest.json -dcRegion north-america --Verbose
```
Which will print out [this example output](#example-output)

## Example Output
```
>>> python main.py -f ShopperTest.json -dcRegion north-america --Verbose
File location Valid, creating shopping list
Reading JSON file
Received 5 items from interiorFurniture section
Received 3 items from interiorFixture section
Received 2 items from exteriorFixture section
Total 10 unique items received from JSON file

Fetching item sells data and optimizing for "ShopperTest:All"
  [████████████████████████████████████████] 10/10 Est wait 00:00
Reorganizing fetched listing data by worlds for "ShopperTest:All"
  [████████████████████████████████████████] 10/10 Est wait 00:00



Shopping list for "ShopperTest:All" created on 05/08/2024 11:53:10
------------------------
In Coeurl Crystal North-America, 125 gil total
└─    1x Carbuncle Chronometer,           avg price:125
       └─    1 listed,  price per unit:125
------------------------
In Gilgamesh Aether North-America, 80,150 gil total
└─    1x Cooking Stove,                   avg price:80000
       └─    1 listed,  price per unit:80,000
└─    1x Storm Blue Interior Wall,        avg price:150
       └─    1 listed,  price per unit:150
------------------------
In Hyperion Primal North-America, 85,598 gil total
└─    1x Cooking Stove,                   avg price:84999
       └─    1 listed,  price per unit:84,999
└─    1x Storm Blue Interior Wall,        avg price:599
       └─    1 listed,  price per unit:599
------------------------
In Cactuar Aether North-America, 38,997 gil total
└─    3x Corner Counter,                  avg price:12999
       └─    1 listed,  price per unit:12,999
       └─    1 listed,  price per unit:12,999
       └─    1 listed,  price per unit:12,999
------------------------
In Exodus Primal North-America, 4,500 gil total
└─    1x Glade Flooring,                  avg price:4500
       └─    1 listed,  price per unit:4,500
------------------------
In Malboro Crystal North-America, 400 gil total
└─    2x Crystal Chandelier,              avg price:200
       └─    1 listed,  price per unit:200
       └─    1 listed,  price per unit:200
------------------------
In Famfrit Primal North-America, 333 gil total
└─    1x Riviera Arched Window,           avg price:333
       └─    1 listed,  price per unit:333
------------------------
In Diabolos Crystal North-America, 300 gil total
└─    1x Riviera Wooden Door,             avg price:300
       └─    1 listed,  price per unit:300
------------------------

Some item should be bought from vendor at a cheaper price than market
------------------------
Vendor Housing Merchant at Mist: [10.87, 11.51]
└─    1x Alpine Pillar,                   price:3500
└─    1x Glade Flooring,                  price:5000
------------------------
Total Cost: 218,903 gil
Items found on Coeurl, Gilgamesh, Hyperion, Cactuar, Exodus, Malboro, Famfrit, Diabolos

The following item cannot be found on North-America marketboard
      1x Stuffed Fox

Shopper disconnected, thank you for shopping!
```

## TODO
- [x] Implement listing optimizations
- [x] Shopping list for all housing criteria (interior/exterior furniture/fixture)
- [x] GarlandTools API Vendor price lookup (So you don't pay for overprice market item)
- [ ] Shopping list for dyes
- [ ] Shopping list for generic item list (non Makeplace JSON input)
- [ ] GUI
