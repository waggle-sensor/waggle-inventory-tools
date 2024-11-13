#!/usr/bin/env python3
from pathlib import Path
import json


def log(vsn, level, *args):
    print(vsn, level, *args, sep="\t", flush=True)


# Example of finding all devices missing a zone.
for path in Path("data").glob("*/kube-nodes.json"):
    vsn = path.parent.stem
    kube_nodes_data = json.loads(path.read_text())
    for item in kube_nodes_data["items"]:
        name = item["metadata"]["name"]
        zone = item["metadata"]["labels"].get("zone")
        if not zone:
            log(vsn, "ERROR", f"missing zone for {name}")
        if zone not in ["core", "agent", "shield", "enclosure"]:
            log(vsn, "ERROR", f"invalid zone {zone} for {name}")
        if not Path("data", vsn, "devices", name).exists():
            log(vsn, "WARNING", f"device {name} in k3s but not scraped")
