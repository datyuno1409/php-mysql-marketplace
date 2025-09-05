#!/usr/bin/env python3
import subprocess
import shlex

HOST = "root@103.9.205.28"
PORT = "2012"

COMMANDS = [
    "which kubectl || echo 'kubectl not found'",
    "kubectl version --client --output=yaml | cat",
    "kubectl version --output=yaml | cat",
    "kubectl cluster-info | cat",
    "kubectl get nodes -o wide | cat",
    "kubectl get ns | cat",
]

def run(cmd: str) -> str:
    full = f"ssh -p {PORT} {HOST} \"{cmd}\""
    proc = subprocess.run(shlex.split(full), capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    return out.strip()

def main():
    print("Kubernetes Connectivity Check")
    print("=" * 32)
    results = {}
    for c in COMMANDS:
        print(f"\n=== {c} ===")
        results[c] = run(c)
        print(results[c])

    summary = {
        "kubectl_present": "not found" not in results[COMMANDS[0]].lower(),
        "cluster_info_ok": "Kubernetes control plane" in results[COMMANDS[3]] or "Error" not in results[COMMANDS[3]],
        "nodes_listed": ("NAME" in results[COMMANDS[4]] and len(results[COMMANDS[4]].splitlines()) > 1),
    }

    print("\nSummary:")
    for k, v in summary.items():
        print(f"- {k}: {v}")

    connected = summary["kubectl_present"] and summary["nodes_listed"]
    print(f"\nConnected to Kubernetes: {connected}")

if __name__ == "__main__":
    main()


