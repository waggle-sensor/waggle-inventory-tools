#!/usr/bin/env python3
from pathlib import Path
import json

# Example of finding all devices missing a zone.
for path in Path("data").glob("*/kube-nodes.json"):
    vsn = path.parent.stem
    kube_nodes_data = json.loads(path.read_text())
    for item in kube_nodes_data["items"]:
        name = item["metadata"]["name"]
        zone = item["metadata"]["labels"].get("zone")
        if not zone:
            print(f"ERROR: Missing zone for {vsn} {name}")
        if zone not in ["core", "agent", "shield", "enclosure"]:
            print(f"ERROR: Invalid zone for {vsn} {name}: {zone}")
        if not Path("data", vsn, "devices", name).exists():
            print("WARNING: Device in k3s but not scraped", vsn, name)
