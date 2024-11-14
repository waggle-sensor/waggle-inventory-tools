#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path
import json
import shlex

parser = argparse.ArgumentParser()
parser.add_argument("vsns", nargs="*")
args = parser.parse_args()

# NOTE Most important point is to just capture the raw data for now and save it. We can do further
# processing and indexing downstream. This not only keeps everything but also saves us from the
# paralysis of choosing formats, fields, etc so we can just focus on the problem.

# TODO Decide which items are really core config vs operations.

for vsn in args.vsns:
    vsn = vsn.upper()
    host = f"node-{vsn}"

    def check_output(cmd):
        return subprocess.check_output(["ssh", host, cmd], text=True)

    def save_file(name, data):
        path = Path("data", vsn, name)
        path.parent.mkdir(exist_ok=True, parents=True)
        Path("data", vsn, name).write_text(data)

    def capture(cmd, name):
        data = check_output(cmd)
        save_file(name, data)

    def capture_optional(cmd, name):
        try:
            capture(cmd, name)
        except subprocess.CalledProcessError:
            print(f"WARNING: Optional command {cmd} failed on {vsn}")

    def capture_device(ip, cmd, name):
        if ip == "10.31.81.1":
            capture(cmd, name)
        else:
            capture(f"ssh {ip} {shlex.quote(cmd)}", name)

    def capture_device_optional(ip, cmd, name):
        try:
            capture_device(ip, cmd, name)
        except subprocess.CalledProcessError:
            print(f"WARNING: Optional device command {cmd} failed on {vsn} {ip}")

    # Check if node is reachable.
    check_output("true")  # Check if node is reachable.

    # Check VSN config to make sure matches cloud side VSN to node mapping.
    assert vsn == check_output("cat /etc/waggle/vsn").strip()

    # Scrape per node information.
    capture("cat /var/lib/misc/dnsmasq.leases", "dnsmasq-leases.txt")
    capture("cat /etc/hosts", "etc-hosts.txt")
    capture("kubectl get nodes -o json", "kube-nodes.json")
    capture("nmcli conn", "nmcli-conn.txt")
    capture("nmcli dev", "nmcli-dev.txt")
    capture_optional("mmcli -m 0", "mmcli-modem.txt")
    capture_optional("mmcli -i 0", "mmcli-sim.txt")

    # Scrape per device information.
    kube_nodes_data = json.loads(Path("data", vsn, "kube-nodes.json").read_text())

    for item in kube_nodes_data["items"]:
        name = item["metadata"]["name"]
        assert name == item["metadata"]["annotations"]["k3s.io/hostname"]
        ip = item["metadata"]["annotations"]["k3s.io/internal-ip"]

        if ip != "10.31.81.1":
            try:
                subprocess.check_call(["ssh", host, "ssh", ip, "true"])
            except subprocess.CalledProcessError:
                print(f"ERROR: Device at {vsn} -> {ip} is unreachable. Skipping.")
                continue

        capture_device(ip, "lsusb", f"devices/{name}/lsusb.txt")
        capture_device_optional(
            ip, "cat /sys/bus/iio/devices/*/name", f"devices/{name}/iio-names.txt"
        )

# Using this data, we can then provide users a simple TODO list of things to do. Examples:
# * Set zone on device
# * Set name for cameras (probably something we generate and sync back as dnsmasq config)

# TODO We can also just have the node periodically create a zip archive with all of this info. Then, we can just
# rsync it back.
