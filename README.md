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

_Note: This assumes your node ssh config is using the convention
`ssh node-vsn`._

## Ideas

This data will allow us to quickly perform queries such as:

- Which devices have a BME680? (`grep -r bme280 data`)
- List all devices with a Hanwha MAC? (`grep -r e4:30:22 data`)
- Find all XNV-8081Z cameras without a pinned hostname?
  (`grep -r XNV-8081Z data`)
- Find all devices which need zone label set? (See example in
  [print-issues.py](./print-issues.py))
- Find all C-Media microphones.
  (`find data -name lsusb.txt | xargs grep C-Media`)

## Example Data Layout

At the moment, here's an example of what [scrape-nodes.py](./scrape-nodes.py)
collects about a node like W022:

```
data/W022
data/W022/mmcli-sim.txt
data/W022/mmcli-modem.txt
data/W022/kube-nodes.json
data/W022/dnsmasq-leases.txt
data/W022/devices
data/W022/devices/0000d83add18cb30.ws-rpi
data/W022/devices/0000d83add18cb30.ws-rpi/iio-names.txt
data/W022/devices/0000d83add18cb30.ws-rpi/lsusb.txt
data/W022/devices/0000e45f012a1f42.ws-rpi
data/W022/devices/0000e45f012a1f42.ws-rpi/iio-names.txt
data/W022/devices/0000e45f012a1f42.ws-rpi/lsusb.txt
data/W022/devices/000048b02d15bda5.ws-nxcore
data/W022/devices/000048b02d15bda5.ws-nxcore/iio-names.txt
data/W022/devices/000048b02d15bda5.ws-nxcore/lsusb.txt
data/W022/devices/000048b02d3b12f9.ws-nxagent
data/W022/devices/000048b02d3b12f9.ws-nxagent/iio-names.txt
data/W022/devices/000048b02d3b12f9.ws-nxagent/lsusb.txt
```
