#!/usr/bin/env python3
from pathlib import Path
import json


print("vsn", "device", "zone", "cpu", "memory", sep="\t")

for path in Path("data").glob("*/kube-nodes.json"):
    vsn = path.parent.stem
    kube_nodes_data = json.loads(path.read_text())
    for item in kube_nodes_data["items"]:
        name = item["metadata"]["name"]
        zone = item["metadata"]["labels"].get("zone", "unknown")
        cpu = item["status"]["capacity"]["cpu"]
        memory = int(item["status"]["capacity"]["memory"].removesuffix("Ki")) * 1024
        print(vsn, name, zone, cpu, round(memory / 1024**3, 3), sep="\t")
