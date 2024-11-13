#!/usr/bin/env python3
from pathlib import Path
import json

fmt = "%-8s %-32s %-12s %-4s %-8s %s"

print(fmt % ("vsn", "device", "zone", "cpu", "memory", "notes"))

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

        print(fmt % (vsn, name, zone, cpu, round(memory / 1024**3, 3), ",".join(notes)))
