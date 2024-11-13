# Waggle Inventory Tools

This repo contains tooling to help scrape relevant information from nodes. It's
a work in process but is intended to automate a lot of the tasks and inventory
management we're currently doing by hand.

## Usage

To scape a node's data, just run:

```sh
./scrape-nodes.py vsn1 vsn2 ...
```

Each node will have their info scraped into the directory `data/vsn/`.

## Ideas

This data will allow us to quickly perform queries such as:

- Which devices have a BME680? (`grep -r bme280 data`)
- List all devices with a Hanwha MAC? (`grep -r 01:e4:30 data`)
- Find all XNV-8081Z cameras without a pinned hostname?
  (`grep -r XNV-8081Z data`)
- Find all devices which need zone label set? (TODO but can use
  `kube-nodes.json` file)
- Find all C-Media microphones.
  (`find data -name lsusb.txt | xargs grep C-Media`)
