from pathlib import Path
import json

# Example of finding all devices missing a zone.
for path in Path("data").rglob("kube-nodes.json"):
    vsn = path.parent.stem
    kube_nodes_data = json.loads(path.read_text())
    for item in kube_nodes_data["items"]:
        name = item["metadata"]["name"]
        zone = item["metadata"]["labels"].get("zone")
        if not zone:
            print(f"Missing zone for {vsn} {name}")
        if zone not in ["core", "agent", "shield", "enclosure"]:
            print(f"Invalid zone for {vsn} {name}: {zone}")
