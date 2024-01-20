# FFXIV-Shopper
FFXIV-Shopper takes in a Makeplace JSON file, and generate a market shopping list of the interior furniture that's seperated into different worlds on your provided datacenter, so you can minimize your shopping time by buying all the item you need from the same world at once.
If certain item can be stacked (I don't think furniture can do that, but I have included the feature for the program to eventually extend into a generic shopping list, not just Makeplace JSON), it will look through the top few marketboard listing and find the cheapest combination of them that satisfy your desired item quantity.
The output is neatly organized into different worlds, with total gil per world, average gil per item for each item in that world, and total gil of the full shopping list.
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
usage: main.py [-h] --file FILE --datacenter DATACENTER [--verbose]

Generate a 'optimized' shopping list given makeplace JSON itemlist

options:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Path to json
  --datacenter DATACENTER, -dc DATACENTER
                        Shopper datacenter name
  --verbose, -v         Verbose, display specific listing for each item instead of just average
```
To have a taste with the example json file, run
```
python main.py -f ShopperTest.json -dc primal -v
```
Which will print out [this example output](#example-output)

## Example Output
```
>>> main.py -f ShopperTest.json -dc Primal -v
File and Datacenter Valid, creating shopping list
Total 5 items received from JSON file
Fetching item sells data and optimizing
    [████████████████████████████████████████] 5/5 Est wait 00:00
Formating fetched listing data into worlds

Shopping list was created on 20/01/2024 10:55:04
------------------------
In Excalibur, 17,999 gil total
└─    1x Alpine Pillar,                   avg price:17999
       └─    1 listed,  price per unit:17,999
------------------------
In Ultros, 26,098 gil total
└─    1x Carbuncle Chronometer,           avg price:98
       └─    1 listed,  price per unit:98
└─    1x Corner Counter,                  avg price:26000
       └─    1 listed,  price per unit:26,000
------------------------
In Leviathan, 121,434 gil total
└─    2x Cooking Stove,                   avg price:60717
       └─    1 listed,  price per unit:60,717
       └─    1 listed,  price per unit:60,717
------------------------
In Lamia, 76,999 gil total
└─    2x Corner Counter,                  avg price:38499
       └─    1 listed,  price per unit:38,000
       └─    1 listed,  price per unit:38,999
------------------------
Total Cost: 242,530 gil
Items found on Excalibur, Ultros, Leviathan, Lamia

The following item cannot be found on Primal marketboard
      1x Stuffed Fox

Shopper disconnected, thank you for shopping!
```

## TODO
- [x] Implement listing optimizations
- [ ] Shopping list for exterior furniture
- [ ] Shopping list for fixtures
- [ ] Shopping list for dyes
- [ ] Shopping list for generic item list (non Makeplace JSON input)
