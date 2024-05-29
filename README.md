# FFXIV-Shopper
FFXIV-Shopper takes in a Makeplace JSON file, and generate a market shopping list that's seperated into different worlds on your provided datacenter, so you can minimize your money shopping time by buying all the item you need from the same world at once with (hopefully) the lowest cost.
If certain item can be stacked (I don't think furniture can do that, but I have included the feature for the program to eventually extend into a generic shopping list, not just Makeplace JSON), it will look through the top few marketboard listing and find the cheapest combination of them that satisfy your desired item quantity.
The output is neatly organized into different worlds, with total gil per world, average gil per item for each item in that world, and total gil of the full shopping list.
The output can also be seperated into 4 different list that distinguish interior/exterior furniture/fixture. Eventually also distinguish between different input shopping list.
It can also be run with a verbose argument that prints out the selected listings for an item for more information but will make the shopping list very cluttered, refer to [this section](#running-the-program) for detail.

## Requirement
This program uses ```argparse``` and ```numpy``` for argument parsing and minor math speed up (very minor, but I'm lazy to write a non numpy version)
Install requirement via
```
python -m pip install argparse numpy
```
or
```
python3 -m pip install argparse numpy
```
Depending on your python alias on your system

## Running the program
The program can only be run in commandline, maybe I'll make a GUI version in the future, but so far only commandline

```
usage: main.py [-h] --file FILE [FILE ...] --datacenter DATACENTER [--output OUTPUT] [--seperate] [--verbose]

Generate a 'optimized' shopping list given makeplace JSON itemlist

options:
  -h, --help            show this help message and exit
  --file FILE [FILE ...], -f FILE [FILE ...]
                        Path to json
  --datacenter DATACENTER, -dc DATACENTER
                        Shopper datacenter name
  --output OUTPUT, -o OUTPUT
                        Name of output file, also remove the output in command line
  --seperate            Create different shopping list for each section of the JSON file: interior/exterior
                        fixture/furnitures
  --verbose             Verbose, display specific listing for each item instead of just average
```
To have a taste with the example json file, run
```
python main.py -f ShopperTest.json -dc primal --verbose
```
Which will print out [this example output](#example-output)

## Example Output
```
>>> python main.py -f ShopperTest.json -dc primal --verbose
File and Datacenter Valid, creating shopping list
Reading JSON file
Received 5 items from interiorFurniture section
Received 4 items from interiorFixture section
Received 2 items from exteriorFixture section
Total 11 unique items received from JSON file

Fetching item sells data and optimizing for "ShopperTest:All"
  [████████████████████████████████████████] 11/11 Est wait 00:00
Reorganizing fetched listing data by worlds for "ShopperTest:All"
  [████████████████████████████████████████] 11/11 Est wait 00:00



Shopping list for "ShopperTest:All" created on 29/05/2024 16:58:39
------------------------
In Ultros, 18,998 gil total
└─    1x Alpine Pillar,                   avg price:13999
       └─    1 listed,  price per unit:13,999
└─    1x Glade Flooring,                  avg price:4999
       └─    1 listed,  price per unit:4,999
------------------------
In Lamia, 900 gil total
└─    1x Carbuncle Chronometer,           avg price:900
       └─    1 listed,  price per unit:900
------------------------
In Leviathan, 179,823 gil total
└─    2x Cooking Stove,                   avg price:60717
       └─    1 listed,  price per unit:60,717
       └─    1 listed,  price per unit:60,717
└─    3x Corner Counter,                  avg price:18500
       └─    1 listed,  price per unit:18,500
       └─    1 listed,  price per unit:18,500
       └─    1 listed,  price per unit:18,500
└─    2x Storm Blue Interior Wall,        avg price:299
       └─    1 listed,  price per unit:250
       └─    1 listed,  price per unit:349
└─    2x Crystal Chandelier,              avg price:1145
       └─    1 listed,  price per unit:1,140
       └─    1 listed,  price per unit:1,150
------------------------
In Exodus, 8,999 gil total
└─    1x Glade Flooring,                  avg price:8999
       └─    1 listed,  price per unit:8,999
------------------------
In Behemoth, 32 gil total
└─    1x Riviera Arched Window,           avg price:32
       └─    1 listed,  price per unit:32
------------------------
In Excalibur, 999 gil total
└─    1x Riviera Wooden Door,             avg price:999
       └─    1 listed,  price per unit:999
------------------------
Total Cost: 209,751 gil
Items found on Ultros, Lamia, Leviathan, Exodus, Behemoth, Excalibur

The following item cannot be found on primal marketboard
      1x Stuffed Fox

Shopper disconnected, thank you for shopping!
```

## TODO
- [x] Implement listing optimizations
- [x] Shopping list for exterior furniture
- [x] Shopping list for fixtures
- [ ] Shopping list for dyes
- [ ] Shopping list for generic item list (non Makeplace JSON input)
- [ ] GarlandTools API Vendor price lookup (So you don't pay for overprice market item)
- [ ] GUI
