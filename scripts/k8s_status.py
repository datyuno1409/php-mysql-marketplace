#!/usr/bin/env python3
import subprocess
import shlex

HOST = "root@103.9.205.28"
PORT = "2012"

CMDS = [
    ("kubectl which", "which kubectl || echo 'kubectl not found'"),
    ("version", "kubectl version --output=yaml | cat"),
    ("cluster-info", "kubectl cluster-info | cat"),
    ("namespaces", "kubectl get ns | cat"),
    ("marketplace ns", "kubectl get ns marketplace -o yaml | cat"),
    ("deployments all", "kubectl get deploy -A -o wide | cat"),
    ("pods all", "kubectl get pods -A -o wide | cat"),
    ("services all", "kubectl get svc -A -o wide | cat"),
]

def run(cmd: str) -> str:
    full = f"ssh -p {PORT} {HOST} \"{cmd}\""
    proc = subprocess.run(shlex.split(full), capture_output=True, text=True)
    return (proc.stdout or "") + (proc.stderr or "")

def main():
    print("K8s Status Check")
    print("=" * 20)
    results = {}
    for name, cmd in CMDS:
        print(f"\n=== {name} ===")
        out = run(cmd)
        results[name] = out
        print(out)

    has_kubectl = "not found" not in results["kubectl which"].lower()
    has_market_ns = "marketplace" in results["namespaces"]
    has_any_pods = any(l.strip() and not l.lower().startswith("namespace") and not l.lower().startswith("name") for l in results["pods all"].splitlines()[1:])
    print("\nSummary:")
    print(f"- kubectl present: {has_kubectl}")
    print(f"- marketplace namespace exists: {has_market_ns}")
    print(f"- any pods present: {has_any_pods}")

if __name__ == "__main__":
    main()


