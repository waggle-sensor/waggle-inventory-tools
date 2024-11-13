#!/usr/bin/env python3
from pathlib import Path
import json


print("vsn      device                           zone         cpu     memory    notes")

for path in Path("data").glob("*/kube-nodes.json"):
    vsn = path.parent.stem
    kube_nodes_data = json.loads(path.read_text())
    for item in kube_nodes_data["items"]:
        name = item["metadata"]["name"]
        zone = item["metadata"]["labels"].get("zone", "unknown")
        cpu = item["status"]["capacity"]["cpu"]
        memory = int(item["status"]["capacity"]["memory"].removesuffix("Ki")) * 1024

        notes = []

        if not Path("data", vsn, "devices", name).exists():
            notes.append("unreachable")

        print(
            f"{vsn:8} {name:32} {zone:12} {cpu:4} {memory / 1024**3:8.3f}     {','.join(notes)}"
        )
